import pymongo


class Database:
  def __init__(self, hostname, port, username, password):
    self.hostname = hostname
    self.port = port
    self.username = username
    self.password = password

    self.client = pymongo.MongoClient(
      self.hostname, self.port, username = self.username, password = self.password)
    self.db = self.client['db']

  def save_device(self, device):
    devices = self.db['devices']
    devices.insert_one(device.dict(by_alias = True))

    return device

  def save_job(self, job):
    jobs = self.db['jobs']
    jobs.insert_one(job.dict(by_alias = True))

    return job

  def save_tasks(self, tasks):
    tasks = self.db['tasks']
    tasks.insertMany([task.dict(by_alias = True) for task in tasks])

    return tasks
