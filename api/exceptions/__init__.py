from fastapi import HTTPException, status


invalid_api_key = HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'Not authenticated')
invalid_resource_id = HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Resource not found')
invalid_container_name = HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Invalid container name')
container_name_already_exists = HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Container name already exists')
invalid_file_format = HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Invalid file format')
invalid_scene_resource = HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Invalid scene resource')
invalid_image_resources = HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Invalid image resources')
image_resource_mismatch = HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Mismatched image resources')
job_not_running = HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Parent job not running')

def invalid_resource_state(state):
  return HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = f'Cannot update resource in "{state}" state')

def invalid_job_action(action, state):
  return HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = f'Cannot "{action}" job in "{state}" state')

def invalid_task_state(source_state, target_state):
  return HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = f'Cannot transition task state from "{source_state}" to "{target_state}"')
