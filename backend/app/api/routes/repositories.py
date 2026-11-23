from fastapi import APIRouter, HTTPException

from app.schemas.repository import RepositoryRequest, RepositoryInfo
from app.services.github_service import GitHubService


router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
)


github_service = GitHubService()


@router.post("", response_model=RepositoryInfo)
async def get_repository(request: RepositoryRequest):
    parts = request.url.rstrip("/").split("/")

    owner = parts[-2]
    name = parts[-1]

    try:
        repository = await github_service.get_repository(
            owner=owner,
            repository=name,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    return RepositoryInfo(
        owner=repository["owner"]["login"],
        name=repository["name"],
        url=repository["html_url"],
        description=repository["description"],
        language=repository["language"],
        stars=repository["stargazers_count"],
        forks=repository["forks_count"],
        default_branch=repository["default_branch"],
    )