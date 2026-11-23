from app.ingestion.file_filter import should_include_file
from app.services.github_service import GitHubService


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