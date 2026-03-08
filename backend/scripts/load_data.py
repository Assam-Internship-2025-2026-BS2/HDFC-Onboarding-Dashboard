import sys
from pathlib import Path

# Add the backend directory to sys.path so the 'app' module can be imported
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

import pandas as pd  # noqa: E402
from app.core.database import get_clickhouse_client  # noqa: E402


def load_csv_to_clickhouse():

    client = get_clickhouse_client()

    BASE_DIR = Path(__file__).resolve().parent.parent
    csv_path = BASE_DIR / "data" / "dashboard_large_dataset.csv"

    df = pd.read_csv(csv_path)

    df["date"] = pd.to_datetime(df["date"]).dt.date

    print(f"Loaded {len(df)} rows from CSV")

    create_table_query = """
    CREATE TABLE IF NOT EXISTS dashboard_data (

        date Date,
        product_name String,
        channel String,
        region String,
        segment String,

        started UInt32,
        submitted UInt32,
        in_progress UInt32,
        completed UInt32,
        approved UInt32,
        failures UInt32,

        avg_time_minutes Float32,
        sla_target_minutes Float32,

        pipeline_total_cr Float32,
        pipeline_risk_cr Float32,

        sla_breached UInt32,
        stuck_24h UInt32

    )
    ENGINE = MergeTree()
    ORDER BY (date, product_name)
    """

    client.command(create_table_query)

    print("Table verified/created")

    client.insert_df("dashboard_data", df)

    print("Data inserted into ClickHouse successfully")


if __name__ == "__main__":
    load_csv_to_clickhouse()