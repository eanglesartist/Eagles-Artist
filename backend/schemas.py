from pydantic import BaseModel
from typing import Optional
import datetime

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: str
    credits: int
    created_at: datetime.datetime
    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: str
    user_id: str
    created_at: datetime.datetime
    class Config:
        orm_mode = True

class SceneBase(BaseModel):
    order: int
    prompt: str

class SceneCreate(SceneBase):
    pass

class Scene(SceneBase):
    id: str
    project_id: str
    video_url: Optional[str]
    created_at: datetime.datetime
    class Config:
        orm_mode = True

class AssetBase(BaseModel):
    name: str
    type: str
    url: str

class AssetCreate(AssetBase):
    pass

class Asset(AssetBase):
    id: str
    user_id: str
    created_at: datetime.datetime
    class Config:
        orm_mode = True

class JobBase(BaseModel):
    prompt: str
    model: str

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: str
    user_id: str
    status: str
    video_url: Optional[str]
    error_message: Optional[str]
    created_at: datetime.datetime
    completed_at: Optional[datetime.datetime]
    class Config:
        orm_mode = True

class CreditDeductRequest(BaseModel):
    user_id: str
    amount: int = 50

class CreditResponse(BaseModel):
    user_id: str
    credits: int
