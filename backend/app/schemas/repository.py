from pydantic import BaseModel, field_validator
from urllib.parse import urlparse


class RepositoryRequest(BaseModel):
    url: str

    @field_validator("url")
    @classmethod
    def validate_github_url(cls, value: str) -> str:
        value = value.strip()

        parsed_url = urlparse(value)

        if parsed_url.scheme != "https":
            raise ValueError("GitHub URL must use HTTPS")

        if parsed_url.netloc.lower() != "github.com":
            raise ValueError("URL must be a GitHub repository URL")

        parts = [part for part in parsed_url.path.split("/") if part]

        if len(parts) != 2:
            raise ValueError(
                "URL must be in the format https://github.com/owner/repository"
            )

        return value.rstrip("/")


class RepositoryInfo(BaseModel):
    owner: str
    name: str
    url: str
    description: str | None = None
    language: str | None = None
    stars: int
    forks: int
    default_branch: str