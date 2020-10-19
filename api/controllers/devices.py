from datetime import datetime

from models import DeviceDocument, DeviceResponse


def join(context, device):
  cluster = context['cluster']
  database = context['database']

  token = cluster.join(device.dict())
  device_document = DeviceDocument(**device.dict())

  database.save(device_document, 'devices')

  return DeviceResponse(**device_document.dict(), token = token)

def get(context, device_id):
  database = context['database']
  device_document = database.find(device_id, 'devices')

  return device_document.dict()
