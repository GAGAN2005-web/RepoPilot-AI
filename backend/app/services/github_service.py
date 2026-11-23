import httpx


class GitHubService:
    BASE_URL = "https://api.github.com"

    async def get_repository(self, owner: str, repository: str) -> dict:
        url = f"{self.BASE_URL}/repos/{owner}/{repository}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code == 404:
            raise ValueError("GitHub repository not found")

        if response.status_code == 403:
            raise ValueError("GitHub API rate limit exceeded or access denied")

        if response.status_code != 200:
            raise ValueError(
                f"GitHub API request failed with status {response.status_code}"
            )

        return response.json()