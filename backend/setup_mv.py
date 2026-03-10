import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from app.core.database import get_clickhouse_client

client = get_clickhouse_client()

print("Creating Aggregated Table...")
client.command("""
CREATE TABLE IF NOT EXISTS dashboard_daily_aggregated (
    date Date,
    product_name String,
    channel String,
    region String,
    segment String,
    total_started UInt64,
    total_completed UInt64,
    total_failures UInt64,
    record_count UInt64
)
ENGINE = SummingMergeTree()
ORDER BY (date, product_name, channel, region, segment)
""")

print("Creating Materialized View.")
client.command("""
CREATE MATERIALIZED VIEW IF NOT EXISTS dashboard_daily_mv 
TO dashboard_daily_aggregated
AS SELECT
    date,
    product_name,
    channel,
    region,
    segment,
    toUInt64(sum(started)) AS total_started,
    toUInt64(sum(completed)) AS total_completed,
    toUInt64(sum(failures)) AS total_failures,
    toUInt64(count()) AS record_count
FROM dashboard_data
GROUP BY date, product_name, channel, region, segment
""")

print("Truncating target table to avoid duplicates during backfill.")
client.command("TRUNCATE TABLE IF EXISTS dashboard_daily_aggregated")

result = client.command("EXISTS TABLE dashboard_data")
if not result:
    print("❌ dashboard_data table not found. Run load_data.py first!")
    sys.exit(1)

print("Backfilling Data...")
client.command("""
INSERT INTO dashboard_daily_aggregated
SELECT
    date,
    product_name,
    channel,
    region,
    segment,
    toUInt64(sum(started)) AS total_started,
    toUInt64(sum(completed)) AS total_completed,
    toUInt64(sum(failures)) AS total_failures,
    toUInt64(count()) AS record_count
FROM dashboard_data
GROUP BY date, product_name, channel, region, segment
""")

print("Successfully created and backfilled Materialized View!")
