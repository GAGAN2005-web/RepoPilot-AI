def build_context(results: dict) -> str:
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not documents:
        return ""

    context_parts = []

    for document, metadata in zip(documents, metadatas):
        path = metadata.get("path", "unknown")
        chunk_index = metadata.get("chunk_index", "unknown")
        language = metadata.get("language", "unknown")

        context_parts.append(
            f"--- File: {path} | "
            f"Chunk: {chunk_index} | "
            f"Language: {language} ---\n\n"
            f"{document}"
        )

    return "\n\n".join(context_parts)