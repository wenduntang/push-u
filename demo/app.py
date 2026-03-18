"""
Demo 入口（从 demo/ 目录运行：streamlit run demo/app.py）
需在项目根目录执行：cd .. && streamlit run demo/app.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import importlib.util
spec = importlib.util.spec_from_file_location("app", Path(__file__).parent.parent / "app.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)
