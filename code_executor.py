"""
极简自主编排引擎 - 代码即编排
核心：模型输出 Python 代码，exec 执行，无 JSON、无 DAG。
"""
import re
import textwrap
import traceback
import multiprocessing
from RestrictedPython import compile_restricted, safe_builtins, utility_builtins
from RestrictedPython.PrintCollector import PrintCollector
from RestrictedPython.Eval import default_guarded_getitem
from RestrictedPython.Guards import safer_getattr

# 1. 内置环境：安全 + 常用工具函数
EXEC_BUILTINS = safe_builtins.copy()
EXEC_BUILTINS.update(utility_builtins)

# 2. 原子工具集（纯函数，__doc__ 自动生成描述）
def get_weather(city: str):
    """获取城市天气。用法: tools['get_weather']('北京')"""
    return f"{city}天气：晴"


def calculator(expr: str):
    """四则运算。用法: tools['calculator']('1+2*3')"""
    import ast
    import operator
    op_map = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}
    tree = ast.parse(expr.strip(), mode="eval")
    if not isinstance(tree.body, (ast.BinOp, ast.Constant, ast.UnaryOp)):
        raise ValueError("仅支持 + - * / 运算")
    def eval_node(n):
        if isinstance(n, ast.Constant):
            return n.value
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
            return -eval_node(n.operand)
        if isinstance(n, ast.BinOp) and type(n.op) in op_map:
            return op_map[type(n.op)](eval_node(n.left), eval_node(n.right))
        raise ValueError("仅支持四则运算")
    return str(eval_node(tree.body))


TOOLS = {"get_weather": get_weather, "calculator": calculator}


def _worker(code: str, queue: multiprocessing.Queue) -> None:
    """子进程内执行，结果通过 Queue 传回。"""
    try:
        code_with_capture = textwrap.dedent(code).rstrip() + "\n\nagent_output = printed"
        byte_code = compile_restricted(code_with_capture, filename="<agent>", mode="exec")
        exec_globals = {
            "__builtins__": EXEC_BUILTINS,
            "tools": TOOLS,
            "_print_": PrintCollector,
            "_getattr_": safer_getattr,
            "_getitem_": default_guarded_getitem,
        }
        exec(byte_code, exec_globals)
        output = exec_globals.get("agent_output", "")
        queue.put((True, str(output).strip()))
    except (ImportError, NameError) as e:
        err_msg = str(e)
        if "__import__" in err_msg or "open" in err_msg.lower():
            queue.put((False, "RestrictionError: 禁止 import/open，仅可通过 tools 调用。"))
        else:
            queue.put((False, f"{type(e).__name__}: {err_msg}"))
    except AttributeError as e:
        err_msg = str(e)
        if "starts with \"_\"" in err_msg or "format" in err_msg.lower():
            queue.put((False, "RestrictionError: 禁止访问 _ 开头属性或 str.format，这是安全限制非权限问题。"))
        else:
            queue.put((False, f"AttributeError: {err_msg}"))
    except (PermissionError, OSError) as e:
        queue.put((False, f"PermissionError: {e}。请检查路径或通过 tools 提供的接口操作。"))
    except SyntaxError as e:
        err_msg = str(e)
        if "starts with \"_\"" in err_msg or "invalid attribute" in err_msg.lower():
            queue.put((False, "RestrictionError: 禁止访问 _ 开头属性，这是安全限制非权限问题。"))
        else:
            queue.put((False, f"SyntaxError: {err_msg}"))
    except Exception:
        queue.put((False, traceback.format_exc().splitlines()[-1]))


def safe_run(llm_text: str, timeout: int = 5) -> tuple[bool, str]:
    """
    从 LLM 输出中提取并安全执行 Python 代码。
    返回 (success, result_or_error_msg)。
    """
    match = re.search(r"```(?:python)?\s*(.*?)\s*```", llm_text, re.DOTALL)
    if not match:
        return False, "FormatError: 未检测到代码块，请用 ```python ... ``` 包裹代码。"

    code = match.group(1).strip()
    if not code:
        return False, "FormatError: 代码块为空。"

    queue = multiprocessing.Queue()
    proc = multiprocessing.Process(target=_worker, args=(code, queue))
    proc.start()
    proc.join(timeout)

    if proc.is_alive():
        proc.terminate()
        proc.join(timeout=1)
        if proc.is_alive():
            proc.kill()
        return False, f"TimeoutError: 执行超过 {timeout}s，请检查死循环。"

    try:
        return queue.get(timeout=0.5)
    except Exception:
        return False, "ExecutionError: 子进程异常退出，无反馈。"


def run_agent(user_prompt: str, llm_client, max_retries: int = 3) -> str | None:
    """
    自主编排循环：Think → Code → Execute → Observe。
    llm_client 需实现 chat(messages) -> str。
    """
    tool_desc = {k: v.__doc__ for k, v in TOOLS.items()}
    system_msg = (
        f"你是自动化 Agent。环境禁止 import，只能用 tools['name'](args)。"
        f"输出代码须包含在 ```python ... ``` 中，并 print 最终结果。"
        f"可用工具: {tool_desc}"
    )
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_prompt},
    ]

    for _ in range(max_retries):
        response = llm_client.chat(messages)
        success, result = safe_run(response)

        if success:
            return result

        messages.append({"role": "assistant", "content": response})
        messages.append({"role": "user", "content": f"报错了: {result}。请修正代码。"})

    return None


if __name__ == "__main__":
    # 测试 1：正常执行
    ok_input = "```python\nprint(tools['get_weather']('北京'))\n```"
    ok, res = safe_run(ok_input)
    print(f"测试1 正常: {ok} | {res}")

    # 测试 2：非法 import
    bad_input = "```python\nimport os\nprint(os.getcwd())\n```"
    ok, res = safe_run(bad_input)
    print(f"测试2 非法import: {ok} | {res}")

    # 测试 3：无代码块
    no_block = "北京天气怎么样？"
    ok, res = safe_run(no_block)
    print(f"测试3 无代码块: {ok} | {res}")

    # 测试 4：超时（死循环）
    loop_input = "```python\nwhile True: pass\n```"
    ok, res = safe_run(loop_input, timeout=1)
    print(f"测试4 超时: {ok} | {res}")

    # 测试 5：整体多缩进（dedent 归一化）
    indent_input = "```python\n    print(tools['get_weather']('上海'))\n```"
    ok, res = safe_run(indent_input)
    print(f"测试5 多缩进: {ok} | {res}")

    # 测试 6：safer_getattr 拦截 _ 属性（权限误区：实为安全限制）
    attr_input = "```python\nx = tools.__dict__\nprint(x)\n```"
    ok, res = safe_run(attr_input)
    print(f"测试6 _属性拦截: {ok} | {res}")
