from typing import Optional

from fastapi import APIRouter, Request, WebSocket, File, UploadFile

from models import ObjectID, ErrorResponse, JobRequest, JobResponse
from controllers import authentication as auth, jobs


router = APIRouter()

responses = {
  403: {'model': ErrorResponse}
}

@router.post('/', response_model = JobResponse, response_model_exclude_unset = True)
def submit_job(request: Request, job: JobRequest):
  return jobs.submit(request.state.context, job)

@router.post('/{job_id}/upload', response_model = JobResponse, response_model_exclude_unset = True)
def upload_job_scene(request: Request, job_id: ObjectID, scene: UploadFile = File(...)):
  return jobs.upload_scene(request.state.context, job_id, scene)

@router.get('/{job_id}', response_model = JobResponse, responses = responses, response_model_exclude_unset = True)
def get_job_by_id(
    request: Request, job_id: ObjectID, task_id: Optional[ObjectID] = None,
    api_key: auth.APIKey = auth.get_api_key()):
  return jobs.get(request.state.context, job_id, task_id)

@router.websocket('/{job_id}/ws')
def listen_job_by_id(websocket: WebSocket, job_id: ObjectID):
  jobs.listen(websocket.state.context, job_id)
