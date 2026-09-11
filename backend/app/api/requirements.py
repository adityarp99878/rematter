from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.requirement import Requirement
from app.schemas.requirement import RequirementCreate, RequirementResponse
from typing import List, Optional

router = APIRouter(prefix="/api/requirements", tags=["requirements"])

@router.post("/", response_model=RequirementResponse)
def create_requirement(req: RequirementCreate, db: Session = Depends(get_db)):
    r = Requirement(**req.dict())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r

@router.get("/", response_model=List[RequirementResponse])
def get_requirements(buyer_id: Optional[int] = None, status: Optional[str] = None, material_type: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Requirement)
    if buyer_id:
        query = query.filter(Requirement.buyer_id == buyer_id)
    if status:
        query = query.filter(Requirement.status == status)
    if material_type:
        query = query.filter(Requirement.material_type == material_type)
    return query.all()

@router.get("/{id}", response_model=RequirementResponse)
def get_requirement(id: int, db: Session = Depends(get_db)):
    r = db.query(Requirement).filter(Requirement.id == id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return r
