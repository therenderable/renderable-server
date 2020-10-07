from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl

from . import ObjectID, FrameRange, JobState


class Task(BaseModel):
  id: ObjectID = Field(..., alias = '_id')
  job_id: ObjectID = Field(...)
  frame_range: FrameRange = Field(...)
  status: JobState = JobState.ready
  image_url: HttpUrl = None
  created_at: datetime = Field(...)
  updated_at: datetime = None
