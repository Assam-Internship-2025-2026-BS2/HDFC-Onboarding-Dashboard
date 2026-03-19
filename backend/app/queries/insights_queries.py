def create_insights_mv_query():
    return """
    CREATE MATERIALIZED VIEW IF NOT EXISTS insights_mv
    TO insights_aggregated
    AS SELECT
        date,
        channel,
        toUInt64(count()) AS reachable_base_count
    FROM dashboard_data
    GROUP BY date, channel
    """

def create_insights_aggregated_table_query():
    return """
    CREATE TABLE IF NOT EXISTS insights_aggregated (
        date Date,
        channel String,
        reachable_base_count UInt64
    )
    ENGINE = SummingMergeTree()
    ORDER BY (date, channel)
    """

def backfill_insights_mv_query():
    return """
    INSERT INTO insights_aggregated
    SELECT
        date,
        channel,
        toUInt64(count()) AS reachable_base_count
    FROM dashboard_data
    GROUP BY date, channel
    """
