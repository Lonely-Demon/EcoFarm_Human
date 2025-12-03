from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class RecommendationRequest(BaseModel):
    farm_id: Optional[UUID] = None
    sector_id: Optional[UUID] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    budget: Optional[float] = None
    preferred_crops: Optional[List[str]] = []
    time_horizon_months: Optional[int] = 6

class CropRecommendation(BaseModel):
    crop: str
    score: float
    rationale: str

class RecommendationResponse(BaseModel):
    recommendations: List[CropRecommendation]
