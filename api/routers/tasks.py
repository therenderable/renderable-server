from fastapi import APIRouter, Request, File, UploadFile

from models import ObjectID, ErrorResponse, TaskRequest, TaskResponse
from controllers import authentication as auth, tasks


router = APIRouter()

responses = {
  403: {'model': ErrorResponse}
}

@router.patch('/', response_model = TaskResponse, responses = responses, response_model_exclude_unset = True)
def submit_task(request: Request, task: TaskRequest, api_key: auth.APIKey = auth.get_api_key()):
  return tasks.submit(request.state.context, task)

@router.patch('/{task_id}/upload', response_model = TaskResponse, responses = responses, response_model_exclude_unset = True)
def upload_task_image(request: Request, image: UploadFile = File(...), api_key: auth.APIKey = auth.get_api_key()):
  return tasks.upload_image(request.state.context, task_id, image)

@router.get('/{task_id}', response_model = TaskResponse, responses = responses, response_model_exclude_unset = True)
def get_task_by_id(request: Request, task_id: ObjectID, api_key: auth.APIKey = auth.get_api_key()):
  return tasks.get(request.state.context, task_id)
