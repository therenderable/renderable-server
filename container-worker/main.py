from pathlib import Path

from renderable_core.models import ContainerMessage
from renderable_core.services import Configuration, Autoscaler, WorkQueue


configuration = Configuration(Path('/run/secrets/'))

autoscaler = Autoscaler(
  configuration.get('CLUSTER_HOSTNAME'),
  configuration.get('CLUSTER_PORT'),
  Path(configuration.get('CLUSTER_CERTIFICATE_PATH')),
  int(configuration.get('CLUSTER_COOLDOWN_PERIOD')))

container_queue = WorkQueue(
  configuration.get('CONTAINER_QUEUE_HOSTNAME'),
  configuration.get('CONTAINER_QUEUE_PORT'),
  configuration.get('CONTAINER_QUEUE_USERNAME'),
  configuration.get('CONTAINER_QUEUE_PASSWORD'))


def callback(channel, method, container_message):
  autoscaler.scale(
    container_message.name,
    container_message.task_count,
    container_message.upscaling)

  channel.basic_ack(delivery_tag = method.delivery_tag)


if __name__ == '__main__':
  container_queue.consume(callback, 'autoscaling', ContainerMessage)
