from app.ingestion.file_filter import should_include_file
from app.services.github_service import GitHubService
from app.ingestion.parsers import parse_file
from app.ingestion.chunker import chunk_file


class IngestionService:
    def __init__(self):
        self.github_service = GitHubService()

    async def get_processable_files(
        self,
        owner: str,
        repository: str,
        branch: str,
    ) -> list[dict]:
        tree = await self.github_service.get_repository_tree(
            owner=owner,
            repository=repository,
            branch=branch,
        )

        processable_files = []

        for item in tree:
            if item.get("type") != "blob":
                continue

            path = item.get("path", "")

            if should_include_file(path):
                processable_files.append(item)

        return processable_files

    async def get_file_contents(
        self,
        owner: str,
        repository: str,
        branch: str,
    ) -> list[dict]:
        files = await self.get_processable_files(
            owner=owner,
            repository=repository,
            branch=branch,
        )

        processed_files = []

        for file in files:
            path = file["path"]

            content = await self.github_service.get_file_content(
                owner=owner,
                repository=repository,
                path=path,
                branch=branch,
            )

            processed_files.append(
                parse_file(
                    path=path,
                    content=content,
                )
            )

        return processed_files

    async def get_repository_chunks(
        self,
        owner: str,
        repository: str,
        branch: str,
    ) -> list[dict]:
        files = await self.get_file_contents(
            owner=owner,
            repository=repository,
            branch=branch,
        )

        all_chunks = []

        for file in files:
            chunks = chunk_file(file)

            all_chunks.extend(chunks)

        return all_chunks