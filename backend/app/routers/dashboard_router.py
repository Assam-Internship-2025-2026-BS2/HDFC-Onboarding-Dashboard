from fastapi import APIRouter, Query
from typing import List, Dict

from app.services.stage_dropoff_service import get_stage_dropoff

router = APIRouter(tags=["Dashboard"])


from app.services.executive_service import get_date_range

@router.get("/dashboard/stage-dropoff", response_model=List[Dict])
def stage_dropoff(
    time_range: str | None = Query("This Month"),
    channel: str | None = Query(None),
    region: str | None = Query(None),
    segment: str | None = Query(None)
):

    from_date, to_date = get_date_range(time_range)

    filters = {
        "from_date": from_date,
        "to_date": to_date,
        "channel": channel,
        "region": region,
        "segment": segment
    }

    data = get_stage_dropoff(filters)

    return data