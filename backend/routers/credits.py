from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/credits", tags=["credits"])

@router.get("/{user_id}", response_model=schemas.CreditResponse)
def get_credits(user_id: str, db: Session = Depends(get_db)):
    credits = crud.get_credits(db, user_id)
    return {"user_id": user_id, "credits": credits}

@router.post("/deduct", response_model=schemas.CreditResponse)
def deduct_credits(req: schemas.CreditDeductRequest, db: Session = Depends(get_db)):
    success, balance = crud.deduct_credits(db, req.user_id, req.amount)
    if not success:
        raise HTTPException(status_code=402, detail="Insufficient credits")
    return {"user_id": req.user_id, "credits": balance}
