from datetime import datetime
from typing import Optional

from pydantic import Field, HttpUrl

from . import ObjectID, JobState, Base, FrameRange


class TaskDocument(Base):
  id: ObjectID = Field(default_factory = ObjectID, alias = '_id')
  job_id: ObjectID = Field(...)
  frame_range: FrameRange = Field(...)
  status: JobState = Field(...)
  image_url: Optional[HttpUrl] = None
  created_at: datetime = Field(default_factory = datetime.now)
  updated_at: datetime = Field(default_factory = datetime.now)


class TaskRequest(Base):
  status: JobState = JobState.done


class TaskResponse(Base):
  id: ObjectID = Field(...)
  frame_range: FrameRange = Field(...)
  status: JobState = Field(...)
  image_url: Optional[HttpUrl] = None
  created_at: datetime = Field(...)
  updated_at: datetime = Field(...)
  job: Optional['JobResponse'] = None


from .job import JobResponse


TaskResponse.update_forward_refs()
