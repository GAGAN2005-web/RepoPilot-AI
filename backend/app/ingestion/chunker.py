from typing import Any
import ast


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


def chunk_python_code(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[str]:
    if not text.strip():
        return []

    try:
        tree = ast.parse(text)
    except SyntaxError:
        return chunk_text(
            text=text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    lines = text.splitlines(keepends=True)

    boundaries = []

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start_line = node.lineno - 1
            end_line = node.end_lineno

            boundaries.append((start_line, end_line))

    if not boundaries:
        return chunk_text(
            text=text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    chunks = []

    first_definition_line = boundaries[0][0]

    if first_definition_line > 0:
        prefix = "".join(lines[:first_definition_line]).strip()

        if prefix:
            chunks.extend(
                chunk_text(
                    text=prefix,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                )
            )

    for start_line, end_line in boundaries:
        block = "".join(lines[start_line:end_line]).strip()

        if not block:
            continue

        if len(block) <= chunk_size:
            chunks.append(block)
        else:
            chunks.extend(
                chunk_text(
                    text=block,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                )
            )

    return chunks


def chunk_file(
    file: dict[str, Any],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[dict[str, Any]]:
    content = file.get("content", "")
    extension = file.get("extension", "")

    if extension == ".py":
        chunks = chunk_python_code(
            text=content,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
    else:
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