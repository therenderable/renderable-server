from pathlib import Path
import functools

from renderable_core import utils
from renderable_core.models import ResourceMessage, JobMessage
from renderable_core.services import Configuration, Database, Storage, WorkQueue, EventQueue


configuration = Configuration(Path('/run/secrets/'))

api_production = configuration.get('API_PRODUCTION') == 'on'

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


def callback(channel, method, resource_message):
  try:
    job_document = database.find(resource_message.job_id, 'jobs')
    task_documents = database.find_many({'_id': {'$in': job_document.task_ids}}, 'tasks')

    def format_resource(resource_url):
      bucket_name, object_name_prefix, filename = resource_url.split('/')[-3:]

      return {
        'bucket_name': bucket_name,
        'object_name': f'{object_name_prefix}/{filename}',
        'filename': filename
      }

    def resolve_resources(resources, task):
      resource_list = list(map(format_resource, task.image_urls))
      resources.extend(resource_list)

      return resources

    def download_resource(resource):
      result = storage.download(resource['bucket_name'], resource['object_name'])

      return resource['filename'], result['data']

    resources = functools.reduce(resolve_resources, task_documents, [])

    files = list(map(download_resource, resources))
    zip_data = utils.compress_files(files)

    result = storage.upload(zip_data, 'application/zip', 'sequences', f'{job_document.id}/sequence.zip')

    job_document.sequence_url = result['resource_url']
    job_document.state = resource_message.job_state
    job_document.updated_at = utils.utc_now()

    database.update({ '_id': job_document.id }, job_document, 'jobs')

    state_queue.publish(JobMessage(**job_document.dict()), job_document.id)

    channel.basic_ack(delivery_tag = method.delivery_tag)
  except:
    channel.basic_nack(delivery_tag = method.delivery_tag)


if __name__ == '__main__':
  resource_queue.consume(callback, 'packing', ResourceMessage)
