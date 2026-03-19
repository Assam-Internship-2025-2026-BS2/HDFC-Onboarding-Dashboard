def create_products_mv_query():
    return """
    CREATE MATERIALIZED VIEW IF NOT EXISTS products_mv
    TO products_aggregated
    AS SELECT
        date,
        product_name,
        toUInt64(sum(started)) AS total_started,
        toUInt64(sum(approved)) AS total_approved,
        toUInt64(sum(failures)) AS total_failures,
        toUInt64(sum(sla_breached)) AS total_sla_breached,
        avg(avg_time_minutes) AS avg_time_minutes,
        sum(pipeline_total_cr) AS pipeline_total_cr
    FROM dashboard_data
    GROUP BY date, product_name
    """

def create_products_aggregated_table_query():
    return """
    CREATE TABLE IF NOT EXISTS products_aggregated (
        date Date,
        product_name String,
        total_started UInt64,
        total_approved UInt64,
        total_failures UInt64,
        total_sla_breached UInt64,
        avg_time_minutes Float32,
        pipeline_total_cr Float32
    )
    ENGINE = SummingMergeTree()
    ORDER BY (date, product_name)
    """

def backfill_products_mv_query():
    return """
    INSERT INTO products_aggregated
    SELECT
        date,
        product_name,
        toUInt64(sum(started)) AS total_started,
        toUInt64(sum(approved)) AS total_approved,
        toUInt64(sum(failures)) AS total_failures,
        toUInt64(sum(sla_breached)) AS total_sla_breached,
        avg(avg_time_minutes) AS avg_time_minutes,
        sum(pipeline_total_cr) AS pipeline_total_cr
    FROM dashboard_data
    GROUP BY date, product_name
    """
