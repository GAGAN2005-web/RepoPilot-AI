from app.services.github_service import GitHubService
from app.services.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore


github_service = GitHubService()
embedding_service = EmbeddingService()
vector_store = VectorStore()


async def search_repository(
    repository_id: int,
    query: str,
    top_k: int = 5,
) -> dict:
    """Search indexed repository code using semantic similarity."""

    query_embedding = embedding_service.create_embedding(query)

    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=top_k,
        repository_id=repository_id,
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    matches = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        matches.append(
            {
                "path": metadata.get("path"),
                "language": metadata.get("language"),
                "chunk_index": metadata.get("chunk_index"),
                "distance": round(distance, 4),
                "content": document,
            }
        )

    return {
        "query": query,
        "results": matches,
    }


async def get_file(
    owner: str,
    repository: str,
    path: str,
    branch: str,
) -> dict:
    """Retrieve the complete content of a repository file."""

    content = await github_service.get_file_content(
        owner=owner,
        repository=repository,
        path=path,
        branch=branch,
    )

    return {
        "path": path,
        "content": content,
    }


async def get_repository_info(
    owner: str,
    repository: str,
) -> dict:
    """Retrieve repository metadata from GitHub."""

    info = await github_service.get_repository(
        owner=owner,
        repository=repository,
    )

    return {
        "owner": info.get("owner", {}).get("login"),
        "name": info.get("name"),
        "url": info.get("html_url"),
        "description": info.get("description"),
        "language": info.get("language"),
        "stars": info.get("stargazers_count"),
        "forks": info.get("forks_count"),
        "default_branch": info.get("default_branch"),
    }