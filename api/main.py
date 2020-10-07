import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services import Configuration, Cluster, Database, Storage, Cache, Queue
from middlewares import RequestState
from routers import api


config = Configuration('/run/secrets/')

cluster = Cluster(
  config.get('CLUSTER_DOMAIN'),
  config.get('CLUSTER_HOSTNAME'), config.get('CLUSTER_PORT'), config.get('CLUSTER_MASTER_PORT'))

database = Database(
  config.get('DATABASE_HOSTNAME'), config.get('DATABASE_PORT'),
  config.get('DATABASE_USERNAME'), config.get('DATABASE_PASSWORD'))

storage = Storage(
  config.get('STORAGE_DOMAIN'),
  config.get('STORAGE_HOSTNAME'), config.get('STORAGE_PORT'),
  config.get('STORAGE_ACCESS_KEY'), config.get('STORAGE_SECRET_KEY'))

cache = Cache(config.get('CACHE_HOSTNAME'), config.get('CACHE_PORT'), config.get('CACHE_PASSWORD'))

queue = Queue(
  config.get('QUEUE_HOSTNAME'), config.get('QUEUE_PORT'),
  config.get('QUEUE_USERNAME'), config.get('QUEUE_PASSWORD'))

state = {
  'config': config,
  'cluster': cluster,
  'database': database,
  'storage': storage,
  'cache': cache,
  'queue': queue
}

api_version = configuration.get('API_VERSION')
api_port = int(configuration.get('API_PORT'))

app = FastAPI(redoc_url = None)

app.add_middleware(
  CORSMiddleware,
  allow_origins = ['*'],
  allow_methods = ['*'],
  allow_headers = ['*'],
  allow_credentials = True)

app.add_middleware(RequestState, state)

app.include_router(api.router, prefix = f'/{api_version}')


if __name__ == '__main__':
  uvicorn.run(app, host = '0.0.0.0', port = api_port)
