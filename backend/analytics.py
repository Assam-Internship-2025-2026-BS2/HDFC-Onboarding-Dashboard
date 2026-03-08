from database import get_client
from queries import *

def get_dashboard_metrics():

    client = get_client()

    started = client.query(onboarding_started_query()).result_rows[0][0]

    completed = client.query(onboarding_completed_query()).result_rows[0][0]

    dropoffs = client.query(dropoff_query()).result_rows[0][0]

    avg_time = client.query(avg_time_query()).result_rows[0][0]

    return {
        "onboarding_started": started,
        "onboarding_completed": completed,
        "dropoffs": dropoffs,
        "avg_completion_time": round(avg_time,2)
    }