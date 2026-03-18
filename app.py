"""
沙箱 + 极简编排 + 符号神经融合 - 统一 Demo 入口
"""
import streamlit as st

st.set_page_config(page_title="沙箱与编排 Demo", page_icon="🛡️", layout="centered")

# 侧边栏导航
demo_type = st.sidebar.radio(
    "选择 Demo",
    ["🛡️ 沙箱运行环境", "⚡ 极简编排引擎", "🧠 符号神经融合AI"],
    label_visibility="collapsed",
)

# ========== 沙箱运行环境 Demo ==========
if demo_type == "🛡️ 沙箱运行环境":
    st.title("🛡️ 沙箱安全运行环境")
    st.caption("Docker/进程双重隔离 · 正逆向验证")

    st.markdown("""
    **功能**：隔离运行不可信命令，支持白名单、资源配额、环境校验。
    
    👇 输入命令，选择白名单模式，查看运行结果。
    """)

    st.subheader("运行配置")
    col1, col2 = st.columns(2)
    with col1:
        command = st.text_input("命令", value="echo ok", help="要执行的命令")
    with col2:
        whitelist_mode = st.selectbox(
            "白名单模式",
            ["全部允许（演示模式）", "仅允许 echo"],
            help="仅允许 echo 时，其他命令会被拒绝",
        )

    allowed = ["echo ok", "echo hello"] if "仅允许" in whitelist_mode else []

    if st.button("▶ 运行沙箱", type="primary"):
        try:
            from sandbox_core import SandboxRunner
            from sandbox_core.config import SandboxConfig, WhitelistConfig

            cfg = SandboxConfig(command=command)
            if allowed:
                cfg.whitelist.allowed_commands = allowed

            runner = SandboxRunner(cfg)
            result = runner.run()

            if result.get("ok"):
                st.success("✅ 运行成功")
                st.json(result)
            else:
                st.error("❌ 运行失败")
                st.code(result.get("error", "unknown"))
                st.info("💡 正向验证：命令不在白名单内")
        except Exception as e:
            st.error(f"执行异常: {e}")
            st.exception(e)

    st.divider()
    st.markdown("""
    **验证流程**：正向 → 启动 → 逆向
    - 正向：白名单、资源配额、环境检查
    - 逆向：审计日志、资源用量、环境篡改检测
    """)

# ========== 极简编排引擎 Demo ==========
elif demo_type == "⚡ 极简编排引擎":
    from code_executor import safe_run, TOOLS

    st.title("⚡ 极简自主编排引擎")
    st.caption("代码即编排 · 无 JSON · 无 DAG")

    st.markdown("""
    **核心理念**：模型输出 Python 代码，引擎安全执行。逻辑在代码里，不在 Prompt 里。
    """)

    EXAMPLES = {
        "北京天气": """```python
print(tools['get_weather']('北京'))
```""",
        "多城市对比": """```python
cities = ['北京', '上海', '广州']
for c in cities:
    print(tools['get_weather'](c))
```""",
        "四则运算": """```python
print(tools['calculator']('1+2*3'))
```""",
        "组合任务": """```python
w = tools['get_weather']('杭州')
n = tools['calculator']('10*2')
print(f'{w}，温度计算: {n}')
```""",
        "❌ 非法 import": """```python
import os
print(os.getcwd())
```""",
        "❌ 未定义变量": """```python
print(undefined_var)
```""",
    }

    example = st.selectbox("选择示例", list(EXAMPLES.keys()))
    code_input = st.text_area("代码", value=EXAMPLES[example], height=120)

    if st.button("▶ 运行", type="primary"):
        with st.spinner("执行中..."):
            ok, result = safe_run(code_input, timeout=5)
        if ok:
            st.success("✅ 执行成功")
            st.code(result, language=None)
        else:
            st.error("❌ 执行失败")
            st.code(result, language=None)
            st.info("💡 Fail-fast：报错回传 LLM，自主 Debug")

    st.divider()
    st.markdown("### 可用工具")
    for name, func in TOOLS.items():
        st.markdown(f"- **{name}**: `{func.__doc__ or ''}`")

# ========== 符号神经融合AI Demo ==========
else:
    from code_executor import safe_run, run_agent, TOOLS

    st.title("🧠 符号神经融合 AI")
    st.caption("神经生成符号 · 符号执行反馈 · 闭环自主")

    st.markdown("""
    **融合架构**：
    - **神经（Neural）**：LLM 理解用户意图，生成 Python 代码
    - **符号（Symbolic）**：受限执行引擎运行代码，逻辑确定、可验证
    - **融合**：神经输出符号，符号执行反馈神经，形成 Think→Code→Execute→Observe 闭环

    👇 输入自然语言，模拟 LLM 生成代码并执行（演示模式）。
    """)

    # 模拟 LLM：根据关键词返回预设代码
    MOCK_RESPONSES = {
        "北京": "```python\nprint(tools['get_weather']('北京'))\n```",
        "上海": "```python\nprint(tools['get_weather']('上海'))\n```",
        "天气": "```python\nfor c in ['北京','上海']:\n    print(tools['get_weather'](c))\n```",
        "计算": "```python\nprint(tools['calculator']('1+2*3'))\n```",
        "杭州": "```python\nprint(tools['get_weather']('杭州'))\n```",
    }

    class MockLLM:
        def chat(self, messages):
            last = messages[-1]["content"] if messages else ""
            for k, v in MOCK_RESPONSES.items():
                if k in last:
                    return v
            return "```python\nprint(tools['get_weather']('北京'))\n```"

    prompt = st.text_input("输入自然语言（如：北京天气、计算1+2*3）", value="北京天气怎么样？")

    if st.button("▶ 运行融合循环", type="primary"):
        with st.spinner("神经生成 → 符号执行 → 观察反馈..."):
            result = run_agent(prompt, MockLLM(), max_retries=3)

        if result:
            st.success("✅ 融合执行成功")
            st.code(result, language=None)
        else:
            st.warning("⚠️ 模拟 LLM 未匹配到预设，返回默认示例")

        st.info("""
        **演示说明**：当前为 Mock 模式，根据关键词返回预设代码。
        接入真实 LLM（如 OpenAI API）即可实现完整符号神经融合。
        """)

    st.divider()
    st.markdown("""
    **融合价值**：
    - 神经：擅长理解、生成，弱于精确逻辑
    - 符号：擅长精确执行、可验证
    - 融合：各取所长，代码即编排
    """)

st.sidebar.divider()
st.sidebar.markdown("[GitHub](https://github.com/wenduntang/push-u) · push-u")
