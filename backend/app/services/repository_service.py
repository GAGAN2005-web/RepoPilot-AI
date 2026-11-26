from sqlalchemy.orm import Session

from app.services.ingestion_service import IngestionService
from app.services.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore

from app.db.repositories import (
    get_repository_by_url,
    update_indexing_status,
)

from app.db.models import Repository
from app.services.github_service import GitHubService


class RepositoryService:
    def __init__(self):
        self.github_service = GitHubService()
        self.ingestion_service = IngestionService()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

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

        repository = Repository(
            owner=repository_data["owner"]["login"],
            name=repository_data["name"],
            url=repository_data["html_url"],
            description=repository_data.get("description"),
            language=repository_data.get("language"),
            stars=repository_data.get("stargazers_count", 0),
            forks=repository_data.get("forks_count", 0),
            default_branch=repository_data["default_branch"],
            indexing_status="pending",
        )

        db.add(repository)
        db.commit()
        db.refresh(repository)

        return repository

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
            # Step 1: Get repository chunks
            chunks = await self.ingestion_service.get_repository_chunks(
                owner=repository.owner,
                repository=repository.name,
                branch=repository.default_branch,
            )

            # Step 2: Create embeddings
            texts = [chunk["content"] for chunk in chunks]

            embeddings = self.embedding_service.create_embeddings(
                texts
            )

            # Step 3: Remove any old vectors
            self.vector_store.delete_repository(
                repository_id=repository.id
            )

            # Step 4: Store chunks + embeddings in Chroma
            self.vector_store.add_chunks(
                chunks=chunks,
                embeddings=embeddings,
                repository_id=repository.id,
            )

            # Step 5: Mark indexing as completed
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