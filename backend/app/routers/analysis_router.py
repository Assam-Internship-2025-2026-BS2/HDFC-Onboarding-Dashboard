from fastapi import APIRouter, Query
from app.schemas.analysis_schema import AnalysisResponse
from app.services.analysis_service import AnalysisService

router = APIRouter()

@router.get("/", response_model=AnalysisResponse)
def get_analysis_dashboard(
    product: str = Query("Credit Card", description="Product Line filter"),
    time_range: str | None = Query("This Month", description="Time Range filter"),
    channel: str | None = Query(None, description="Channel filter"),
    region: str | None = Query(None, description="Region filter"),
    segment: str | None = Query(None, description="Segment filter")
):
    filters = {
        "product": product,
        "time_range": time_range,
        "channel": channel,
        "region": region,
        "segment": segment
    }
    return AnalysisService.get_analysis_data(filters)
