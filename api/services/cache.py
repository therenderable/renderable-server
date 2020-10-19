import redis


class Cache:
  def __init__(self, hostname, port, password):
    self.hostname = hostname
    self.port = port
    self.password = password

    self.connection = redis.ConnectionPool(
      host = self.hostname, port = self.port, db = 0, password = self.password)

    self.client = None

  def _connect(self):
    self.client = redis.Redis(connection_pool = self.connection)

  def store(self, session_id, job_id):
    self._connect()

    return self.client.hmset('session_to_job', { session_id: job_id }) \
      and self.client.hmset('job_to_session', { job_id: session_id })

  def remove(self, session_id):
    self._connect()

    job_id = self.client.hget('session_to_job', session_id)

    return job_id \
      and self.client.hdel('session_to_job', session_id) \
      and self.client.hdel('job_to_session', job_id)

  def get_job_id(self, session_id):
    self._connect()

    return self.client.hget('session_to_job', session_id)

  def get_session_id(self, job_id):
    self._connect()

    return self.client.hget('job_to_session', job_id)
