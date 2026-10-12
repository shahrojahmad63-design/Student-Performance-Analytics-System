#!/bin/bash
# 1-Click Runner for CLI Analysis

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

if [ -d "$DIR/student-performance-analytics" ]; then
    cd "$DIR/student-performance-analytics"
elif [ -d "$DIR" ]; then
    cd "$DIR"
fi

if [ -f ".venv/bin/python" ]; then
    .venv/bin/python main.py "$@"
else
    python3 main.py "$@"
fi
