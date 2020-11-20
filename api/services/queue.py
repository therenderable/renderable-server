import json

import pika

from models import JobMessage


class Queue:
  def __init__(self, hostname, port, username, password):
    self.hostname = hostname
    self.port = port
    self.username = username
    self.password = password

    credentials = pika.PlainCredentials(self.username, self.password)

    self.parameters = pika.ConnectionParameters(self.hostname, self.port, '/', credentials)

  def publish(self, message, routing_key):
    raise NotImplementedError

  def consume(self, callback, routing_key):
    raise NotImplementedError


class TaskQueue(Queue):
  def publish(self, task_messages, container_name):
    connection = pika.BlockingConnection(self.parameters)
    channel = connection.channel()

    channel.queue_declare(queue = container_name, durable = True)

    for task_message in task_messages:
      channel.basic_publish(
        exchange = '',
        routing_key = container_name,
        body = task_message.json(),
        properties = pika.BasicProperties(delivery_mode = 2))

    connection.close()


class StateQueue(Queue):
  def publish(self, job_message, job_id):
    connection = pika.BlockingConnection(self.parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange = 'state', exchange_type = 'direct')

    channel.basic_publish(
      exchange = 'state',
      routing_key = str(job_id),
      body = job_message.json())

    connection.close()

  def consume(self, listener, job_id):
    def callback(channel, method, properties, body):
      job_message = JobMessage(**json.loads(body.decode()))

      listener(channel, job_message)

    connection = pika.BlockingConnection(self.parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange = 'state', exchange_type = 'direct')

    result = channel.queue_declare(queue = '', exclusive = True)
    queue_name = result.method.queue

    channel.queue_bind(exchange = 'state', queue = queue_name, routing_key = str(job_id))

    channel.basic_consume(queue = queue_name, on_message_callback = callback, auto_ack = True)
    channel.start_consuming()
