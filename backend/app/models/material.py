from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional

class Material(SQLModel, table=True):
    __tablename__ = "materials"
    id: Optional[int] = Field(default=None, primary_key=True)
    seller_id: int = Field(foreign_key="users.id")
    material_type: str = Field(index=True)
    quantity: float
    unit: str = Field(default="units")
    age: Optional[str] = None
    dimensions: Optional[str] = None
    previous_use: Optional[str] = None
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    condition: Optional[str] = None
    reuse_score: Optional[float] = None
    risk_level: Optional[str] = None
    ai_confidence: Optional[float] = None
    estimated_value: Optional[float] = None
    carbon_estimate: Optional[float] = None
    status: str = Field(default="draft")
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MaterialImage(SQLModel, table=True):
    __tablename__ = "material_images"
    id: Optional[int] = Field(default=None, primary_key=True)
    material_id: int = Field(foreign_key="materials.id")
    image_url: str
    image_type: str = Field(default="photo")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MaterialAssessment(SQLModel, table=True):
    __tablename__ = "material_assessments"
    id: Optional[int] = Field(default=None, primary_key=True)
    material_id: int = Field(foreign_key="materials.id")
    detections: str
    visible_defects: str
    condition: str
    reuse_score: float
    risk_level: str
    confidence: float
    recommendation: str
    reasoning: str
    assessment_type: str = Field(default="ai")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MaterialPassport(SQLModel, table=True):
    __tablename__ = "material_passports"
    id: Optional[int] = Field(default=None, primary_key=True)
    material_id: int = Field(foreign_key="materials.id", unique=True)
    passport_id: str = Field(unique=True)
    source_building: Optional[str] = None
    previous_use: Optional[str] = None
    material_grade: Optional[str] = None
    ai_condition: str
    ai_reuse_score: float
    carbon_estimate: Optional[float] = None
    verification_status: str = Field(default="not_required")
    inspection_notes: Optional[str] = None
    lifecycle_stage: str = Field(default="assessed")
    created_at: datetime = Field(default_factory=datetime.utcnow)
