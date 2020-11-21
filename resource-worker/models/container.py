from datetime import datetime

from pydantic import Field, conlist

from . import ObjectID, Base, ResourceDocument


class ContainerDocument(Base):
  id: ObjectID = Field(default_factory = ObjectID, alias = '_id')
  name: str = Field(...)
  scenes: conlist(ResourceDocument, min_items = 1)
  images: conlist(ResourceDocument, min_items = 1)
  created_at: datetime = Field(default_factory = datetime.now)
  updated_at: datetime = Field(default_factory = datetime.now)


class ContainerMessage(Base):
  name: str = Field(...)
  replicas: int = Field(..., gt = 0)


class ContainerRequest(Base):
  name: str = Field(...)
  scenes: conlist(ResourceDocument, min_items = 1)
  images: conlist(ResourceDocument, min_items = 1)


class ContainerResponse(Base):
  id: ObjectID = Field(...)
  name: str = Field(...)
  scenes: conlist(ResourceDocument, min_items = 1)
  images: conlist(ResourceDocument, min_items = 1)
  created_at: datetime = Field(...)
  updated_at: datetime = Field(...)
