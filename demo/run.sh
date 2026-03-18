#!/bin/bash
# 从项目根目录运行 Demo
cd "$(dirname "$0")/.."
streamlit run demo/app.py --server.port 8501
