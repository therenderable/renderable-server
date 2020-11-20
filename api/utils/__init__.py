from pathlib import Path
import asyncio
from functools import partial

import numpy as np


def get_file_extension(filename):
  filename = Path(filename)

  return filename.suffix

def group_frames(start, end, parallelism):
  end = end + 1

  frame_count = end - start
  parallelism = min(frame_count, parallelism)
  frame_batch = round(frame_count / parallelism)

  frames = np.arange(start, end)
  groups = np.split(frames, np.arange(frame_batch, len(frames), frame_batch))

  return [group.tolist() for group in groups]

def run_as_sync(coroutine, loop):
  future = asyncio.run_coroutine_threadsafe(coroutine, loop)

  return future.result()

async def run_as_async(function, *args, **kwargs):
  loop = asyncio.get_running_loop()
  partial_function = partial(function, *args, **kwargs)

  return await loop.run_in_executor(None, partial_function)
