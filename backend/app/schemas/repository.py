from urllib.parse import urlparse

from pydantic import BaseModel, field_validator


class RepositoryRequest(BaseModel):
    url: str

    @field_validator("url")
    @classmethod
    def validate_github_url(cls, value: str) -> str:
        value = value.strip()

        parsed = urlparse(value)

        if parsed.scheme != "https":
            raise ValueError("Repository URL must use HTTPS")

        if parsed.netloc.lower() != "github.com":
            raise ValueError("URL must be a GitHub repository URL")

        parts = [part for part in parsed.path.split("/") if part]

        if len(parts) != 2:
            raise ValueError(
                "URL must be in the format https://github.com/owner/repository"
            )

        return value.rstrip("/")


class RepositoryInfo(BaseModel):
    id:int
    owner: str
    name: str
    url: str
    description: str | None = None
    language: str | None = None
    stars: int
    forks: int
    default_branch: str