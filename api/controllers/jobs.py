import asyncio

from renderable_core import utils
from renderable_core.models import ObjectID, State, Action, FrameRange, ControlFrameType, ControlFrame,\
  ContainerMessage, JobDocument, JobMessage, JobResponse, TaskDocument, TaskMessage, TaskResponse

import exceptions


def submit(context, job):
  database = context['database']

  container_document = database.find({'name': job.container_name}, 'containers')

  if container_document is None:
    raise exceptions.invalid_container_name

  job_id = ObjectID()
  frame_groups = utils.group_frames(job.frame_range.start, job.frame_range.end, job.parallelism)

  def create_task(group):
    return TaskDocument(
      job_id = job_id,
      frame_range = FrameRange(start = group[0], end = group[len(group) - 1]),
      state = State.ready,
      retries = 0)

  def get_task_id(task):
    return task.id

  task_documents = list(map(create_task, frame_groups))
  task_ids = list(map(get_task_id, task_documents))

  job_document = JobDocument(
    **job.dict(),
    id = job_id,
    task_ids = task_ids,
    state = State.ready)

  database.save_many(task_documents, 'tasks')
  database.save(job_document, 'jobs')

  task_responses = [TaskResponse(**task_document.dict()) for task_document in task_documents]

  return JobResponse(**job_document.dict(), tasks = task_responses)

def update(context, job_id, job):
  cluster = context['cluster']
  database = context['database']
  container_queue = context['container_queue']
  task_queue = context['task_queue']
  state_queue = context['state_queue']

  job_document = database.find(job_id, 'jobs')

  if job_document is None:
    raise exceptions.invalid_resource_id

  task_documents = database.find_many({'_id': {'$in': job_document.task_ids}}, 'tasks')
  task_responses = [TaskResponse(**task_document.dict()) for task_document in task_documents]

  if job.action == Action.start:
    if job_document.state != State.ready:
      raise exceptions.invalid_job_action(job.action, job_document.state)

    if job_document.scene_url is None:
      raise exceptions.invalid_scene_resource

    cluster.create_service(job_document.container_name)

    container_message = ContainerMessage(
      name = job_document.container_name,
      task_count = len(job_document.task_ids),
      upscaling = True)

    task_messages = [TaskMessage(**task_document.dict()) for task_document in task_documents]

    container_queue.publish([container_message], 'autoscaling')
    task_queue.publish(task_messages, job_document.container_name)

    job_document.state = State.running
  else:
    raise exceptions.invalid_job_action(job.action, job_document.state)

  job_document.updated_at = utils.utc_now()

  database.update({ '_id': job_id }, job_document, 'jobs')

  state_queue.publish(JobMessage(**job_document.dict()), job_id)

  return JobResponse(**job_document.dict(), tasks = task_responses)

def upload_scene(context, job_id, scene):
  storage = context['storage']
  database = context['database']
  state_queue = context['state_queue']

  job_document = database.find(job_id, 'jobs')

  if job_document is None:
    raise exceptions.invalid_resource_id

  if job_document.state != State.ready:
    raise exceptions.invalid_resource_state(job_document.state)

  task_documents = database.find_many({'_id': {'$in': job_document.task_ids}}, 'tasks')
  task_responses = [TaskResponse(**task_document.dict()) for task_document in task_documents]

  container_document = database.find({'name': job_document.container_name}, 'containers')
  file_extension = utils.get_file_extension(scene.filename)

  def filter_by_extension(resource):
    return file_extension in resource.extensions

  resource_document = next(filter(filter_by_extension, container_document.scenes), None)

  if resource_document is None:
    raise exceptions.invalid_file_format

  content_type = resource_document.content_types[0]

  result = storage.upload(scene.file, content_type, 'scenes', f'{job_id}/scene{file_extension}')

  job_document.scene_url = result['resource_url']
  job_document.updated_at = utils.utc_now()

  database.update({ '_id': job_id }, job_document, 'jobs')

  state_queue.publish(JobMessage(**job_document.dict()), job_id)

  return JobResponse(**job_document.dict(), tasks = task_responses)

def get(context, job_id, task_id = None):
  database = context['database']

  job_document = database.find(job_id, 'jobs')

  if job_document is None:
    raise exceptions.invalid_resource_id

  if task_id is None:
    task_documents = database.find_many({'_id': {'$in': job_document.task_ids}}, 'tasks')
  else:
    if task_id in job_document.task_ids:
      task_documents = [database.find(task_id, 'tasks')]
    else:
      task_documents = []

  task_responses = [TaskResponse(**task_document.dict()) for task_document in task_documents]

  return JobResponse(**job_document.dict(), tasks = task_responses)

async def listen(context, websocket, job_id):
  configuration = context['configuration']
  database = context['database']
  state_queue = context['state_queue']

  websocket_timeout = int(configuration.get('API_WEBSOCKET_TIMEOUT'))
  websocket_heartbeat_period = int(configuration.get('API_WEBSOCKET_HEARTBEAT_PERIOD'))

  loop = asyncio.get_event_loop()

  async def is_websocket_active():
    try:
      ping_frame = ControlFrame(type = ControlFrameType.ping)

      await asyncio.wait_for(websocket.send_text(ping_frame.json()), websocket_timeout)

      response = await asyncio.wait_for(websocket.receive_json(), websocket_timeout)
      pong_frame = ControlFrame(**response)

      return pong_frame.type == ControlFrameType.pong
    except:
      return False

  async def handle_connection():
    while True:
      try:
        await asyncio.sleep(websocket_heartbeat_period)
        assert await is_websocket_active()
      except:
        await utils.run_as_async(state_queue.publish, JobMessage(), job_id)
        break

  async def process_message(channel, method, job_message):
    try:
      if job_message.id is None:
        assert await is_websocket_active()
      else:
        job_document = database.find(job_id, 'jobs')

        assert job_document is not None

        task_documents = database.find_many({'_id': {'$in': job_document.task_ids}}, 'tasks')
        task_responses = [TaskResponse(**task_document.dict()) for task_document in task_documents]

        job_response = JobResponse(**job_document.dict(), tasks = task_responses)

        await asyncio.wait_for(websocket.send_text(job_response.json(exclude_unset = True)), websocket_timeout)
    except:
      channel.stop_consuming()
      channel.connection.close()

  def callback(channel, method, job_message):
    utils.run_as_sync(process_message(channel, method, job_message), loop)

  await websocket.accept()

  task = asyncio.create_task(handle_connection())

  await utils.run_as_async(state_queue.consume, callback, job_id, JobMessage)
  await task
