from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.verification import VerificationRequest
from pydantic import BaseModel

router = APIRouter(prefix="/api/verification", tags=["verification"])

class VerificationCreate(BaseModel):
    material_id: int
    reason: str
    notes: str = None
    requested_by: int = None

@router.post("/request")
def request_verification(req: VerificationCreate, db: Session = Depends(get_db)):
    v = VerificationRequest(**req.dict())
    db.add(v)
    db.commit()
    db.refresh(v)
    return v

@router.get("/{material_id}")
def get_verification_status(material_id: int, db: Session = Depends(get_db)):
    v = db.query(VerificationRequest).filter(VerificationRequest.material_id == material_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Verification not found")
    return {"status": v.status, "reason": v.reason}
