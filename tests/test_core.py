import json
import tempfile
import unittest
from pathlib import Path

from src.context_collector import collect_context
from src.dockerfile_assembler import assemble_dockerfile
from src.llm_client import build_prompt, mock_model_response


class CorePipelineTests(unittest.TestCase):
    def test_collect_and_generate_offline(self):
        root = Path("testing_repo/flask-app")
        context = collect_context(root)
        self.assertEqual(context["language"], "python")
        self.assertEqual(context["dependency_file"], "requirements.txt")
        self.assertIn("port_hints", context)
        self.assertIn("Port hints found", build_prompt(context))

        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "Dockerfile.generated"
            dockerfile = assemble_dockerfile(mock_model_response(context), output)
            self.assertTrue(output.exists())
            self.assertIn("COPY . .", dockerfile)
            self.assertIn("COPY --from=builder /opt/venv /opt/venv", dockerfile)
            self.assertIn("/opt/venv/bin", dockerfile)
            self.assertIn("USER appuser", dockerfile)
            self.assertIn('CMD ["gunicorn"', dockerfile)


if __name__ == "__main__":
    unittest.main()
