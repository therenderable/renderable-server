from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestState(BaseHTTPMiddleware):
  def __init__(self, state):
    self.state = state

  async def dispatch(self, request: Request, call_next):
    request.state.update(self.state)

    return await call_next(request)
