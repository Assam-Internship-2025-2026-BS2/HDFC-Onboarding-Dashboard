from fastapi import APIRouter, Query
from app.schemas.products_schema import ProductsResponse
from app.services.products_service import ProductsService

router = APIRouter()

@router.get("/", response_model=ProductsResponse)
def get_products_dashboard(
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
    return ProductsService.get_products_data(filters)
