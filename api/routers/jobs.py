from fastapi import APIRouter

from ..services import jobs


router = APIRouter()

@router.post('/')
def join_cluster(response_model = Device):
  return devices.join_cluster()

@router.get('/{device_id}')
def get_device(device_id: ObjectID):
  return devices.get_device(device_id)
