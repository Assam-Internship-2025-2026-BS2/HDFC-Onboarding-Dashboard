from pydantic import BaseModel
from typing import List

class FunnelStep(BaseModel):
    name: str
    count: int

class TrendPoint(BaseModel):
    month: str
    Conversion: int
    Dropoff: int

class ChannelPoint(BaseModel):
    name: str
    value: int

class AnalysisResponse(BaseModel):
    funnel: List[FunnelStep]
    trend: List[TrendPoint]
    channels: List[ChannelPoint]
