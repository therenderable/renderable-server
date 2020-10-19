from datetime import datetime

from pydantic import BaseModel, Field, PositiveInt, HttpUrl

from . import ObjectID, FrameRange, JobState


class Task(BaseModel):
  id: ObjectID = Field(...)
  job_id: ObjectID = Field(...)
  concurrency: PositiveInt = 4
  frame_range: FrameRange = Field(...)
  status: JobState = JobState.ready
  image_url: HttpUrl = None
  created_at: datetime = Field(...)
  updated_at: datetime = None
