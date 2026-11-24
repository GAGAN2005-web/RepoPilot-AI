from sqlalchemy.orm import Session

from app.services.ingestion_service import IngestionService

from app.db.repositories import (
    create_repository,
    get_repository_by_url,
    update_indexing_status,
)

from app.services.github_service import GitHubService


class RepositoryService:
    def __init__(self):
        self.github_service = GitHubService()
        self.ingestion_service = IngestionService()

    async def register_repository(
        self,
        db: Session,
        owner: str,
        repository: str,
        url: str,
    ):
        existing_repository = get_repository_by_url(
            db=db,
            url=url,
        )

        if existing_repository:
            return existing_repository

        repository_data = await self.github_service.get_repository(
            owner=owner,
            repository=repository,
        )

        return create_repository(
            db=db,
            owner=repository_data.owner,
            name=repository_data.name,
            url=repository_data.url,
            description=repository_data.description,
            language=repository_data.language,
            stars=repository_data.stars,
            forks=repository_data.forks,
            default_branch=repository_data.default_branch,
        )

    def mark_processing(
        self,
        db: Session,
        repository,
    ):
        return update_indexing_status(
            db=db,
            repository=repository,
            status="processing",
        )

    def mark_completed(
        self,
        db: Session,
        repository,
    ):
        return update_indexing_status(
            db=db,
            repository=repository,
            status="completed",
        )

    def mark_failed(
        self,
        db: Session,
        repository,
    ):
        return update_indexing_status(
            db=db,
            repository=repository,
            status="failed",
        )

    async def index_repository(
        self,
        db: Session,
        repository,
    ):
        self.mark_processing(
            db=db,
            repository=repository,
        )

        try:
            chunks = await self.ingestion_service.get_repository_chunks(
                owner=repository.owner,
                repository=repository.name,
                branch=repository.default_branch,
            )

            self.mark_completed(
                db=db,
                repository=repository,
            )

            return chunks

        except Exception:
            self.mark_failed(
                db=db,
                repository=repository,
            )
            raise