from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db
import threading
import time
import replicate
import os
from ..services.ai_service import enhance_prompt

router = APIRouter(prefix="/ai", tags=["ai"])

MODEL_MAP = {
    "veo": "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
    "runway": "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
    "sora": "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
    "kling": "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438"
}

@router.post("/generate")
def generate(request: schemas.JobCreate, user_id: str, db: Session = Depends(get_db)):
    credits = crud.get_credits(db, user_id)
    if credits < 50:
        raise HTTPException(status_code=402, detail="Insufficient credits")
    success, new_balance = crud.deduct_credits(db, user_id, 50)
    if not success:
        raise HTTPException(status_code=402, detail="Insufficient credits")
    job_id = crud.create_job(db, user_id, request.prompt, request.model)

    def process():
        try:
            crud.update_job_status(db, job_id, "processing")
            enhanced_prompt = enhance_prompt(request.prompt)
            model_version = MODEL_MAP.get(request.model.lower(), MODEL_MAP["veo"])
            prediction = replicate.predictions.create(
                version=model_version,
                input={
                    "prompt": enhanced_prompt,
                    "width": 1024,
                    "height": 576,
                    "num_frames": 14,
                    "fps": 7,
                    "steps": 25,
                    "cfg_scale": 9.0,
                }
            )
            while True:
                prediction.reload()
                if prediction.status == "succeeded":
                    video_url = prediction.output
                    crud.update_job_status(db, job_id, "completed", video_url)
                    break
                elif prediction.status == "failed":
                    crud.update_job_status(db, job_id, "failed", error=str(prediction.error))
                    break
                time.sleep(2)
        except Exception as e:
            crud.update_job_status(db, job_id, "failed", error=str(e))

    threading.Thread(target=process).start()
    return {"job_id": job_id, "status": "queued", "message": "Job accepted"}

@router.get("/job/{job_id}", response_model=schemas.Job)
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = crud.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
