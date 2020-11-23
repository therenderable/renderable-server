from datetime import datetime
from typing import List, Optional

from pydantic import Field, HttpUrl

from . import ObjectID, State, Base, FrameRange


class TaskDocument(Base):
  id: ObjectID = Field(default_factory = ObjectID, alias = '_id')
  job_id: ObjectID = Field(...)
  container_name: str = Field(...)
  frame_range: FrameRange = Field(...)
  state: State = Field(...)
  image_urls: List[HttpUrl] = []
  created_at: datetime = Field(default_factory = datetime.now)
  updated_at: datetime = Field(default_factory = datetime.now)


class TaskCountDocument(Base):
  container_name: Optional[str] = None
  count: int = Field(..., ge = 0)


class TaskMessage(Base):
  id: ObjectID = Field(...)
  job_id: ObjectID = Field(...)


class TaskRequest(Base):
  state: State = Field(...)


class TaskResponse(Base):
  id: ObjectID = Field(...)
  frame_range: FrameRange = Field(...)
  state: State = Field(...)
  image_urls: List[HttpUrl] = Field(...)
  created_at: datetime = Field(...)
  updated_at: datetime = Field(...)
  job: Optional['JobResponse'] = None


from .job import JobResponse


TaskResponse.update_forward_refs()
