from pydantic import BaseModel

from . import ObjectID


class Base(BaseModel):
  class Config:
    allow_population_by_field_name = True

    json_encoders = {
      ObjectID: lambda value: str(value)
    }
