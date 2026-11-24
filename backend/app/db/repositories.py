from sqlalchemy.orm import Session

from app.db.models import Repository


def create_repository(
    db: Session,
    owner: str,
    name: str,
    url: str,
    description: str | None,
    language: str | None,
    stars: int,
    forks: int,
    default_branch: str,
) -> Repository:
    repository = Repository(
        owner=owner,
        name=name,
        url=url,
        description=description,
        language=language,
        stars=stars,
        forks=forks,
        default_branch=default_branch,
        indexing_status="pending",
    )

    db.add(repository)
    db.commit()
    db.refresh(repository)

    return repository


def get_repository_by_url(
    db: Session,
    url: str,
) -> Repository | None:
    return (
        db.query(Repository)
        .filter(Repository.url == url)
        .first()
    )


def update_indexing_status(
    db: Session,
    repository: Repository,
    status: str,
) -> Repository:
    repository.indexing_status = status

    db.commit()
    db.refresh(repository)

    return repository