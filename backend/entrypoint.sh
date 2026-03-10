#!/bin/sh

echo "Waiting for ClickHouse to be ready..."
until python -c "import urllib.request; urllib.request.urlopen('http://$CLICKHOUSE_HOST:$CLICKHOUSE_PORT/ping')" 2>/dev/null; do
  echo "ClickHouse not ready yet, retrying in 5s..."
  sleep 5
done

echo "ClickHouse is ready."

echo "Checking if data already loaded..."
ROW_COUNT=$(python -c "
import clickhouse_connect
client = clickhouse_connect.get_client(host='$CLICKHOUSE_HOST', port=$CLICKHOUSE_PORT, username='$CLICKHOUSE_USER', password='$CLICKHOUSE_PASSWORD')
try:
    result = client.command('SELECT count() FROM business_ops.dashboard_data')
    print(result)
except:
    print(0)
")

if [ "$ROW_COUNT" -gt "0" ]; then
  echo "Data already loaded ($ROW_COUNT rows), skipping init scripts."
else
  echo "No data found, running init scripts..."
  python scripts/load_data.py
  python setup_mv.py
fi

echo "Starting FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000