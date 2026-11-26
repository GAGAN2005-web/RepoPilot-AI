from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.repository import RepositoryRequest, RepositoryInfo
from app.services.repository_service import RepositoryService


router = APIRouter(prefix="/repositories", tags=["Repositories"])

repository_service = RepositoryService()


@router.post("", response_model=RepositoryInfo)
async def get_repository(
    request: RepositoryRequest,
    db: Session = Depends(get_db),
):
    parts = request.url.rstrip("/").split("/")

    owner = parts[-2]
    name = parts[-1]

    # GitHub URLs may end with .git
    if name.endswith(".git"):
        name = name[:-4]

    # Normalize the URL so the same repository is not stored twice
    normalized_url = f"https://github.com/{owner}/{name}"

    try:
        repository = await repository_service.register_repository(
            db=db,
            owner=owner,
            repository=name,
            url=normalized_url,
        )

        # Index the repository only when it has not already been completed.
        
        await repository_service.index_repository(
            db=db,
            repository=repository,
        )

    except ValueError as error:
        message = str(error)

        if "not found" in message.lower():
            raise HTTPException(
                status_code=404,
                detail=message,
            ) from error

        if "rate limit" in message.lower():
            raise HTTPException(
                status_code=429,
                detail=message,
            ) from error

        raise HTTPException(
            status_code=502,
            detail=message,
        ) from error

    return RepositoryInfo(
        id=repository.id,
        owner=repository.owner,
        name=repository.name,
        url=repository.url,
        description=repository.description,
        language=repository.language,
        stars=repository.stars,
        forks=repository.forks,
        default_branch=repository.default_branch,
    )