from fastapi import APIRouter

from . import devices, jobs, tasks


router = APIRouter()

router.include_router(devices.router, prefix = '/devices')
router.include_router(jobs.router, prefix = '/jobs')
router.include_router(tasks.router, prefix = '/tasks')
