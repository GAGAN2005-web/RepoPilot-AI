import asyncio

from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.rag.vector_store import VectorStore
from app.rag.context_builder import build_context
from app.rag.prompt_builder import build_rag_prompt


async def main():
    question = "Where is the machine learning model loaded?"

    # 1. Create embedding for the question
    embedding_service = EmbeddingService()

    query_embedding = embedding_service.create_embedding(question)

    # 2. Retrieve relevant repository chunks
    vector_store = VectorStore()

    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=3,
        repository_id=1,
    )

    # 3. Build context from retrieved chunks
    context = build_context(results)

    print("\nRetrieved Context:")
    print("=" * 80)
    print(context)

    # 4. Build RAG prompt
    prompt = build_rag_prompt(
        question=question,
        context=context,
    )

    # 5. Send prompt to Ollama
    llm_service = LLMService()

    answer = await llm_service.generate(prompt)

    # 6. Display answer
    print("\n\nAI Answer:")
    print("=" * 80)
    print(answer)


if __name__ == "__main__":
    asyncio.run(main())