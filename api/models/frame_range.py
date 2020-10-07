from pydantic import validator, BaseModel, Field


class FrameRange(BaseModel):
  start: int = Field(...)
  end: int = Field(...)

  @validator('start')
  def validate_range(cls, value, values):
    if value > values['end']:
      raise ValueError('invalid range')

    return value
