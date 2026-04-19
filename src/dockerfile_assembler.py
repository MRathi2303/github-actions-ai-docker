import pathlib


def assemble_dockerfile(spec: dict, output_path: str = "Dockerfile.generated") -> str:
    """
    Takes the JSON spec from Claude and assembles
    it into an actual Dockerfile string.
    """
    lines = []

    # --- Build stage ---
    lines.append(f"FROM {spec['build_stage_image']} AS builder")
    lines.append("WORKDIR /app")
    lines.append("")

    # Copy and install dependencies
    for cmd in spec["copy_commands"]:
        if "requirements" in cmd or "package.json" in cmd:
            fixed = cmd.replace("txt.", "txt .").replace("json.", "json .")
            lines.append(fixed)

    for cmd in spec["install_commands"]:
        lines.append(f"RUN {cmd}")

    lines.append("")

    # --- Runtime stage ---
    lines.append(f"FROM {spec['base_image']}")
    lines.append("WORKDIR /app")
    lines.append("")

    # Environment variables
    for key, value in spec["env_vars"].items():
        lines.append(f"ENV {key}={value}")

    lines.append("")

    # Copy built artifacts from builder
    lines.append("COPY --from=builder /app /app")
    lines.append("")

    # Create and switch to non-root user
    lines.append("RUN useradd -m appuser")
    lines.append("USER appuser")
    lines.append("")

    # Expose port
    lines.append(f"EXPOSE {spec['expose_port']}")
    lines.append("")

    # Entrypoint
    entrypoint = json_list_to_dockerfile(spec["entrypoint"])
    lines.append(f"CMD {entrypoint}")

    # Join all lines into one string
    dockerfile_content = "\n".join(lines)

    # Write to file
    output = pathlib.Path(output_path)
    output.write_text(dockerfile_content)

    print(f"Dockerfile written to: {output.resolve()}")
    return dockerfile_content


def json_list_to_dockerfile(items: list) -> str:
    """
    Converts ["gunicorn", "-w", "4"] 
    into     ["gunicorn", "-w", "4"]  ← Dockerfile exec format
    """
    formatted = ', '.join(f'"{item}"' for item in items)
    return f"[{formatted}]"


if __name__ == "__main__":
    # Test with the exact response Claude gave us
    sample_spec = {
        "base_image": "python:3.11-slim",
        "build_stage_image": "python:3.11",
        "expose_port": 5000,
        "env_vars": {
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONUNBUFFERED": "1"
        },
        "install_commands": [
            "pip install --no-cache-dir -r requirements.txt"
        ],
        "copy_commands": [
            "COPY requirements.txt .",
            "COPY . ."
        ],
        "entrypoint": ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"],
        "notes": "Flask app detected. Gunicorn used as production WSGI server."
    }

    result = assemble_dockerfile(sample_spec)
    print("\n=== GENERATED DOCKERFILE ===")
    print(result)