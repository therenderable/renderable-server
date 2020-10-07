import json
import pika


class Queue:
  def __init__(self, hostname, port, username, password):
    self.hostname = hostname
    self.port = port
    self.username = username
    self.password = password

    credentials = pika.PlainCredentials(self.username, self.password)

    self.parameters = pika.ConnectionParameters(self.hostname, self.port, '/', credentials)
    self.connection = None
    self.channel = None

  def _connect(self, queue_name):
    if not self.connection or self.connection.is_closed:
      self.connection = pika.BlockingConnection(self.parameters)
      self.channel = self.connection.channel()
      self.channel.queue_declare(queue = queue_name, durable = True)

  def _publish(self, message, queue_name):
    self.channel.basic_publish(
      exchange = '',
      routing_key = queue_name,
      body = json.dumps(message).encode(),
      properties = pika.BasicProperties(delivery_mode = 2))

  def enqueue(self, task_message, container_name):
    try:
      self._publish(task_message, container_name)
    except pika.exceptions.ConnectionClosed:
      self._connect(container_name)
      self._publish(task_message, container_name)

  def close(self):
    if self.connection and self.connection.is_open:
      self.connection.close()
