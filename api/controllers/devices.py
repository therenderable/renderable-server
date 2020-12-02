from renderable_core.models import DeviceDocument, DeviceResponse

import exceptions


def join(context, device):
  cluster = context['cluster']
  database = context['database']

  address = cluster.get_address()
  token = cluster.join(device.dict())

  device_document = DeviceDocument(
    **device.dict(),
    cluster_address = address,
    token = token)

  database.save(device_document, 'devices')

  return DeviceResponse(**device_document.dict())

def get(context, device_id):
  database = context['database']
  device_document = database.find(device_id, 'devices')

  if device_document is None:
    raise exceptions.invalid_resource_id

  return DeviceResponse(**device_document.dict())
