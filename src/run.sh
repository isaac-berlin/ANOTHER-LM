#!/bin/bash

echo "Starting FastAPI backend..."
uvicorn api:app --host 0.0.0.0 --port 8000 &

echo "Starting Streamlit frontend..."
streamlit run Chat.py --server.port=8501 --server.address=0.0.0.0
