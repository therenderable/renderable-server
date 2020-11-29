from fastapi import APIRouter, Request

from renderable_core.models import ObjectID, NodeType, ErrorResponse, DeviceRequest, DeviceResponse

import exceptions
from controllers import authentication as auth, devices


router = APIRouter()

responses = {
  exceptions.invalid_api_key.status_code: {'model': ErrorResponse}
}

@router.post('/', response_model = DeviceResponse, responses = responses, response_model_exclude_unset = True)
def join_device(request: Request, device: DeviceRequest, api_key: auth.APIKey = auth.get_api_key(optional = True)):
  if api_key is None and device.node_type == NodeType.manager:
    raise exceptions.invalid_api_key

  return devices.join(request.app.state.context, device)

responses = {
  exceptions.invalid_api_key.status_code: {'model': ErrorResponse},
  exceptions.invalid_resource_id.status_code: {'model': ErrorResponse}
}

@router.get('/{device_id}', response_model = DeviceResponse, responses = responses, response_model_exclude_unset = True)
def get_device_by_id(request: Request, device_id: ObjectID, api_key: auth.APIKey = auth.get_api_key()):
  return devices.get(request.app.state.context, device_id)
