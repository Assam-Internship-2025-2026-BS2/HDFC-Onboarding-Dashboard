from app.core.database import get_clickhouse_client
from app.utils.calculations import calculate_dropoff


def get_stage_dropoff(filters):

    client = get_clickhouse_client()

    conditions = []
    params = {}

    # --------------------------------
    # FILTERS
    # --------------------------------

    if filters.get("from_date"):
        conditions.append("date >= {from_date:Date}")
        params["from_date"] = filters["from_date"]

    if filters.get("to_date"):
        conditions.append("date <= {to_date:Date}")
        params["to_date"] = filters["to_date"]

    if filters.get("channel") and filters["channel"] != "All Channels":
        conditions.append("channel = {channel:String}")
        params["channel"] = filters["channel"]

    if filters.get("region") and filters["region"] != "All Regions":
        conditions.append("region = {region:String}")
        params["region"] = filters["region"]

    if filters.get("segment") and filters["segment"] != "All Segments":
        conditions.append("segment = {segment:String}")
        params["segment"] = filters["segment"]

    where_clause = ""

    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    # --------------------------------
    # QUERY
    # --------------------------------

    query = f"""
    SELECT
        product_name,
        SUM(started) AS started,
        SUM(submitted) AS submitted,
        SUM(in_progress) AS in_progress,
        SUM(completed) AS completed,
        SUM(approved) AS approved
    FROM dashboard_data
    {where_clause}
    GROUP BY product_name
    """

    result = client.query(query, parameters=params)

    rows = result.result_rows

    response = []

    # --------------------------------
    # STAGE DROPOFF CALCULATION
    # --------------------------------

    for row in rows:

        product = row[0]

        started = row[1] or 0
        submitted = row[2] or 0
        progress = row[3] or 0
        completed = row[4] or 0
        approved = row[5] or 0

        response.append({
            "product": product,

            "OTP Verify": calculate_dropoff(started, submitted),

            "CKYC/KYC": calculate_dropoff(submitted, progress),

            "Doc Upload": calculate_dropoff(progress, completed),

            "Eligibility": calculate_dropoff(completed, approved)
        })

    return response