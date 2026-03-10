#!/bin/sh

echo "Waiting for ClickHouse to be ready..."
until python -c "import urllib.request; urllib.request.urlopen('http://$CLICKHOUSE_HOST:$CLICKHOUSE_PORT/ping')" 2>/dev/null; do
  echo "ClickHouse not ready yet, retrying in 5s..."
  sleep 5
done

echo "ClickHouse is ready."

echo "Running load_data.py..."
python scripts/load_data.py

echo "Running setup_mv.py..."
python setup_mv.py

echo "Starting FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000