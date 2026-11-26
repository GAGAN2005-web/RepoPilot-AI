from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.repositories import router as repository_router
from app.api.routes.chat import router as chat_router
from app.api.routes.conversations import router as conversations_router
from app.api.routes.agent_chat import router as agent_chat_router
from app.core.configure import settings


app = FastAPI(
    title=settings.app_name,
    description="AI-powered GitHub repository understanding and engineering assistant",
    version=settings.app_version,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "repopilot-pg3j6esq7-gagan-bhati-s-projects.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router)
app.include_router(health_router)
app.include_router(repository_router)
app.include_router(conversations_router)
app.include_router(agent_chat_router)