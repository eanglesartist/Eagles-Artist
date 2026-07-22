from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db
from typing import List

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, user_id: str, db: Session = Depends(get_db)):
    return crud.create_project(db, user_id, project.name, project.description)

@router.get("/{user_id}", response_model=List[schemas.Project])
def list_projects(user_id: str, db: Session = Depends(get_db)):
    return crud.get_projects(db, user_id)

@router.post("/{project_id}/scenes", response_model=schemas.Scene)
def add_scene(project_id: str, scene: schemas.SceneCreate, db: Session = Depends(get_db)):
    return crud.create_scene(db, project_id, scene.order, scene.prompt)
