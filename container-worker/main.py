from pathlib import Path

from models import State, ContainerMessage, TaskCountDocument
from services import Configuration, Autoscaler, Database, WorkQueue


configuration = Configuration(Path('/run/secrets/'))

autoscaler = Autoscaler(
  configuration.get('CLUSTER_HOSTNAME'),
  configuration.get('CLUSTER_PORT'),
  Path(configuration.get('CLUSTER_CERTIFICATE_PATH')),
  int(configuration.get('CLUSTER_AVERAGE_TASKS_PER_WORKER')),
  float(configuration.get('CLUSTER_AUTOSCALE_THRESHOLD')))

database = Database(
  configuration.get('DATABASE_HOSTNAME'),
  configuration.get('DATABASE_PORT'),
  configuration.get('DATABASE_USERNAME'),
  configuration.get('DATABASE_PASSWORD'))

container_queue = WorkQueue(
  configuration.get('CONTAINER_QUEUE_HOSTNAME'),
  configuration.get('CONTAINER_QUEUE_PORT'),
  configuration.get('CONTAINER_QUEUE_USERNAME'),
  configuration.get('CONTAINER_QUEUE_PASSWORD'))


def callback(channel, method, container_message):
  try:
    pipeline_query = [
      {'$match': {'state': {'$in': [State.ready, State.running]}}},
      {'$group': {'_id': '$container_name', 'count': {'$sum': 1}}},
      {'$project': {'_id': 0, 'container_name': '$_id', 'count': 1}}
    ]

    task_count_documents = database.compute(pipeline_query, 'tasks', TaskCountDocument)
    task_state = {task_count.container_name: task_count.count for task_count in task_count_documents}

    autoscaler.scale(task_state)

    channel.basic_ack(delivery_tag = method.delivery_tag)
  except:
    channel.basic_nack(delivery_tag = method.delivery_tag)


if __name__ == '__main__':
  container_queue.consume(callback, 'autoscaling', ContainerMessage)
