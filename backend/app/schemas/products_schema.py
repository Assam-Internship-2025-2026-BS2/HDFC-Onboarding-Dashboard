from pydantic import BaseModel
from typing import List, Optional

class ProductKPIs(BaseModel):
    total_active: str
    total_active_trend: str
    total_disbursed: str
    total_disbursed_trend: str
    total_conversions: str
    total_conversions_trend: str
    sla_breaches: str
    sla_breaches_trend: str

class ProductMatrixRow(BaseModel):
    product_line: str
    applications_started: str
    approved: str
    conversion_rate: str
    avg_processing_time: str
    status: str

class ProductsResponse(BaseModel):
    kpis: ProductKPIs
    matrix_rows: List[ProductMatrixRow]
