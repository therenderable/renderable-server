from pathlib import Path

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services import Configuration, Cluster, Database, Storage, WorkQueue, EventQueue
from routers import api


configuration = Configuration(Path('/run/secrets/'))

api_version = configuration.get('API_VERSION')
api_production = configuration.get('API_PRODUCTION') == 'on'
api_workers = int(configuration.get('API_WORKERS'))
api_hostname = configuration.get('API_HOSTNAME')
api_port = int(configuration.get('API_PORT'))

cluster_secret_variables = ['API_ACCESS_KEY', 'TASK_QUEUE_USERNAME', 'TASK_QUEUE_PASSWORD']
cluster_secrets = { name: configuration.get(name) for name in cluster_secret_variables }

cluster_environment_variables = ['API_DOMAIN', 'API_PRODUCTION', 'TASK_QUEUE_DOMAIN', 'TASK_QUEUE_PORT']
cluster_environment = { name: configuration.get(name) for name in cluster_environment_variables }

cluster = Cluster(
  configuration.get('CLUSTER_DOMAIN_IP'),
  configuration.get('CLUSTER_HOSTNAME'),
  configuration.get('CLUSTER_PORT'),
  configuration.get('CLUSTER_MANAGER_PORT'),
  Path(configuration.get('CLUSTER_CERTIFICATE_PATH')),
  configuration.get('REGISTRY_DOMAIN'),
  api_production,
  configuration.get('REGISTRY_USERNAME'),
  configuration.get('REGISTRY_PASSWORD'),
  cluster_secrets,
  cluster_environment)

database = Database(
  configuration.get('DATABASE_HOSTNAME'),
  configuration.get('DATABASE_PORT'),
  configuration.get('DATABASE_USERNAME'),
  configuration.get('DATABASE_PASSWORD'))

storage = Storage(
  configuration.get('STORAGE_DOMAIN'),
  api_production,
  configuration.get('STORAGE_HOSTNAME'),
  configuration.get('STORAGE_PORT'),
  configuration.get('STORAGE_ACCESS_KEY'),
  configuration.get('STORAGE_SECRET_KEY'))

container_queue = WorkQueue(
  configuration.get('CONTAINER_QUEUE_HOSTNAME'),
  configuration.get('CONTAINER_QUEUE_PORT'),
  configuration.get('CONTAINER_QUEUE_USERNAME'),
  configuration.get('CONTAINER_QUEUE_PASSWORD'))

task_queue = WorkQueue(
  configuration.get('TASK_QUEUE_HOSTNAME'),
  configuration.get('TASK_QUEUE_PORT'),
  configuration.get('TASK_QUEUE_USERNAME'),
  configuration.get('TASK_QUEUE_PASSWORD'))

resource_queue = WorkQueue(
  configuration.get('RESOURCE_QUEUE_HOSTNAME'),
  configuration.get('RESOURCE_QUEUE_PORT'),
  configuration.get('RESOURCE_QUEUE_USERNAME'),
  configuration.get('RESOURCE_QUEUE_PASSWORD'))

state_queue = EventQueue(
  configuration.get('STATE_QUEUE_HOSTNAME'),
  configuration.get('STATE_QUEUE_PORT'),
  configuration.get('STATE_QUEUE_USERNAME'),
  configuration.get('STATE_QUEUE_PASSWORD'))

context = {
  'configuration': configuration,
  'cluster': cluster,
  'database': database,
  'storage': storage,
  'container_queue': container_queue,
  'task_queue': task_queue,
  'resource_queue': resource_queue,
  'state_queue': state_queue
}

app = FastAPI(redoc_url = None)

app.state.context = context

app.add_middleware(
  CORSMiddleware,
  allow_origins = ['*'],
  allow_methods = ['*'],
  allow_headers = ['*'],
  allow_credentials = True)

app.include_router(api.router, prefix = f'/{api_version}')


if __name__ == '__main__':
  uvicorn.run(
    'main:app', host = api_hostname or '0.0.0.0', port = api_port,
    workers = api_workers, debug = not api_production)
