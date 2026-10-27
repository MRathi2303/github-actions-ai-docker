# AI Dockerfile Generator

An AI-assisted CI pipeline that inspects a repository, generates a production Dockerfile with Groq-hosted open models, scans the image with Trivy, and publishes immutable images to Amazon ECR.

## What works today

- Repository language, dependency, entry-point, port, and existing-Dockerfile detection.
- Offline fallback for local development when Groq is unavailable.
- Structured model output converted into a multi-stage, non-root Dockerfile.
- GitHub Actions build → Trivy HIGH/CRITICAL gate → ECR push.
- Commit-SHA image tags plus `latest`.

## Architecture

```text
repository → context collector → Groq JSON response → Dockerfile assembler
                                      ↓
                              deterministic fallback
                                      ↓
                 Docker build → Trivy gate → Amazon ECR
```

The generated image uses a multi-stage build, copies the dependency virtual environment into the runtime stage, and runs as a non-root user.

## Run locally (no AWS required)

```bash
cp .env.example .env
# Edit .env and replace gsk_your_key_here with your Groq API key.
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
python3 main.py testing_repo/flask-app
python3 scripts/benchmark.py
```

The generated file is `Dockerfile.generated`. The Groq call uses a hosted free-tier model and falls back to a deterministic local spec when the API is unavailable.

Get a key from [Groq Console](https://console.groq.com/keys), paste it after `GROQ_API_KEY=` in `.env`, and run `python3 main.py testing_repo/flask-app` from this project directory. The key is never committed because `.env` is ignored.

## AWS image publishing

The original AWS resources are not recoverable from Git. Recreate an IAM role trusted by GitHub Actions OIDC and configure these GitHub Actions secrets:

`AWS_ROLE_ARN`, `AWS_REGION`, `GROQ_API_KEY`, and `ECR_REPOSITORY`.

For GitHub Actions, add `GROQ_API_KEY` under the repository’s Settings → Secrets and variables → Actions → New repository secret. Do not paste the key into the workflow file.

The repository-scoped OIDC role is created by `scripts/setup_aws_oidc.sh`; it trusts only the `main` branch of this repository and can publish only to this project’s ECR repository.

For this restored environment, the intended values are `ap-south-1`, `openai/gpt-oss-20b`, and the ECR repository created for this project. GitHub Actions uses OIDC for AWS; it does not use the local AWS profile.

Current ECR repository: `357275711997.dkr.ecr.ap-south-1.amazonaws.com/ai-dockerfile-generator`.

## Measured baseline

On 2026-10-27, the deterministic local pipeline completed 10 runs with a mean of 0.22 ms and p95 of 0.44 ms on the development machine. This measures repository inspection plus Dockerfile assembly only; it excludes the hosted model, Docker build, Trivy, and network time. One automated integration-style test passes.

The generated sample image was built successfully as `ai-dockerfile-generator:local`, and its non-root Gunicorn container returned `{"service":"ai-docker-utility","status":"healthy"}` from `/health`. Trivy reported 0 HIGH/CRITICAL vulnerabilities after unfixed findings were ignored.

The role needs only ECR push and the permissions required by the selected deployment target. Do not commit access keys.

## Honest resume bullets

Resume-ready wording:

> Built an AI-assisted DevOps pipeline using Groq, Python, Docker, GitHub Actions, Trivy, and Amazon ECR; generated multi-stage non-root Dockerfiles from repository context, added a deterministic offline fallback, and gated SHA-tagged images on HIGH/CRITICAL vulnerabilities.

Before adding more numbers, run the Docker build and Trivy scan locally or from GitHub Actions and record image size, build duration, scan duration, and vulnerability counts.
