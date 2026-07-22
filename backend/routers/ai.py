from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db
import threading
import time

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/generate")
def generate(request: schemas.JobCreate, user_id: str, db: Session = Depends(get_db)):
    # Check credits
    credits = crud.get_credits(db, user_id)
    if credits < 50:
        raise HTTPException(status_code=402, detail="Insufficient credits")
    
    # Deduct credits
    success, new_balance = crud.deduct_credits(db, user_id, 50)
    if not success:
        raise HTTPException(status_code=402, detail="Insufficient credits")
    
    # Create job
    job_id = crud.create_job(db, user_id, request.prompt, request.model)
    
    # Background processing (replace with Celery in Phase 4)
    def process():
        time.sleep(5)  # Simulate AI work
        video_url = "https://www.w3schools.com/html/mov_bbb.mp4"
        crud.update_job_status(db, job_id, "completed", video_url)
    
    threading.Thread(target=process).start()
    
    return {"job_id": job_id, "status": "queued", "message": "Job accepted"}

@router.get("/job/{job_id}", response_model=schemas.Job)
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = crud.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
