from pydantic import validator, Field

from . import Base


class FrameRange(Base):
  start: int = Field(...)
  end: int = Field(...)

  @validator('end')
  def validate_range(cls, value, values):
    if value > values['start']:
      raise ValueError('invalid range')

    return value
