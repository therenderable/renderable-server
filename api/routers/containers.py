from typing import List, Optional

from fastapi import APIRouter, Request

import exceptions
from models import ObjectID, ErrorResponse, ContainerRequest, ContainerResponse
from controllers import authentication as auth, containers


router = APIRouter()

responses = {
  exceptions.invalid_api_key.status_code: {'model': ErrorResponse},
  exceptions.invalid_container_name.status_code: {'model': ErrorResponse},
  exceptions.container_name_already_exists.status_code: {'model': ErrorResponse}
}

@router.post('/', response_model = ContainerResponse, responses = responses, response_model_exclude_unset = True)
def register_container(request: Request, container: ContainerRequest, api_key: auth.APIKey = auth.get_api_key()):
  return containers.register(request.app.state.context, container)

@router.get('/', response_model = List[ContainerResponse], response_model_exclude_unset = True)
def list_containers(request: Request, name: Optional[str] = None):
  return containers.get_list(request.app.state.context, name)

responses = {
  exceptions.invalid_resource_id.status_code: {'model': ErrorResponse}
}

@router.get('/{container_id}', response_model = ContainerResponse, responses = responses, response_model_exclude_unset = True)
def get_container(request: Request, container_id: ObjectID):
  return containers.get(request.app.state.context, container_id)
