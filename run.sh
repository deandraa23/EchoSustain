#!/bin/bash

echo "Cleaning up existing processes on 8001 and 8501..."
lsof -ti tcp:8001 | xargs -r kill -9 2>/dev/null
lsof -ti tcp:8501 | xargs -r kill -9 2>/dev/null

source venv/bin/activate

cleanup() {
    echo ""
    echo "Stopping EchoSustain services..."
    kill $UVICORN_PID $STREAMLIT_PID 2>/dev/null
    exit 0
}
trap cleanup SIGINT SIGTERM

echo "Starting Uvicorn Backend on port 8001..."
python -m uvicorn backend.main:app --port 8001 &
UVICORN_PID=$!

sleep 2

echo "Starting Streamlit Frontend on port 8501..."
python -m streamlit run frontend/app.py &
STREAMLIT_PID=$!

wait
