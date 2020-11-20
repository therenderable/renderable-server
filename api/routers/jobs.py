from typing import Optional

from fastapi import APIRouter, Request, WebSocket, File, UploadFile

import exceptions
from models import ObjectID, Action, ErrorResponse, JobRequest, JobResponse
from controllers import jobs


router = APIRouter()

responses = {
  exceptions.invalid_container_name.status_code: {'model': ErrorResponse}
}

@router.post('/', response_model = JobResponse, responses = responses, response_model_exclude_unset = True)
def submit_job(request: Request, job: JobRequest):
  return jobs.submit(request.app.state.context, job)

responses = {
  exceptions.invalid_resource_id.status_code: {'model': ErrorResponse},
  exceptions.invalid_job_action('update', 'some').status_code: {'model': ErrorResponse},
  exceptions.invalid_scene_resource.status_code: {'model': ErrorResponse}
}

@router.post('/{job_id}', response_model = JobResponse, responses = responses, response_model_exclude_unset = True)
def update_job_state(request: Request, job_id: ObjectID, action: Action):
  return jobs.update(request.app.state.context, job_id, action)

responses = {
  exceptions.invalid_resource_id.status_code: {'model': ErrorResponse},
  exceptions.invalid_resource_state('some').status_code: {'model': ErrorResponse},
  exceptions.invalid_file_format.status_code: {'model': ErrorResponse}
}

@router.post('/{job_id}/scene', response_model = JobResponse, responses = responses, response_model_exclude_unset = True)
def upload_job_scene(request: Request, job_id: ObjectID, scene: UploadFile = File(...)):
  return jobs.upload_scene(request.app.state.context, job_id, scene)

responses = {
  exceptions.invalid_resource_id.status_code: {'model': ErrorResponse}
}

@router.get('/{job_id}', response_model = JobResponse, responses = responses, response_model_exclude_unset = True)
def get_job_by_id(request: Request, job_id: ObjectID, task_id: Optional[ObjectID] = None):
  return jobs.get(request.app.state.context, job_id, task_id)

@router.websocket('/{job_id}/ws')
async def listen_job_by_id(websocket: WebSocket, job_id: ObjectID):
  await jobs.listen(websocket.app.state.context, websocket, job_id)
