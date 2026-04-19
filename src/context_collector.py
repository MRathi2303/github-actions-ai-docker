import os
import pathlib
import json

def collect_context(repo_path:str) -> dict:
    """
    Reads a repository and returns a dictonary of everything the AI needs to know about the project.
    """
    root = pathlib.Path(repo_path)
    context = {}

    #stage - 1 - language detection
    language_signals = {
        "requirements.txt": "python",
        "package.json": "javascript",
        "pom.xml": "java",
        "build.gradle": "java",
        "Cargo.toml": "rust",
        "go.mod": "go",
        "Gemfile": "ruby",
        "pyproject.toml": "python",
        "setup.py": "python",
        "composer.json": "php",
        "CMakeLists.txt": "cpp",
    }

    for filename, language in language_signals.items():
        if (root / filename).exists():
            context["language"] = language
            context["dependency_file"] = filename
            break
    
    # ---stage 2 - read the actual dependency file content
    if "dependency_file" in context:
        dep_path = root / context["dependency_file"]
        context["dependencies"] = dep_path.read_text()[:2000] 

    # ---stage 3: Find the entry point ----
    entry_points = [
        "app.py", "main.py", "run.py",
        "index.js", "server.js", "app.js",
        "src/main/java",
        "main.go",
        "src/main/cpp",
        "src/main/rust",
        "src/main/php",
        "src/main/ruby",
    ]

    for entry in entry_points:
        if (root / entry).exists():
            context["entry_point"] = entry
            break

    # --- Stage 4: Detect port from source code ---
    port_keywords = ["PORT=", "port=", "listen(", ".listen(", "EXPOSE"]
    ports_found = []

    for py_file in root.rglob("*"):
        if py_file.suffix in [".py", ".js", ".java", ".go", ".cpp", ".rs", ".php", ".rb"]:
            try:
                content = py_file.read_text(errors="ignore")
                for keyword in port_keywords:
                    if keyword in content:
                        ports_found.append(py_file.name)
                        break
            except Exception:
                pass
    context["ports_hints"] = ports_found

    # --- Stage 5: check if a Dockerfile exists ---
    dockerfile_path = root / "Dockerfile"

    if dockerfile_path.exists():
        context["existing_dockerfile"] = dockerfile_path.read_text()
    else:
        context["existing_dockerfile"] = None
    return context

# temporary test — we'll remove this later
if __name__ == "__main__":
    result = collect_context("sample_repos/flask-app")
    print(json.dumps(result, indent=2))