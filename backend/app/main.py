from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.repositories import router as repository_router
from app.core.configure import settings
from app.api.routes.chat import router as chat_router


app = FastAPI(
    title=settings.app_name,
    description="AI-powered GitHub repository understanding and engineering assistant",
    version=settings.app_version,
)

app.include_router(chat_router)
app.include_router(health_router)
app.include_router(repository_router)