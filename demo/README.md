# 极简自主编排引擎 - 在线 Demo

展示「代码即编排」：模型输出 Python 代码，引擎安全执行。

## 本地运行

```bash
cd demo
pip install streamlit RestrictedPython
streamlit run app.py
```

或从项目根目录：

```bash
pip install streamlit RestrictedPython
streamlit run demo/app.py
```

## 部署到 Hugging Face Spaces

1. 在 [Hugging Face](https://huggingface.co/spaces) 创建新 Space
2. 选择 **Streamlit** 模板
3. 上传 `app.py` 和 `requirements.txt`
4. 将 `code_executor.py` 放入仓库根目录（或调整 `sys.path`）

## 示例

- 北京天气、多城市对比
- 四则运算、组合任务
- 非法 import、未定义变量（演示安全拦截与 Fail-fast）
