#!/bin/bash
# 1-Click Runner for Streamlit Web Dashboard
# Works from either workspace root or student-performance-analytics directory

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

if [ -d "$DIR/student-performance-analytics" ]; then
    cd "$DIR/student-performance-analytics"
elif [ -d "$DIR" ]; then
    cd "$DIR"
fi

if [ -f ".venv/bin/streamlit" ]; then
    echo "Starting Student Performance Analytics Dashboard..."
    echo "Opening URL: http://localhost:8501"
    .venv/bin/streamlit run app.py
else
    echo "[ERROR] Virtual environment not found. Please run:"
    echo "  python3 -m venv .venv"
    echo "  .venv/bin/pip install -r requirements.txt"
fi
