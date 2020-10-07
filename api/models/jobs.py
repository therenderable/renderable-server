from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, HttpUrl

from . import ObjectID, FrameRange, JobState


class Job(BaseModel):
  id: ObjectID = Field(..., alias = '_id')
  task_ids: List[ObjectID] = Field(..., min_items = 1)
  container_name: str = Field(...)
  frame_range: FrameRange = Field(...)
  status: JobState = JobState.ready
  scene_url: HttpUrl = Field(...)
  created_at: datetime = Field(...)
  updated_at: datetime = None
