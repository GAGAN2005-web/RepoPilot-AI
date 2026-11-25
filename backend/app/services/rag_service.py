from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.rag.vector_store import VectorStore
from app.rag.context_builder import build_context
from app.rag.prompt_builder import build_rag_prompt


class RAGService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
        self.llm_service = LLMService()

    async def answer_question(
        self,
        question: str,
        repository_id: int,
        top_k: int = 5,
    ) -> dict:

        # 1. Convert question into an embedding
        query_embedding = self.embedding_service.create_embedding(
            question
        )

        # 2. Retrieve relevant repository chunks
        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            repository_id=repository_id,
        )

        # 3. Build context
        context = build_context(results)

        if not context:
            return {
                "answer": (
                    "I could not find relevant information in "
                    "the indexed repository."
                ),
                "sources": [],
            }

        # 4. Build RAG prompt
        prompt = build_rag_prompt(
            question=question,
            context=context,
        )

        # 5. Generate answer using Ollama
        answer = await self.llm_service.generate(prompt)

        # 6. Extract source information
        metadatas = results.get("metadatas", [[]])[0]

        sources = []

        for metadata in metadatas:
            sources.append(
                {
                    "path": metadata.get("path"),
                    "language": metadata.get("language"),
                    "chunk_index": metadata.get("chunk_index"),
                }
            )

        return {
            "answer": answer,
            "sources": sources,
        }