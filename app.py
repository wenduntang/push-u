"""
极简自主编排引擎 - 在线 Demo（Hugging Face Spaces 入口）
"""
import streamlit as st
from code_executor import safe_run, TOOLS

st.set_page_config(page_title="代码即编排 Demo", page_icon="⚡", layout="centered")

st.title("⚡ 极简自主编排引擎")
st.caption("代码即编排 · 无 JSON · 无 DAG · 约 50 行核心")

st.markdown("""
**核心理念**：模型输出 Python 代码，引擎安全执行。逻辑在代码里，不在 Prompt 里。

👇 选择示例或输入自定义代码，点击运行查看效果。
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
    "❌ 非法 import（演示拦截）": """```python
import os
print(os.getcwd())
```""",
    "❌ 未定义变量（演示 Fail-fast）": """```python
print(undefined_var)
```""",
}

example = st.selectbox("选择示例", list(EXAMPLES.keys()))
code_input = st.text_area("代码（需包含 ```python ... ```）", value=EXAMPLES[example], height=120)

if st.button("▶ 运行", type="primary"):
    with st.spinner("执行中..."):
        ok, result = safe_run(code_input, timeout=5)

    if ok:
        st.success("✅ 执行成功")
        st.code(result, language=None)
    else:
        st.error("❌ 执行失败")
        st.code(result, language=None)
        st.info("💡 报错会原样回传 LLM，触发自主 Debug（Fail-fast）")

st.divider()
st.markdown("### 可用工具")
for name, func in TOOLS.items():
    st.markdown(f"- **{name}**: `{func.__doc__ or ''}`")

st.divider()
st.markdown("""
**🔗 了解更多**
- [GitHub](https://github.com/wenduntang/push-u) · 轻量化极简化编排 Agent
""")
