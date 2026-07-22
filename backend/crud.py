from sqlalchemy.orm import Session
from . import models, schemas
import uuid
import datetime

# ---------- Users ----------
def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, email: str):
    user = models.User(id=str(uuid.uuid4()), email=email, credits=1250)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_or_create_user(db: Session, user_id: str, email: str = None):
    user = get_user(db, user_id)
    if not user:
        if not email:
            email = f"{user_id}@example.com"
        user = create_user(db, email)
    return user

# ---------- Credits ----------
def get_credits(db: Session, user_id: str) -> int:
    user = get_user(db, user_id)
    if not user:
        return 1250
    return user.credits

def deduct_credits(db: Session, user_id: str, amount: int) -> tuple[bool, int]:
    user = get_user(db, user_id)
    if not user:
        return False, 0
    if user.credits < amount:
        return False, user.credits
    user.credits -= amount
    db.commit()
    return True, user.credits

def add_credits(db: Session, user_id: str, amount: int, stripe_session_id: str = None):
    user = get_or_create_user(db, user_id)
    user.credits += amount
    transaction = models.Transaction(
        id=str(uuid.uuid4()),
        user_id=user_id,
        amount=amount,
        type="purchase",
        description="Credit purchase via Stripe",
        stripe_session_id=stripe_session_id
    )
    db.add(transaction)
    db.commit()
    return user.credits

# ---------- Projects ----------
def create_project(db: Session, user_id: str, name: str, description: str = None):
    project = models.Project(
        id=str(uuid.uuid4()),
        user_id=user_id,
        name=name,
        description=description
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def get_projects(db: Session, user_id: str):
    return db.query(models.Project).filter(models.Project.user_id == user_id).all()

# ---------- Scenes ----------
def create_scene(db: Session, project_id: str, order: int, prompt: str):
    scene = models.Scene(
        id=str(uuid.uuid4()),
        project_id=project_id,
        order=order,
        prompt=prompt
    )
    db.add(scene)
    db.commit()
    db.refresh(scene)
    return scene

# ---------- Jobs ----------
def create_job(db: Session, user_id: str, prompt: str, model: str) -> str:
    job_id = str(uuid.uuid4())
    job = models.Job(
        id=job_id,
        user_id=user_id,
        prompt=prompt,
        model=model,
        status="queued"
    )
    db.add(job)
    db.commit()
    return job_id

def get_job(db: Session, job_id: str):
    return db.query(models.Job).filter(models.Job.id == job_id).first()

def update_job_status(db: Session, job_id: str, status: str, video_url: str = None, error: str = None):
    job = get_job(db, job_id)
    if job:
        job.status = status
        if video_url:
            job.video_url = video_url
        if error:
            job.error_message = error
        if status in ("completed", "failed"):
            job.completed_at = datetime.datetime.utcnow()
        db.commit()
    return job
