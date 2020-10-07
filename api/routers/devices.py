from fastapi import APIRouter

from ..models import ObjectID, Device
from ..services import authentication as auth, devices


router = APIRouter()

@router.post('/')
def join_cluster(response_model = Device):
  return devices.join_cluster()

@router.get('/{device_id}')
def get_devices(device_id: ObjectID, api_key: auth.APIKey = auth.api_key):
  return devices.get_device(device_id)
