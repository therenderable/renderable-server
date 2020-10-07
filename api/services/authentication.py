from fastapi import Request, Security, Depends
from fastapi.security.api_key import APIKeyHeader, APIKey

from .. import exceptions


api_key_header = APIKeyHeader(name = 'X-API-Key')

def get_api_key(request: Request, api_key_header: str = Security(api_key_header)):
  config = request.state['config']

  if api_key_header == config.get('API_ACCESS_KEY'):
    return api_key_header
  else:
    raise exceptions.invalid_api_key

api_key = Depends(get_api_key)
