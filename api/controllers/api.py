import renderable_core
from renderable_core.models import Status, HealthCheckResponse


def health_check(context):
  return HealthCheckResponse(
    version = renderable_core.__version__,
    status = Status.online)
