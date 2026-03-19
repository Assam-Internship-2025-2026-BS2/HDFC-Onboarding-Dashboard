def create_analysis_mv_query():
    return """
    CREATE MATERIALIZED VIEW IF NOT EXISTS analysis_mv
    TO analysis_aggregated
    AS SELECT
        date,
        product_name,
        channel,
        toUInt64(sum(started)) AS total_started,
        toUInt64(sum(submitted)) AS total_submitted,
        toUInt64(sum(in_progress)) AS total_in_progress,
        toUInt64(sum(completed)) AS total_completed,
        toUInt64(sum(approved)) AS total_approved
    FROM dashboard_data
    GROUP BY date, product_name, channel
    """

def create_analysis_aggregated_table_query():
    return """
    CREATE TABLE IF NOT EXISTS analysis_aggregated (
        date Date,
        product_name String,
        channel String,
        total_started UInt64,
        total_submitted UInt64,
        total_in_progress UInt64,
        total_completed UInt64,
        total_approved UInt64
    )
    ENGINE = SummingMergeTree()
    ORDER BY (date, product_name, channel)
    """

def backfill_analysis_mv_query():
    return """
    INSERT INTO analysis_aggregated
    SELECT
        date,
        product_name,
        channel,
        toUInt64(sum(started)) AS total_started,
        toUInt64(sum(submitted)) AS total_submitted,
        toUInt64(sum(in_progress)) AS total_in_progress,
        toUInt64(sum(completed)) AS total_completed,
        toUInt64(sum(approved)) AS total_approved
    FROM dashboard_data
    GROUP BY date, product_name, channel
    """
