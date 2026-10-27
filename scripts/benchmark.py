"""Measure the deterministic local pipeline; no AWS credentials are required."""
import json
import contextlib
import io
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.context_collector import collect_context
from src.dockerfile_assembler import assemble_dockerfile
from src.llm_client import mock_model_response


def main():
    root = Path("testing_repo/flask-app")
    samples = []
    for _ in range(10):
        started = time.perf_counter()
        context = collect_context(root)
        with contextlib.redirect_stdout(io.StringIO()):
            assemble_dockerfile(mock_model_response(context), "/tmp/Dockerfile.generated")
        samples.append((time.perf_counter() - started) * 1000)

    print(json.dumps({
        "runs": len(samples),
        "mean_ms": round(statistics.mean(samples), 2),
        "p95_ms": round(sorted(samples)[-1], 2),
        "detected_language": context["language"],
        "detected_entry_point": context["entry_point"],
    }, indent=2))


if __name__ == "__main__":
    main()
