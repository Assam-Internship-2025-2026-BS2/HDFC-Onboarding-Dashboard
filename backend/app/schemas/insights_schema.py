from pydantic import BaseModel
from typing import List

class DemographicData(BaseModel):
    age_18_25: str
    age_26_35: str
    age_36_50: str
    age_50_plus: str

class ChannelDistribution(BaseModel):
    mobile_app: str
    website: str
    branch: str

class InsightsResponse(BaseModel):
    reachable_base: str
    reachable_base_trend: str
    engagement_score: str
    engagement_score_trend: str
    overall_nps: str
    overall_nps_trend: str
    demographics: DemographicData
    channel_preference: ChannelDistribution
