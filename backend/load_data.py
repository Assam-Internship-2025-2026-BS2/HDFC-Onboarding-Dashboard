import pandas as pd
from database import get_client

client = get_client()

client.command("""
CREATE TABLE IF NOT EXISTS onboarding (
    journey_id Int32,
    product String,
    stage String,
    status String,
    processing_time Int32,
    date DateTime
)
ENGINE = MergeTree()
ORDER BY journey_id
""")

df = pd.read_csv("../data/onboarding_data.csv")

# IMPORTANT FIX
df["date"] = pd.to_datetime(df["date"])

client.insert_df("onboarding", df)

print("Data inserted into ClickHouse successfully")