from enum import Enum


class JobState(str, Enum):
  ready = 'ready'
  running = 'running'
  done = 'done'
  error = 'error'
