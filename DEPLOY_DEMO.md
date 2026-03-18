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

1. 登录 [huggingface.co](https://huggingface.co)，进入 [Spaces](https://huggingface.co/spaces)
2. 点击 **Create new Space**
3. 选择 **Streamlit** 作为 SDK
4. 选择 **Connect to Hub repository**，关联 `wenduntang/push-u`（或 Fork 后关联）
5. 或手动上传：将 `app.py`、`code_executor.py`、`requirements.txt` 放入 Space
6. 创建后自动构建，约 1–2 分钟可访问

Space 将提供公开 URL，如：`https://huggingface.co/spaces/你的用户名/push-u-demo`

## 一键部署（Hugging Face）

若已 Fork 本仓库，可在 Space 创建时选择 **Duplicate this Space** 或直接关联 GitHub 仓库。
