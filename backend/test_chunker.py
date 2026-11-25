import asyncio

from app.services.github_service import GitHubService
from app.ingestion.chunker import chunk_python_code


async def main():
    github_service = GitHubService()

    content = await github_service.get_file_content(
        owner="GAGAN2005-web",
        repository="SmartLogix-AI",
        path="app.py",
        branch="main",
    )

    chunks = chunk_python_code(content)

    print(f"Total chunks: {len(chunks)}")
    print("=" * 60)

    for index, chunk in enumerate(chunks):
        print(f"\nChunk {index}")
        print("-" * 60)
        print(chunk)


if __name__ == "__main__":
    asyncio.run(main())