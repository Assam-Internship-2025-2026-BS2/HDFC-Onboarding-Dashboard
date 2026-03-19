import pandas as pd
from datetime import datetime, timedelta
import random
from pathlib import Path


def generate_dashboard_data(num_records=100000):
    print(f"Generating {num_records} records...")
    products = ['Credit Card', 'Personal Loan', 'Savings Acc', 'Home Loan', 'Auto Loan']
    channels = ['Mobile App', 'NetBanking', 'Branch Assisted']
    regions = ['North Zone', 'South Zone', 'East Zone', 'West Zone']
    segments = ['Retail', 'Priority', 'NR', 'SME']

    # Generate dates over the last 60 days
    end_date = datetime.now().date() - timedelta(days=1)
    start_date = end_date - timedelta(days=60)
    dates = [
        start_date + timedelta(days=x)
        for x in range((end_date - start_date).days + 1)
    ]

    data = []

    # Generate daily aggregates per segment/region/channel/product
    for _ in range(num_records):
        prod = random.choice(products)
        chan = random.choice(channels)
        reg = random.choice(regions)
        seg = random.choice(segments)
        dt = random.choice(dates)
        # Base numbers
        started = random.randint(100, 1000)

        # Dropoffs at various stages
        submitted = int(started * random.uniform(0.7, 0.95))
        in_progress = int(submitted * random.uniform(0.2, 0.5))
        completed = submitted - in_progress
        approved = int(completed * random.uniform(0.6, 0.9))
        failures = int(started * random.uniform(0.01, 0.1))

        avg_time = random.uniform(5.0, 45.0)
        sla_target = 15.0 if prod in ['Credit Card', 'Savings Acc'] else 45.0

        pipeline_total = round(random.uniform(1.0, 50.0), 2)
        pipeline_risk = round(pipeline_total * random.uniform(0.1, 0.4), 2)

        sla_breached = int(started * random.uniform(0.05, 0.2))
        stuck_24h = int(started * random.uniform(0.01, 0.1))

        row = {
            "date": dt,
            "product_name": prod,
            "channel": chan,
            "region": reg,
            "segment": seg,
            "started": started,
            "submitted": submitted,
            "in_progress": in_progress,
            "completed": completed,
            "approved": approved,
            "failures": failures,
            "avg_time_minutes": avg_time,
            "sla_target_minutes": sla_target,
            "pipeline_total_cr": pipeline_total,
            "pipeline_risk_cr": pipeline_risk,
            "sla_breached": sla_breached,
            "stuck_24h": stuck_24h
        }
        data.append(row)

    df = pd.DataFrame(data)

    BASE_DIR = Path(__file__).resolve().parent.parent
    data_dir = BASE_DIR / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    output_path = data_dir / "dashboard_large_dataset.csv"
    df.to_csv(output_path, index=False)
    print(f"Successfully generated {num_records} records at {output_path}")


if __name__ == "__main__":
    generate_dashboard_data(200000)
