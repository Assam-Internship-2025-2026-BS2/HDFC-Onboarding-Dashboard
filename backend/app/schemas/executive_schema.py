from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class Alert(BaseModel):
    text: str
    severity: str

class OverallHealth(BaseModel):
    status: str
    critical_products: int
    message: str
    alerts: List[Alert]

class OnboardingStarted(BaseModel):
    value: int
    trend_percentage: float
    trend_direction: str
    submitted: int
    in_progress: int


class OnboardingCompleted(BaseModel):
    value: int
    trend_percentage: float
    trend_direction: str
    conversion_rate: float
    approval_rate: float


class AvgCompletionTime(BaseModel):
    value_minutes: float
    trend_minutes: float
    trend_direction: str
    sla_target_minutes: float
    max_product_time_minutes: float
    max_product_name: str


class PipelineAtRisk(BaseModel):
    amount_cr: float
    trend_cr: float
    trend_direction: str
    percentage_of_total_pipeline: float
    sla_breached: int
    stuck_over_24h: int


class KPICards(BaseModel):
    onboarding_started: OnboardingStarted
    onboarding_completed: OnboardingCompleted
    avg_completion_time: AvgCompletionTime
    pipeline_at_risk: PipelineAtRisk


class FiltersApplied(BaseModel):
    time_range: str
    comparison: Optional[str]
    channel: str
    region: str
    segment: str


class ExecutiveResponse(BaseModel):
    overall_health: OverallHealth
    kpi_cards: KPICards
    filters_applied: FiltersApplied
    channel_distribution: List[Dict]
    trend_data: List[Dict]
    data_as_of_timestamp: datetime