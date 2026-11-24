from typing import Any


DEFAULT_CHUNK_SIZE = 1200
DEFAULT_CHUNK_OVERLAP = 200


def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[str]:
    if not text.strip():
        return []

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size"
        )

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(
            start + chunk_size,
            text_length,
        )

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = end - chunk_overlap

    return chunks


def chunk_file(
    file: dict[str, Any],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[dict[str, Any]]:
    content = file.get("content", "")

    chunks = chunk_text(
        text=content,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunked_files = []

    for index, chunk in enumerate(chunks):
        chunked_files.append(
            {
                "path": file["path"],
                "extension": file["extension"],
                "language": file["language"],
                "chunk_index": index,
                "content": chunk,
            }
        )

    return chunked_files