import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from app.core.database import get_clickhouse_client
from app.queries.products_queries import create_products_mv_query, create_products_aggregated_table_query, backfill_products_mv_query
from app.queries.insights_queries import create_insights_mv_query, create_insights_aggregated_table_query, backfill_insights_mv_query
from app.queries.analysis_queries import create_analysis_mv_query, create_analysis_aggregated_table_query, backfill_analysis_mv_query


client = get_clickhouse_client()

print("Creating Aggregated Table...")
client.command("""
CREATE TABLE IF NOT EXISTS dashboard_aggregated (
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
CREATE MATERIALIZED VIEW IF NOT EXISTS dashboard_mv 
TO dashboard_aggregated
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
client.command("TRUNCATE TABLE IF EXISTS dashboard_aggregated")

result = client.command("EXISTS TABLE dashboard_data")
if not result:
    print("❌ dashboard_data table not found. Run load_data.py first!")
    sys.exit(1)

print("Backfilling Data...")
client.command("""
INSERT INTO dashboard_aggregated
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

# Setup New Materialized Views
print("Creating Products Aggregated Table and MV...")
client.command(create_products_aggregated_table_query())
client.command(create_products_mv_query())
client.command("TRUNCATE TABLE IF EXISTS products_aggregated")
client.command(backfill_products_mv_query())

print("Creating Insights Aggregated Table and MV...")
client.command(create_insights_aggregated_table_query())
client.command(create_insights_mv_query())
client.command("TRUNCATE TABLE IF EXISTS insights_aggregated")
client.command(backfill_insights_mv_query())

print("Creating Analysis Aggregated Table and MV...")
client.command(create_analysis_aggregated_table_query())
client.command(create_analysis_mv_query())
client.command("TRUNCATE TABLE IF EXISTS analysis_aggregated")
client.command(backfill_analysis_mv_query())

print("Successfully created all new Materialized Views!")
