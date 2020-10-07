from datetime import datetime
from pydantic import BaseModel, Field

from . import ObjectID


class Device(BaseModel):
  id: ObjectID = Field(..., alias = '_id')
  joined_at: datetime = Field(...)
