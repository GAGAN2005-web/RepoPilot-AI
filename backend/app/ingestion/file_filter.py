from pathlib import Path


ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".h",
    ".cs",
    ".go",
    ".rs",
    ".php",
    ".rb",
    ".swift",
    ".kt",
    ".kts",
    ".html",
    ".css",
    ".scss",
    ".sql",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".xml",
    ".env.example",
}


IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".idea",
    ".vscode",
    "dist",
    "build",
    "coverage",
}


IGNORED_FILES = {
    ".gitignore",
}


def should_include_file(path: str) -> bool:
    path_obj = Path(path)

    if path_obj.name in IGNORED_FILES:
        return False

    for part in path_obj.parts:
        if part in IGNORED_DIRECTORIES:
            return False

    if path_obj.name == "":
        return False

    if path_obj.suffix.lower() in ALLOWED_EXTENSIONS:
        return True

    return False