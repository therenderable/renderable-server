import exceptions
from models import ContainerDocument, ContainerResponse


def register(context, container):
  cluster = context['cluster']
  database = context['database']

  container_name = container.name

  if container_name == 'renderable-box' or container_name not in cluster.get_container_names():
    raise exceptions.invalid_container_name

  container_document = database.find({'name': container_name}, 'containers')

  if container_document is not None:
    raise exceptions.container_name_already_exists

  container_document = ContainerDocument(**container.dict())
  database.save(container_document, 'containers')

  return ContainerResponse(**container_document.dict())

def get_list(context, name = None):
  database = context['database']

  if name is None:
    container_documents = database.find_many({}, 'containers')
  else:
    container_documents = database.find({'name': name}, 'containers')
    container_documents = [] if container_documents is None else [container_documents]

  return [ContainerResponse(**container_document.dict()) for container_document in container_documents]

def get(context, container_id):
  database = context['database']
  container_document = database.find(container_id, 'containers')

  if container_document is None:
    raise exceptions.invalid_resource_id

  return ContainerResponse(**container_document.dict())
