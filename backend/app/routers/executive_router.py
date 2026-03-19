from fastapi import APIRouter, Query
from enum import Enum
from typing import Optional

from app.services.executive_service import fetch_executive_dashboard
from app.schemas.executive_schema import ExecutiveResponse


router = APIRouter(
    prefix="/executive",
    tags=["Executive Dashboard"]
)


class TimeRange(str, Enum):

    THIS_MONTH = "This Month"
    TODAY = "Today"
    YESTERDAY = "Yesterday"
    LAST_7_DAYS = "Last 7 Days"
    LAST_30_DAYS = "Last 30 Days"


class Comparison(str, Enum):

    VS_LAST_MONTH = "V/S Last Month"
    VS_LAST_WEEK = "V/S Last Week"
    VS_PREVIOUS_PERIOD = "V/S Previous Period"
    VS_YESTERDAY = "V/S Yesterday"


@router.get(
    "/dashboard",
    response_model=ExecutiveResponse
)
def get_executive_dashboard(

    time_range: TimeRange = Query(TimeRange.THIS_MONTH),
    comparison: Optional[Comparison] = Query(None),

    channel: str = Query("All Channels"),
    region: str = Query("All Regions"),
    segment: str = Query("All Segments")
):

    return fetch_executive_dashboard(        time_range.value,
        comparison.value if comparison else None,
        channel,
        region,
        segment
    )