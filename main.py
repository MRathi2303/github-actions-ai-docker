import sys
import json
from src.context_collector import collect_context
from src.llm_client import load_config, build_prompt, call_bedrock
from src.dockerfile_assembler import assemble_dockerfile


def run(repo_path: str):
    print(f"\n--- Step 1: Analysing repo at {repo_path} ---")
    context = collect_context(repo_path)
    print(f"Detected: {context.get('language', 'unknown')} project")
    print(f"Entry point: {context.get('entry_point', 'unknown')}")
    print(f"Dependencies: {context.get('dependency_file', 'none found')}")

    print("\n--- Step 2: Building prompt and calling Claude ---")
    config = load_config()
    prompt = build_prompt(context)
    spec = call_bedrock(prompt, config, context)
    print("\n=== RAW SPEC FROM NOVA ===")
    print(json.dumps(spec, indent=2))
    print("Claude responded with a valid Dockerfile spec")
    print(f"Notes from Claude: {spec.get('notes', '')}")

    print("\n--- Step 3: Assembling Dockerfile ---")
    dockerfile = assemble_dockerfile(spec, output_path="Dockerfile.generated")

    print("\n=== DONE ===")
    print(dockerfile)


if __name__ == "__main__":
    # Takes repo path as argument, defaults to current directory
    repo = sys.argv[1] if len(sys.argv) > 1 else "."
    run(repo)