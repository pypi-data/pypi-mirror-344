import os

IGNORED_DIRS = {".git", "node_modules", "venv", "__pycache__"}

def read_project_files(base_dir=".", max_chars=3000):
    contents = []
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for file in files:
            if file.endswith((".py", ".js", ".md", ".txt")) and "README" not in file:
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        text = f.read()
                        contents.append(f"File: {path}\n{text[:max_chars]}\n\n")
                except Exception as e:
                    print(f"⚠️ Failed to read {path}: {e}")
    return "\n".join(contents)