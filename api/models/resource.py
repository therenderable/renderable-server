from pydantic import conlist

from . import Base


class Resource(Base):
  extensions: conlist(str, min_items = 1)
  content_types: conlist(str, min_items = 1)
