from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse
from typing import List

router = APIRouter(prefix="/api/transactions", tags=["transactions"])

@router.post("/", response_model=TransactionResponse)
def create_transaction(req: TransactionCreate, db: Session = Depends(get_db)):
    t = Transaction(**req.dict())
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

@router.get("/", response_model=List[TransactionResponse])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()

@router.get("/{id}", response_model=TransactionResponse)
def get_transaction(id: int, db: Session = Depends(get_db)):
    t = db.query(Transaction).filter(Transaction.id == id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return t

@router.put("/{id}/status")
def update_transaction_status(id: int, status: str, db: Session = Depends(get_db)):
    t = db.query(Transaction).filter(Transaction.id == id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transaction not found")
    t.status = status
    db.commit()
    return {"status": "success", "new_status": status}
