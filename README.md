# AI Dockerfile Generator

I built this project to automate the first steps of containerizing an application.

It reads a repository, identifies the language, dependencies, entry point, and port, then uses a Groq-hosted model to generate a Dockerfile. If the model is unavailable, it uses a local fallback so the pipeline can still run.

The generated Dockerfile uses a multi-stage build and runs the application as a non-root user.

## How it works

1. GitHub Actions checks out the repository.
2. The Python code collects basic project information.
3. Groq generates a structured Dockerfile specification.
4. The project converts that specification into a Dockerfile.
5. Docker builds the image.
6. Trivy scans the image for HIGH and CRITICAL vulnerabilities.
7. Clean images are pushed to Amazon ECR with the Git commit SHA as the tag.

## Run locally

```bash
cd /Users/m.rathi/Projects/ai-dockerfile-generator
cp .env.example .env
```

Add your Groq key to `.env`:

```env
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

Then run:

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
python3 main.py testing_repo/flask-app
```

The generated file is `Dockerfile.generated`.

## Build and test the container

```bash
docker build -f Dockerfile.generated \
  -t ai-dockerfile-generator:local \
  testing_repo/flask-app

docker run --rm -p 5000:5000 ai-dockerfile-generator:local
```

The sample application is available at `http://localhost:5000` and its health check is at `/health`.

## AWS deployment

GitHub Actions uses GitHub OIDC to authenticate to AWS. It builds the image, scans it with Trivy, and pushes it to ECR.

The workflow uses these GitHub repository secrets:

- `AWS_ROLE_ARN`
- `AWS_REGION`
- `ECR_REPOSITORY`
- `GROQ_API_KEY`

The ECR repository used for this project is:

```text
357275711997.dkr.ecr.ap-south-1.amazonaws.com/ai-dockerfile-generator
```

## Results

- Groq generation works locally.
- The sample image builds successfully.
- The container health check passes.
- Trivy found 0 HIGH or CRITICAL vulnerabilities in the final image.
- GitHub Actions successfully pushed the image to ECR.
- The local pipeline benchmark completed 10 runs with a mean of 0.22 ms and p95 of 0.44 ms for repository inspection and Dockerfile generation.
