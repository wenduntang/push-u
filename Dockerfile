# Hugging Face Spaces - Streamlit Demo
# HF 已弃用 Streamlit SDK，需用 Docker 运行
FROM python:3.10-slim

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

RUN pip install --no-cache-dir streamlit RestrictedPython pydantic

COPY --chown=user app.py code_executor.py requirements.txt ./
COPY --chown=user sandbox_core ./sandbox_core

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
