from typing import List
from datetime import datetime
import functools

import utils
import exceptions
from models import State, JobMessage, JobResponse, TaskResponse


def update(context, task_id, task):
  storage = context['storage']
  database = context['database']
  state_queue = context['state_queue']

  task_document = database.find(task_id, 'tasks')

  if task_document is None:
    raise exceptions.invalid_resource_id

  job_document = database.find(task_document.job_id, 'jobs')

  if job_document.state != State.running:
    raise exceptions.job_not_running

  if task.state == State.done:
    if task_document.state != State.running:
      raise exceptions.invalid_task_state(task_document.state, task.state)

    task_document.state = task.state
    task_document.updated_at = datetime.now()

    database.update({ '_id': task_id }, task_document, 'tasks')

    document_query = {
      '_id': {'$in': job_document.task_ids},
      'state': {'$in': [State.ready, State.running]}
    }

    unresolved_task_documents = database.find_many(document_query, 'tasks')

    if len(unresolved_task_documents) == 0:
      document_query['state'] = State.error
      error_task_documents = database.find_many(document_query, 'tasks')

      job_document.state = State.error if len(error_task_documents) > 0 else State.done
      job_document.updated_at = datetime.now()

      database.update({ '_id': job_document.id }, job_document, 'jobs')
  else:
    if task.state == State.running:
      if task_document.state != State.ready:
        raise exceptions.invalid_task_state(task_document.state, task.state)
    elif task.state == State.error:
      if task_document.state not in [State.ready, State.running]:
        raise exceptions.invalid_task_state(task_document.state, task.state)
    else:
      raise exceptions.invalid_task_state(task_document.state, task.state)

    task_document.state = task.state
    task_document.updated_at = datetime.now()

    database.update({ '_id': task_id }, task_document, 'tasks')

  state_queue.publish(JobMessage(**job_document.dict()), job_document.id)

  job_response = JobResponse(**job_document.dict())

  return TaskResponse(**task_document.dict(), job = job_response)

def upload_images(context, task_id, images):
  storage = context['storage']
  database = context['database']
  state_queue = context['state_queue']

  task_document = database.find(task_id, 'tasks')

  if task_document is None:
    raise exceptions.invalid_resource_id

  if task_document.state != State.running:
    raise exceptions.invalid_resource_state(task_document.state)

  frame_count = task_document.frame_range.end - task_document.frame_range.start + 1

  if frame_count != len(images):
    raise exceptions.image_resource_mismatch

  job_document = database.find(task_document.job_id, 'jobs')
  job_response = JobResponse(**job_document.dict())

  container_document = database.find({'name': job_document.container_name}, 'containers')

  def resolve_resources(resources, frame):
    id, image = frame

    file_extension = utils.get_file_extension(image.filename)

    def filter_by_extension(resource):
      return file_extension in resource.extensions

    resource_document = next(filter(filter_by_extension, container_document.images), None)

    if resource_document is None:
      raise exceptions.invalid_file_format

    content_type = resource_document.content_types[0]
    padded_id = str(id).rjust(max(10, len(str(job_document.frame_range.end))))

    resources.append({
      'file': image.file,
      'filename': f'image{padded_id}{file_extension}',
      'content_type': content_type
    })

    return resources

  def upload_resource(resource):
    result = storage.upload(resource['file'], resource['content_type'], 'images', f'{task_id}/{resource["filename"]}')

    return result['resource_url']

  resources = functools.reduce(resolve_resources, enumerate(images, task_document.frame_range.start), [])
  resource_urls = list(map(upload_resource, resources))

  task_document.image_urls = resource_urls
  task_document.updated_at = datetime.now()

  database.update({ '_id': task_id }, task_document, 'tasks')

  state_queue.publish(JobMessage(**job_document.dict()), job_document.id)

  return TaskResponse(**task_document.dict(), job = job_response)

def get(context, task_id):
  database = context['database']

  task_document = database.find(task_id, 'tasks')

  if task_document is None:
    raise exceptions.invalid_resource_id

  job_document = database.find(task_document.job_id, 'jobs')
  job_response = JobResponse(**job_document.dict())

  return TaskResponse(**task_document.dict(), job = job_response)
