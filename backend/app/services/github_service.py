import httpx

from app.core.configure import settings


class GitHubService:
    BASE_URL = "https://api.github.com"

    def __init__(self):
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        if settings.github_token:
            self.headers["Authorization"] = f"Bearer {settings.github_token}"

    async def get_repository(
        self,
        owner: str,
        repository: str,
    ) -> dict:
        url = f"{self.BASE_URL}/repos/{owner}/{repository}"

        try:
            async with httpx.AsyncClient(
                timeout=10.0,
                headers=self.headers,
            ) as client:
                response = await client.get(url)

        except httpx.TimeoutException as error:
            raise ValueError(
                "GitHub API request timed out"
            ) from error

        except httpx.RequestError as error:
            raise ValueError(
                "Unable to connect to GitHub API"
            ) from error

        if response.status_code == 404:
            raise ValueError("GitHub repository not found")

        if response.status_code == 403:
            remaining = response.headers.get("X-RateLimit-Remaining")

            if remaining == "0":
                raise ValueError("GitHub API rate limit exceeded")

            raise ValueError("GitHub API access denied")

        if response.status_code != 200:
            raise ValueError(
                f"GitHub API request failed with status {response.status_code}"
            )

        return response.json()

    async def get_repository_tree(
        self,
        owner: str,
        repository: str,
        branch: str,
    ) -> list[dict]:
        url = (
            f"{self.BASE_URL}/repos/"
            f"{owner}/{repository}/git/trees/{branch}"
        )

        params = {
            "recursive": "1",
        }

        try:
            async with httpx.AsyncClient(
                timeout=15.0,
                headers=self.headers,
            ) as client:
                response = await client.get(
                    url,
                    params=params,
                )

        except httpx.TimeoutException as error:
            raise ValueError(
                "GitHub repository tree request timed out"
            ) from error

        except httpx.RequestError as error:
            raise ValueError(
                "Unable to connect to GitHub API"
            ) from error

        if response.status_code == 404:
            raise ValueError(
                "GitHub repository tree not found"
            )

        if response.status_code == 403:
            remaining = response.headers.get("X-RateLimit-Remaining")

            if remaining == "0":
                raise ValueError(
                    "GitHub API rate limit exceeded"
                )

            raise ValueError(
                "GitHub API access denied"
            )

        if response.status_code != 200:
            raise ValueError(
                f"GitHub tree API request failed with status "
                f"{response.status_code}"
            )

        data = response.json()

        return data.get("tree", [])