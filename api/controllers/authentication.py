from typing import Optional

from fastapi import Request, Security, Depends
from fastapi.security.api_key import APIKeyHeader, APIKey

import exceptions


def get_api_key(optional = False):
  api_key_header = APIKeyHeader(name = 'X-API-Key', auto_error = not optional)

  def validate_api_key(request: Request, api_key: Optional[str] = Security(api_key_header)):
    config = request.app.state.context['configuration']

    if api_key is None:
      return None
    elif api_key == config.get('API_ACCESS_KEY'):
      return api_key
    else:
      raise exceptions.invalid_api_key

  return Depends(validate_api_key)
