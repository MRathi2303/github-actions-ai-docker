import boto3
import json
import yaml

def load_config(config_path: str = "config.yaml") -> dict:
    """Reads your personal config.yaml and return it as a dictionary."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
    

def build_prompt(context: dict) -> str:
    """
    Converts the repo context dictionary into a text prompt
    that LLM can understand and act on.
    """

    # Are we generating or auditing?
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
No markdown, no explanation, no code blocks. Just raw JSON.

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


def mock_bedrock_response(context: dict) -> dict:
    """
    Returns a hardcoded spec when Bedrock is unavailable.
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

def call_bedrock(prompt: str, config: dict, context: dict = None) -> dict:
    try:
        model_id = config["bedrock"]["model_id"]

        client = boto3.client(
            service_name="bedrock-runtime",
            region_name=config["bedrock"]["region"]
        )

        # Build request based on provider
        if "anthropic" in model_id:
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}]
            }
        else:
            # Amazon Nova format
            request_body = {
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ],
                "inferenceConfig": {
                    "max_new_tokens": 1000
                }
            }

        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body)
        )

        response_body = json.loads(response["body"].read())

        # Parse response based on provider
        if "anthropic" in model_id:
            raw_text = response_body["content"][0]["text"]
        else:
            # Amazon Nova format
            raw_text = response_body["output"]["message"]["content"][0]["text"]

        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            start = raw_text.find("{")
            end = raw_text.rfind("}") + 1
            if start != -1 and end != 0:
                return json.loads(raw_text[start:end])
            else:
                raise ValueError(f"Could not extract JSON from response: {raw_text}")

    except Exception as e:
        print(f"Bedrock unavailable ({type(e).__name__}). Using mock response.")
        return mock_bedrock_response(context or {})
    try:
        client = boto3.client(
            service_name="bedrock-runtime",
            region_name=config["bedrock"]["region"]
        )

        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        response = client.invoke_model(
            modelId=config["bedrock"]["model_id"],
            body=json.dumps(request_body)
        )

        response_body = json.loads(response["body"].read())
        raw_text = response_body["content"][0]["text"]

        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            start = raw_text.find("{")
            end = raw_text.rfind("}") + 1
            if start != -1 and end != 0:
                return json.loads(raw_text[start:end])
            else:
                raise ValueError(f"Could not extract JSON from response: {raw_text}")

    except Exception as e:
        print(f"Bedrock unavailable ({type(e).__name__}). Using mock response.")
        return mock_bedrock_response(context or {})
    """
    Sends the prompt to Claude via AWS Bedrock.
    Returns the parsed JSON response.
    """

    # Create a Bedrock client pointed at your region
    client = boto3.client(
        service_name="bedrock-runtime",
        region_name=config["bedrock"]["region"]
    )

    # This is the exact format Bedrock expects
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    # Make the API call
    response = client.invoke_model(
        modelId=config["bedrock"]["model_id"],
        body=json.dumps(request_body)
    )

    # The response body is a stream — we read and decode it
    response_body = json.loads(response["body"].read())

    # Claude's reply is inside content[0]["text"]
    raw_text = response_body["content"][0]["text"]

    # Parse the JSON Claude returned
    return json.loads(raw_text)


if __name__ == "__main__":
    from context_collector import collect_context

    config = load_config()
    context = collect_context("sample_repos/flask-app")
    prompt = build_prompt(context)

    print("=== PROMPT BEING SENT TO CLAUDE ===")
    print(prompt)
    print("\n=== CALLING BEDROCK ===")

    result = call_bedrock(prompt, config)

    print("\n=== CLAUDE'S RESPONSE ===")
    print(json.dumps(result, indent=2))