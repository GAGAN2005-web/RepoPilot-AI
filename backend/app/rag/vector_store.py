import chromadb


class VectorStore:
    def __init__(
        self,
        persist_directory: str = "./chroma_db",
        collection_name: str = "repository_chunks",
    ):
        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def delete_repository(self, repository_id: int)-> None:
        self.collection.delete(
            where={"repository_id":repository_id}
        )

    def add_chunks(
        self,
        chunks: list[dict],
        embeddings: list[list[float]],
        repository_id: int,
    ) -> None:

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks must match number of embeddings."
            )

        if not chunks:
            return

        ids = [
            f"{repository_id}:{chunk['path']}:{chunk['chunk_index']}"
            for chunk in chunks
        ]

        documents = [
            chunk["content"]
            for chunk in chunks
        ]

        metadatas = [
            {
                "repository_id": repository_id,
                "path": chunk["path"],
                "extension": chunk["extension"],
                "language": chunk["language"],
                "chunk_index": chunk["chunk_index"],
            }
            for chunk in chunks
        ]

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding,
        top_k=5,
        repository_id: int | None = None,
    ):
        where = None

        if repository_id is not None:
            where = {
                "repository_id": repository_id
            }

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )