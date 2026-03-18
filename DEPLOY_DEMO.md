# Demo 部署指南

## 本地运行

```bash
pip install streamlit RestrictedPython
streamlit run app.py
```

浏览器打开 http://localhost:8501，侧边栏可切换：
- 🛡️ 沙箱运行环境
- ⚡ 极简编排引擎
- 🧠 符号神经融合AI

## 部署到 Hugging Face Spaces

> **说明**：HF 已弃用 Streamlit SDK，需选择 **Docker** 运行。

### 步骤（与当前 HF 界面一致）

1. 登录 [huggingface.co](https://huggingface.co)，点击 **Spaces** → **Create new Space**
2. **Owner**：选你的用户名
3. **Space name**：`push-u-demo`
4. **Select the Space SDK**：选择 **Docker**（不要选 Static 或 Gradio）
5. **Choose a Docker template**：选 **Blank** 或 **Python**
6. 创建后，将本仓库文件推送到该 Space：
   - 必须包含：`Dockerfile`、`app.py`、`code_executor.py`、`sandbox_core/`
   - 或选择 **Clone from a repo** 关联 `wenduntang/push-u`
7. 将仓库根目录的 `README_HF.md` 内容复制到 Space 的 `README.md`（含 YAML 头 `sdk: docker`、`app_port: 8501`）
8. 等待构建（约 2–5 分钟）

Space URL：`https://huggingface.co/spaces/你的用户名/push-u-demo`
