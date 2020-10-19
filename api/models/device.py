from datetime import datetime

from pydantic import BaseModel, Field

from . import ObjectID, NodeType


class DeviceDocument(BaseModel):
  id: ObjectID = Field(default_factory = ObjectID, alias = '_id')
  node_type: NodeType = Field(...)
  joined_at: datetime = Field(default_factory = datetime.now)


  class Config:
    allow_population_by_field_name = True


class DeviceRequest(BaseModel):
  node_type: NodeType = NodeType.worker


class DeviceResponse(BaseModel):
  id: ObjectID = Field(...)
  node_type: NodeType = Field(...)
  token: str = None
  joined_at: datetime = Field(...)
