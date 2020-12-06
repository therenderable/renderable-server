from renderable_core.models import DeviceDocument, DeviceResponse

import exceptions


def join(context, device):
  cluster = context['cluster']
  database = context['database']

  address = cluster.get_address()
  token = cluster.join(device.dict())

  device_document = DeviceDocument(**device.dict())

  database.save(device_document, 'devices')

  return DeviceResponse(
    **device_document.dict(),
    cluster_address = address,
    token = token)

def get(context, device_id):
  cluster = context['cluster']
  database = context['database']

  device_document = database.find(device_id, 'devices')

  if device_document is None:
    raise exceptions.invalid_resource_id

  address = cluster.get_address()
  token = cluster.join(device_document.dict())

  return DeviceResponse(
    **device_document.dict(),
    cluster_address = address,
    token = token)
