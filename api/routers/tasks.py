from typing import List

from fastapi import APIRouter, Request, File, UploadFile

import exceptions
from models import ObjectID, ErrorResponse, TaskRequest, TaskResponse
from controllers import authentication as auth, tasks


router = APIRouter()

responses = {
  exceptions.invalid_api_key.status_code: {'model': ErrorResponse},
  exceptions.invalid_resource_id.status_code: {'model': ErrorResponse},
  exceptions.job_not_running.status_code: {'model': ErrorResponse},
  exceptions.invalid_task_state('A', 'B').status_code: {'model': ErrorResponse}
}

@router.post('/{task_id}', response_model = TaskResponse, responses = responses, response_model_exclude_unset = True)
def update_task_state(request: Request, task_id: ObjectID, task: TaskRequest, api_key: auth.APIKey = auth.get_api_key()):
  return tasks.update(request.app.state.context, task_id, task)

responses = {
  exceptions.invalid_api_key.status_code: {'model': ErrorResponse},
  exceptions.invalid_resource_id.status_code: {'model': ErrorResponse},
  exceptions.invalid_resource_state('some').status_code: {'model': ErrorResponse},
  exceptions.image_resource_mismatch.status_code: {'model': ErrorResponse},
  exceptions.invalid_file_format.status_code: {'model': ErrorResponse}
}

@router.post('/{task_id}/images', response_model = TaskResponse, responses = responses, response_model_exclude_unset = True)
def upload_task_images(request: Request, task_id: ObjectID, images: List[UploadFile] = File(...), api_key: auth.APIKey = auth.get_api_key()):
  return tasks.upload_images(request.app.state.context, task_id, images)

responses = {
  exceptions.invalid_api_key.status_code: {'model': ErrorResponse},
  exceptions.invalid_resource_id.status_code: {'model': ErrorResponse}
}

@router.get('/{task_id}', response_model = TaskResponse, responses = responses, response_model_exclude_unset = True)
def get_task_by_id(request: Request, task_id: ObjectID, api_key: auth.APIKey = auth.get_api_key()):
  return tasks.get(request.app.state.context, task_id)
