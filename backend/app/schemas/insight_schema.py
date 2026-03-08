from pydantic import BaseModel
from typing import List
from datetime import date


class InsightCard(BaseModel):

    product: str
    type: str
    severity: str
    priority_score: int
    metric_value: float
    metric_unit: str
    stage: str
    impact: str
    message: str
    cta_label: str


class InsightResponse(BaseModel):

    date: date
    critical_count: int
    insights: List[InsightCard]