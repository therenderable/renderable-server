from bson.objectid import ObjectId
from bson.errors import InvalidId


class ObjectID(ObjectId):
  @classmethod
  def __get_validators__(cls):
    yield cls.validate

  @classmethod
  def __modify_schema__(cls, field_schema):
    field_schema.update(type = 'string')

  @classmethod
  def validate(cls, value):
    if isinstance(value, ObjectId):
      return str(value)
    else:
      try:
        return str(ObjectId(value))
      except InvalidId:
        raise ValueError('invalid ID')
