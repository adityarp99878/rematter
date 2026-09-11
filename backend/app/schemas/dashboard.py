from pydantic import BaseModel
from typing import List

class DashboardStats(BaseModel):
    materials_listed: int
    active_requirements: int
    successful_matches: int
    materials_reused: int
    co2_avoided: float
    value_recovered: float
    recent_materials: List[dict] = []
    recent_matches: List[dict] = []
    ai_recommendations: List[dict] = []
