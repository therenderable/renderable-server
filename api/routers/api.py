from fastapi import APIRouter, Request
from renderable_core.models import HealthCheckResponse

from . import containers, devices, jobs, tasks
from controllers import api


router = APIRouter()

@router.get('/', response_model = HealthCheckResponse, response_model_exclude_unset = True)
def api_health_check(request: Request):
  return api.health_check(request.app.state.context)

router.include_router(containers.router, prefix = '/containers')
router.include_router(devices.router, prefix = '/devices')
router.include_router(jobs.router, prefix = '/jobs')
router.include_router(tasks.router, prefix = '/tasks')
