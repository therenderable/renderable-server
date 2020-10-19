from pathlib import Path

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services import Configuration, Cluster, Database, Storage, Queue
from middlewares import RequestContext
from routers import api


config = Configuration(Path('/run/secrets/'))

cluster_secrets = { name: config.get(name) for name in ['API_ACCESS_KEY', 'QUEUE_USERNAME', 'QUEUE_PASSWORD'] }

cluster = Cluster(
  config.get('CLUSTER_DOMAIN_IP'),
  config.get('CLUSTER_HOSTNAME'), config.get('CLUSTER_PORT'), config.get('CLUSTER_MASTER_PORT'),
  Path(config.get('CLUSTER_CERTIFICATE_PATH')),
  cluster_secrets)

database = Database(
  config.get('DATABASE_HOSTNAME'), config.get('DATABASE_PORT'),
  config.get('DATABASE_USERNAME'), config.get('DATABASE_PASSWORD'))

storage = Storage(
  config.get('STORAGE_DOMAIN'),
  config.get('STORAGE_HOSTNAME'), config.get('STORAGE_PORT'),
  config.get('STORAGE_ACCESS_KEY'), config.get('STORAGE_SECRET_KEY'))

queue = Queue(
  config.get('QUEUE_HOSTNAME'), config.get('QUEUE_PORT'),
  config.get('QUEUE_USERNAME'), config.get('QUEUE_PASSWORD'))

context = {
  'config': config,
  'cluster': cluster,
  'database': database,
  'storage': storage,
  'queue': queue
}

api_version = config.get('API_VERSION')

api_hostname = config.get('API_HOSTNAME')
api_port = config.get('API_PORT')

app = FastAPI(redoc_url = None)

app.add_middleware(
  CORSMiddleware,
  allow_origins = ['*'],
  allow_methods = ['*'],
  allow_headers = ['*'],
  allow_credentials = True)

app.add_middleware(RequestContext, context = context)

app.include_router(api.router, prefix = f'/{api_version}')


if __name__ == '__main__':
  uvicorn.run(app, host = api_hostname or '0.0.0.0', port = api_port)
