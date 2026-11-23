from fastapi import APIRouter

from app.core.configure import settings
from app.schemas.common import HealthResponse


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="ok",
        project=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )