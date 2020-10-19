from typing import Optional

from fastapi import Request, Security, Depends
from fastapi.security.api_key import APIKeyHeader, APIKey

import exceptions


api_key_header = APIKeyHeader(name = 'X-API-Key', auto_error = False)

def validate_api_key(request: Request, api_key: str = Security(api_key_header)):
  config = request.state.context['config']

  if api_key == config.get('API_ACCESS_KEY'):
    return api_key
  else:
    raise exceptions.invalid_api_key

def validate_optional_api_key(request: Request, api_key: Optional[str] = Security(api_key_header)):
  config = request.state.context['config']

  if api_key is None:
    return None
  elif api_key == config.get('API_ACCESS_KEY'):
    return api_key
  else:
    raise exceptions.invalid_api_key

def get_api_key(optional = False):
  return Depends(validate_optional_api_key if optional else validate_api_key)
