import asyncio

from app.services.agent_service import AgentService


async def main():
    agent = AgentService()

    tests = [
        {
            "question": "Where is the machine learning model loaded?",
            "repository_id": 1,
            "owner": "GAGAN2005-web",
            "repository": "SmartLogix-AI",
            "branch": "main",
        },
        {
            "question": "Show me the complete app.py file.",
            "repository_id": 1,
            "owner": "GAGAN2005-web",
            "repository": "SmartLogix-AI",
            "branch": "main",
        },
        {
            "question": "How many stars does this repository have?",
            "repository_id": 1,
            "owner": "GAGAN2005-web",
            "repository": "SmartLogix-AI",
            "branch": "main",
        },
    ]

    for index, test in enumerate(tests, start=1):
        print("=" * 60)
        print(f"TEST {index}")
        print("=" * 60)

        print("QUESTION:")
        print(test["question"])

        result = await agent.run(
            question=test["question"],
            repository_id=test["repository_id"],
            owner=test["owner"],
            repository=test["repository"],
            branch=test["branch"],
        )

        print("\nTOOL USED:")
        print(result["tool"])

        print("\nFINAL ANSWER:")
        print(result["answer"])

        print("\n")


if __name__ == "__main__":
    asyncio.run(main())