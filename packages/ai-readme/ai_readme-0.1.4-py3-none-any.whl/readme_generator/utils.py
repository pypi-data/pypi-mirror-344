import os

IGNORED_DIRS = {
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "__pycache__",
    ".idea",
    ".vscode",
    ".ipynb_checkpoints",
    "build",
    "dist",
    "*.egg-info",
}

ALLOWED_EXTENSIONS = (
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".ini",
    ".cfg",
    ".html",
    ".css",
)


def read_project_files(base_dir=".", max_chars=10000):
    contents = []
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not any(ignored in d for ignored in IGNORED_DIRS)]
        for file in files:
            if file.endswith(ALLOWED_EXTENSIONS) and "README" not in file.upper():
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        text = f.read()
                        contents.append(f"File: {path}\n{text[:max_chars]}\n\n")
                except Exception as e:
                    print(f"⚠️ Failed to read {path}: {e}")
    return "\n".join(contents)
