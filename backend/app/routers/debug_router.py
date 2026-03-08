from fastapi import APIRouter
from app.core.database import get_clickhouse_client


router = APIRouter(
    prefix="/debug",
    tags=["Debug"]
)


@router.get("/db-health")
def check_database():

    client = get_clickhouse_client()

    count_query = """
    SELECT count()
    FROM dashboard_data
    """

    date_query = """
    SELECT
        min(date),
        max(date)
    FROM dashboard_data
    """

    total_rows = client.query(count_query).result_rows[0][0]

    min_date, max_date = client.query(date_query).result_rows[0]

    return {
        "database": "connected",
        "table": "dashboard_data",
        "total_rows": total_rows,
        "min_date": min_date,
        "max_date": max_date
    }