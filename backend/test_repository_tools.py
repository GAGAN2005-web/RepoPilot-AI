import asyncio

from app.tools.repository_tools import (
    search_repository,
    get_file,
    get_repository_info,
)


async def main():

    print("=" * 60)
    print("TEST 1: SEARCH REPOSITORY")
    print("=" * 60)

    result = await search_repository(
        repository_id=1,
        query="Where is the machine learning model loaded?",
        top_k=3,
    )

    for item in result["results"]:
        print("\nPath:", item["path"])
        print("Chunk:", item["chunk_index"])
        print("Distance:", item["distance"])
        print("Content:")
        print(item["content"][:300])

    print("\n")
    print("=" * 60)
    print("TEST 2: GET FILE")
    print("=" * 60)

    result = await get_file(
        owner="GAGAN2005-web",
        repository="SmartLogix-AI",
        path="app.py",
        branch="main",
    )

    print("Path:", result["path"])
    print("Content length:", len(result["content"]))
    print(result["content"][:300])

    print("\n")
    print("=" * 60)
    print("TEST 3: REPOSITORY INFO")
    print("=" * 60)

    result = await get_repository_info(
        owner="GAGAN2005-web",
        repository="SmartLogix-AI",
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())