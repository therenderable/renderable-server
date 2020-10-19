from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import State


class RequestContext(BaseHTTPMiddleware):
  def __init__(self, app, context):
    super().__init__(app)

    self.context = context

  async def dispatch(self, request: Request, call_next):
    request.state.context = self.context

    return await call_next(request)
