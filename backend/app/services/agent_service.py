import json

from app.services.llm_service import LLMService
from app.tools.repository_tools import (
    search_repository,
    get_file,
    get_repository_info,
)


class AgentService:
    def __init__(self):
        self.llm_service = LLMService()

    async def decide_tool(self, question: str) -> dict:
        prompt = f"""
You are RepoPilot AI, a GitHub repository analysis assistant.

Choose the best tool for the user's question.

Available tools:

1. search_repository
Use for questions about code, implementation, functions,
classes, algorithms, or where something is implemented.

2. get_file
Use when the user explicitly asks for the complete contents
of a specific file.

3. get_repository_info
Use for repository metadata such as description, language,
stars, forks, URL, or default branch.

Return ONLY valid JSON.

Examples:

For search:
{{
    "tool": "search_repository",
    "query": "machine learning model loading"
}}

For file:
{{
    "tool": "get_file",
    "path": "app.py"
}}

For repository information:
{{
    "tool": "get_repository_info"
}}

User question:
{question}
""".strip()

        response = await self.llm_service.generate(prompt)

        try:
            cleaned_response = response.strip()

            # Handle JSON wrapped in Markdown code fences.
            if cleaned_response.startswith("```"):
                lines = cleaned_response.splitlines()

                # Remove the opening ```json / ```
                if lines and lines[0].startswith("```"):
                    lines = lines[1:]

                # Remove the closing ```
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]

                cleaned_response = "\n".join(lines).strip()

            return json.loads(cleaned_response)

        except json.JSONDecodeError:
            raise ValueError(
                f"Agent returned invalid JSON: {response}"
            )

    async def run(
        self,
        question: str,
        repository_id: int,
        owner: str,
        repository: str,
        branch: str,
    ) -> dict:

        decision = await self.decide_tool(question)

        tool_name = decision.get("tool")

        if tool_name == "search_repository":

            tool_result = await search_repository(
                repository_id=repository_id,
                query=decision.get("query", question),
                top_k=3,
            )

        elif tool_name == "get_file":

            path = decision.get("path")

            if not path:
                raise ValueError(
                    "Agent did not provide a file path."
                )

            tool_result = await get_file(
                owner=owner,
                repository=repository,
                path=path,
                branch=branch,
            )

        elif tool_name == "get_repository_info":

            tool_result = await get_repository_info(
                owner=owner,
                repository=repository,
            )

        else:
            raise ValueError(
                f"Unknown tool selected by agent: {tool_name}"
            )

        final_prompt = f"""
You are RepoPilot AI, a repository analysis assistant.

Answer the user's question using ONLY the tool result below.

STRICT RULES:

1. Use only facts explicitly present in the tool result.
2. Do not invent or assume anything.
3. Preserve exact function names, file names, class names,
   library names, and important code details from the tool result.
4. If code directly answers the question, explain what the code does.
5. Mention the relevant file path.
6. Do not add generic programming knowledge.
7. Keep the answer concise but complete.

USER QUESTION:
{question}

TOOL USED:
{tool_name}

TOOL RESULT:
{json.dumps(tool_result, indent=2)}

FINAL ANSWER:
""".strip()

        answer = await self.llm_service.generate(final_prompt)

        return {
            "answer": answer,
            "tool": tool_name,
            "decision": decision,
            "tool_result": tool_result,
        }