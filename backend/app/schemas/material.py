from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class MaterialCreate(BaseModel):
    material_type: str
    quantity: float
    unit: str = "units"
    location: str
    age: Optional[str] = None
    dimensions: Optional[str] = None
    previous_use: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class MaterialResponse(BaseModel):
    id: int
    seller_id: int
    material_type: str
    quantity: float
    unit: str
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    condition: Optional[str] = None
    reuse_score: Optional[float] = None
    risk_level: Optional[str] = None
    ai_confidence: Optional[float] = None
    estimated_value: Optional[float] = None
    carbon_estimate: Optional[float] = None
    status: str
    description: Optional[str] = None
    age: Optional[str] = None
    dimensions: Optional[str] = None
    previous_use: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AgentActivityStep(BaseModel):
    agent: str
    status: str
    message: str
    timestamp: str
    duration_ms: int = 0


class VisionDetection(BaseModel):
    material: str
    confidence: float
    count_estimate: int
    bbox: Optional[List[float]] = None


class AssessmentResult(BaseModel):
    condition: str
    visible_defects: List[str] = []
    reuse_score: float
    risk_level: str
    confidence: float
    recommendation: str
    verification_required: bool = False
    reasoning: List[str] = []
    safety_disclaimer: str = ""


class PassportResponse(BaseModel):
    id: Optional[int] = None
    material_id: Optional[int] = None
    passport_id: str
    source_building: Optional[str] = None
    previous_use: Optional[str] = None
    material_grade: Optional[str] = None
    ai_condition: str = ""
    ai_reuse_score: float = 0
    carbon_estimate: Optional[float] = None
    verification_status: str = "not_required"
    inspection_notes: Optional[str] = None
    lifecycle_stage: str = "assessed"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MaterialAnalyzeResponse(BaseModel):
    material_id: int
    material: dict
    assessment: dict
    passport: dict
    pricing: dict = {}
    impact: dict = {}
    second_life: List[dict] = []
    agent_activity: List[dict] = []
