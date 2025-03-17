from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from pydantic_core import Url
from sqlmodel import SQLModel

from datetime import datetime

## DB models

class Video(SQLModel, table=True):
    id: int = Field(primary_key=True)
    cloudflare_id: str
    name: str
    uploader: int = Field(default=None, foreign_key="user.id")
    duration: int

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str 
    email: EmailStr

class VideoLike(SQLModel, table=True):
    video_id: int = Field(default=None, foreign_key="video.id")
    user_id: int = Field(default=None, foreign_key="user.id")
    created: datetime

## Response Models

class VideoResponse(BaseModel):
    stream: str
    thumbnail: str
    uploaded_by: str
    duration: int
    likes: int

class PublicUserProfileResponse(BaseModel):
    likes: List[VideoResponse]
    favourites: List[VideoResponse]
    uploads: List[VideoResponse]
    bio: Optional[str]
    profile_photo: Optional[str]

class UploadVideoResponse(BaseModel):
    video_meta: Video
    upload_url: Url
    
