from fastapi import APIRouter, Query
from app.schemas.insights_schema import InsightsResponse
from app.services.insights_service import InsightsService

router = APIRouter()

@router.get("/", response_model=InsightsResponse)
def get_insights_dashboard(
    time_range: str | None = Query("This Month", description="Time Range filter"),
    channel: str | None = Query(None, description="Channel filter"),
    region: str | None = Query(None, description="Region filter"),
    segment: str | None = Query(None, description="Segment filter")
):
    filters = {
        "time_range": time_range,
        "channel": channel,
        "region": region,
        "segment": segment
    }
    return InsightsService.get_insights_data(filters)
