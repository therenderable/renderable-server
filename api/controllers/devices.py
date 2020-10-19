from datetime import datetime

from models import DeviceDocument, DeviceResponse


def join(context, device_request):
  cluster = context['cluster']
  database = context['database']

  token = cluster.join(device_request.dict())
  device_document = DeviceDocument(**device_request.dict())

  database.save(device_document, 'devices')

  return DeviceResponse(token = token, **device_document.dict())

def get(context, device_id):
  database = context['database']
  device_document = database.find(device_id, 'devices')

  return device_document.dict()
