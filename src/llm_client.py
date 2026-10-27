import os
import pathlib
import json
import subprocess


def load_config(config_path: str = "config.yaml") -> dict:
    """
    Loads config from file if available, otherwise from environment variables.
    File is used locally, env vars are used in CI.
    """
    env_path = pathlib.Path(".env")
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

    if pathlib.Path(config_path).exists():
        import yaml
        with open(config_path, "r") as f:
            return yaml.safe_load(f)

    # CI environment — read from environment variables
    return {"groq": {
        "api_key": os.environ.get("GROQ_API_KEY", ""),
        "model": os.environ.get("GROQ_MODEL", "openai/gpt-oss-20b"),
    }}


def build_prompt(context: dict) -> str:
    """
    Converts the repo context dictionary into a text prompt
    that the LLM can understand and act on.
    """
    if context["existing_dockerfile"]:
        mode = f"""
An existing Dockerfile was found. AUDIT it instead of generating a new one.
Identify specific problems with it and suggest fixes.

EXISTING DOCKERFILE:
{context["existing_dockerfile"]}
"""
    else:
        mode = "No Dockerfile exists. GENERATE a new one from scratch."

    prompt = f"""
You are a senior Docker engineer helping automate containerization.

PROJECT DETAILS:
- Language: {context.get("language", "unknown")}
- Dependency file: {context.get("dependency_file", "none")}
- Dependencies: {context.get("dependencies", "none")}
- Entry point: {context.get("entry_point", "unknown")}
- Port hints found in: {context.get("port_hints", [])}

TASK:
{mode}

REQUIREMENTS:
- Use a multi-stage build (separate build and runtime stages)
- Pin base image to a specific version, never use 'latest'
- Run the app as a non-root user called 'appuser'
- Only copy what is needed into the final image
- Set correct EXPOSE port based on the project

CRITICAL: Respond ONLY with a valid JSON object.
- In copy_commands, always include a space before the destination dot: "COPY file ." not "COPY file."
- No markdown, no explanation, no code blocks. Just raw JSON.

Use exactly this structure:
{{
  "base_image": "python:3.11-slim",
  "build_stage_image": "python:3.11",
  "expose_port": 5000,
  "env_vars": {{"PYTHONDONTWRITEBYTECODE": "1", "PYTHONUNBUFFERED": "1"}},
  "install_commands": ["pip install --no-cache-dir -r requirements.txt"],
  "copy_commands": ["COPY requirements.txt .", "COPY . ."],
  "entrypoint": ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"],
  "notes": "Flask app detected. Gunicorn used as production WSGI server."
}}
"""
    return prompt.strip()


def mock_model_response(context: dict) -> dict:
    """
    Returns a hardcoded spec when the hosted model is unavailable.
    Used for local development and testing.
    """
    language = context.get("language", "python")

    templates = {
        "python": {
            "base_image": "python:3.11-slim",
            "build_stage_image": "python:3.11",
            "expose_port": 5000,
            "env_vars": {
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONUNBUFFERED": "1"
            },
            "install_commands": ["pip install --no-cache-dir -r requirements.txt"],
            "copy_commands": ["COPY requirements.txt .", "COPY . ."],
            "entrypoint": ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"],
            "notes": "MOCK: Flask/Python app detected."
        },
        "nodejs": {
            "base_image": "node:20-alpine",
            "build_stage_image": "node:20",
            "expose_port": 3000,
            "env_vars": {"NODE_ENV": "production"},
            "install_commands": ["npm ci --only=production"],
            "copy_commands": ["COPY package*.json .", "COPY . ."],
            "entrypoint": ["node", "index.js"],
            "notes": "MOCK: Node.js app detected."
        }
    }

    return templates.get(language, templates["python"])


def call_groq(prompt: str, config: dict, context: dict = None) -> dict:
    """
    Sends the prompt to the hosted Groq model.
    Returns the parsed JSON response.
    """
    try:
        api_key = config["groq"]["api_key"]
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not configured")
        body = json.dumps({
            "model": config["groq"]["model"],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "response_format": {"type": "json_object"},
        }).encode()
        response = subprocess.run([
            "curl", "--fail-with-body", "--silent", "--show-error", "--max-time", "60",
            "https://api.groq.com/openai/v1/chat/completions",
            "-H", f"Authorization: Bearer {api_key}",
            "-H", "Content-Type: application/json",
            "--data", body,
        ], capture_output=True, text=True, check=True)
        raw_text = json.loads(response.stdout)["choices"][0]["message"]["content"]
        return json.loads(raw_text)
    except Exception as e:
        print(f"Groq unavailable ({type(e).__name__}). Using mock response.")
        return mock_model_response(context or {})


if __name__ == "__main__":
    from context_collector import collect_context

    config = load_config()
    context = collect_context("sample_repos/flask-app")
    prompt = build_prompt(context)

    print("=== PROMPT BEING SENT TO NOVA ===")
    print(prompt)
    print("\n=== CALLING GROQ ===")

    result = call_groq(prompt, config, context)

    print("\n=== NOVA'S RESPONSE ===")
    print(json.dumps(result, indent=2))
