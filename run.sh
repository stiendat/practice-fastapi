#!/bin/bash

# Chạy lệnh khởi tạo database thông qua Typer CLI
echo "Running database initialization..."
/usr/bin/env python3 -c '
import sys
sys.path.append(".")
from cli import app
if __name__ == "__main__":
    app(["init_database"])
'

# Chạy ứng dụng FastAPI
echo "Starting FastAPI application..."
uvicorn src.api.main_router:router --host 0.0.0.0 --port 8000 --reload
