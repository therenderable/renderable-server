from datetime import datetime
from typing import Optional, List

from pydantic import Field, HttpUrl

from . import ObjectID, JobState, Base, FrameRange


class JobDocument(Base):
  id: ObjectID = Field(default_factory = ObjectID, alias = '_id')
  task_ids: List[ObjectID] = Field(...)
  concurrency: int = Field(..., gt = 0)
  container_name: str = Field(...)
  frame_range: FrameRange = Field(...)
  status: JobState = Field(...)
  scene_url: Optional[HttpUrl] = None
  image_url: Optional[HttpUrl] = None
  created_at: datetime = Field(default_factory = datetime.now)
  updated_at: datetime = Field(default_factory = datetime.now)


class JobRequest(Base):
  concurrency: int = Field(4, gt = 0)
  container_name: str = Field(...)
  frame_range: FrameRange = Field(...)


class JobResponse(Base):
  id: ObjectID = Field(...)
  concurrency: int = Field(..., gt = 0)
  container_name: str = Field(...)
  frame_range: FrameRange = Field(...)
  status: JobState = Field(...)
  scene_url: Optional[HttpUrl] = Field(...)
  image_url: Optional[HttpUrl] = None
  created_at: datetime = Field(...)
  updated_at: datetime = Field(...)
  tasks: Optional[List['TaskResponse']] = None


from .task import TaskResponse


JobResponse.update_forward_refs()
