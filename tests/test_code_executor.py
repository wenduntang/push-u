# tests/test_code_executor.py
"""极简自主编排引擎：正向自测 + 逆向自测"""
import sys
from pathlib import Path

# 将项目根目录加入 path，以便导入 code_executor
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from code_executor import safe_run


# ========== 正向自测：预期成功的用例 ==========

def test_forward_normal_execution():
    """正向：正常执行，返回工具输出"""
    ok, res = safe_run("```python\nprint(tools['get_weather']('北京'))\n```")
    assert ok is True
    assert "北京" in res
    assert "晴" in res


def test_forward_dedent_normalization():
    """正向：整体多缩进，dedent 归一化后执行成功"""
    ok, res = safe_run("```python\n    print(tools['get_weather']('上海'))\n```")
    assert ok is True
    assert "上海" in res


def test_forward_multi_line_output():
    """正向：多行 print 输出"""
    ok, res = safe_run("```python\nprint('a')\nprint('b')\n```")
    assert ok is True
    assert "a" in res and "b" in res


def test_forward_pure_computation():
    """正向：纯计算，无工具调用"""
    ok, res = safe_run("```python\nprint(1 + 2 * 3)\n```")
    assert ok is True
    assert res == "7"


# ========== 逆向自测：预期失败的用例 ==========

def test_reverse_no_code_block():
    """逆向：无代码块 → FormatError"""
    ok, res = safe_run("北京天气怎么样？")
    assert ok is False
    assert "FormatError" in res or "代码块" in res


def test_reverse_empty_code_block():
    """逆向：空代码块 → FormatError"""
    ok, res = safe_run("```python\n\n```")
    assert ok is False
    assert "FormatError" in res or "空" in res


def test_reverse_illegal_import():
    """逆向：非法 import → RestrictionError"""
    ok, res = safe_run("```python\nimport os\nprint(os.getcwd())\n```")
    assert ok is False
    assert "RestrictionError" in res or "import" in res.lower()


def test_reverse_timeout():
    """逆向：死循环 → TimeoutError"""
    ok, res = safe_run("```python\nwhile True: pass\n```", timeout=1)
    assert ok is False
    assert "Timeout" in res


def test_reverse_underscore_attribute():
    """逆向：访问 _ 开头属性 → RestrictionError"""
    ok, res = safe_run("```python\nx = tools.__dict__\nprint(x)\n```")
    assert ok is False
    assert "RestrictionError" in res or "安全限制" in res


def test_reverse_name_error():
    """逆向：未定义变量 → NameError"""
    ok, res = safe_run("```python\nprint(undefined_var)\n```")
    assert ok is False
    assert "NameError" in res or "undefined" in res.lower()


def test_reverse_syntax_error():
    """逆向：语法错误 → SyntaxError"""
    ok, res = safe_run("```python\nprint(\n```")
    assert ok is False
    assert "SyntaxError" in res
