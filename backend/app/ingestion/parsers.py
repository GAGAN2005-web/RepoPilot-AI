from pathlib import Path


LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
    ".cpp": "cpp",
    ".c": "c",
    ".h": "c",
    ".cs": "csharp",
    ".go": "go",
    ".rs": "rust",
    ".php": "php",
    ".rb": "ruby",
    ".swift": "swift",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".html": "html",
    ".css": "css",
    ".scss": "scss",
    ".sql": "sql",
    ".md": "markdown",
    ".txt": "text",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".xml": "xml",
}


def get_file_extension(path: str) -> str:
    return Path(path).suffix.lower()


def get_language(path: str) -> str:
    extension = get_file_extension(path)

    return LANGUAGE_MAP.get(
        extension,
        "text",
    )


def parse_file(
    path: str,
    content: str,
) -> dict:
    return {
        "path": path,
        "extension": get_file_extension(path),
        "language": get_language(path),
        "content": content,
    }