from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Docker Utility — Project Documentation</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #0d1117;
    color: #c9d1d9;
    line-height: 1.7;
  }

  nav {
    background: #161b22;
    border-bottom: 1px solid #30363d;
    padding: 16px 40px;
    position: sticky;
    top: 0;
    z-index: 100;
    display: flex;
    align-items: center;
    gap: 12px;
  }

  nav h1 {
    font-size: 18px;
    color: #58a6ff;
    font-weight: 600;
  }

  .badge {
    background: #238636;
    color: #aff5b4;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 500;
  }

  .badge.yellow {
    background: #9e6a03;
    color: #f8e3a1;
  }

  .container {
    max-width: 900px;
    margin: 0 auto;
    padding: 60px 40px;
  }

  .hero {
    text-align: center;
    padding: 80px 0 60px;
    border-bottom: 1px solid #30363d;
    margin-bottom: 60px;
  }

  .hero h2 {
    font-size: 36px;
    color: #e6edf3;
    font-weight: 700;
    margin-bottom: 16px;
  }

  .hero p {
    font-size: 18px;
    color: #8b949e;
    max-width: 600px;
    margin: 0 auto 30px;
  }

  .tech-stack {
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
  }

  .tech-pill {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 13px;
    color: #79c0ff;
  }

  h2.section-title {
    font-size: 24px;
    color: #e6edf3;
    margin-bottom: 8px;
    padding-bottom: 8px;
    border-bottom: 1px solid #30363d;
  }

  .section {
    margin-bottom: 60px;
  }

  .subtitle {
    color: #8b949e;
    margin-bottom: 24px;
    font-size: 15px;
  }

  .card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 24px;
    margin-bottom: 16px;
  }

  .card h3 {
    color: #58a6ff;
    font-size: 15px;
    margin-bottom: 8px;
    font-family: monospace;
  }

  .card p {
    color: #8b949e;
    font-size: 14px;
    margin-bottom: 12px;
  }

  .card ul {
    list-style: none;
    padding: 0;
  }

  .card ul li {
    color: #c9d1d9;
    font-size: 13px;
    padding: 4px 0;
    padding-left: 16px;
    position: relative;
  }

  .card ul li::before {
    content: "→";
    position: absolute;
    left: 0;
    color: #3fb950;
  }

  .code-block {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 20px;
    font-family: monospace;
    font-size: 13px;
    line-height: 1.8;
    overflow-x: auto;
    margin: 16px 0;
    white-space: pre;
  }

  .pipeline {
    display: flex;
    flex-direction: column;
    gap: 0;
  }

  .pipeline-step {
    display: flex;
    align-items: flex-start;
    gap: 16px;
  }

  .pipeline-left {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 40px;
  }

  .step-circle {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: #1f6feb;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 600;
    flex-shrink: 0;
  }

  .step-line {
    width: 2px;
    flex: 1;
    background: #30363d;
    min-height: 40px;
  }

  .pipeline-content {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 8px;
    flex: 1;
  }

  .pipeline-content h4 {
    color: #e6edf3;
    font-size: 14px;
    margin-bottom: 4px;
  }

  .pipeline-content p {
    color: #8b949e;
    font-size: 13px;
  }

  .pipeline-content .tag {
    display: inline-block;
    background: #0d419d;
    color: #79c0ff;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    margin-top: 6px;
    font-family: monospace;
  }

  .two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }

  .decision-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 20px;
  }

  .decision-card h4 {
    color: #3fb950;
    font-size: 13px;
    margin-bottom: 8px;
    font-family: monospace;
  }

  .decision-card p {
    color: #8b949e;
    font-size: 13px;
  }

  .highlight {
    color: #ffa657;
    font-family: monospace;
  }

  .green { color: #3fb950; }
  .blue { color: #79c0ff; }
  .yellow { color: #e3b341; }

  .problem-solution {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 16px;
  }

  .problem {
    background: #161b22;
    border: 1px solid #f85149;
    border-radius: 8px;
    padding: 16px;
  }

  .solution {
    background: #161b22;
    border: 1px solid #238636;
    border-radius: 8px;
    padding: 16px;
  }

  .problem h4 { color: #f85149; font-size: 13px; margin-bottom: 8px; }
  .solution h4 { color: #3fb950; font-size: 13px; margin-bottom: 8px; }
  .problem p, .solution p { color: #8b949e; font-size: 13px; }

  .metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 24px;
  }

  .metric {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
  }

  .metric .number {
    font-size: 28px;
    font-weight: 700;
    color: #58a6ff;
  }

  .metric .label {
    font-size: 12px;
    color: #8b949e;
    margin-top: 4px;
  }

  footer {
    border-top: 1px solid #30363d;
    padding: 40px;
    text-align: center;
    color: #8b949e;
    font-size: 13px;
  }

  @media (max-width: 600px) {
    .two-col, .problem-solution, .metric-row {
      grid-template-columns: 1fr;
    }
    .hero h2 { font-size: 24px; }
    .container { padding: 40px 20px; }
  }
</style>
</head>
<body>

<nav>
  <h1>AI Docker Utility</h1>
  <span class="badge">live on eks fargate</span>
  <span class="badge yellow">built by AI pipeline</span>
</nav>

<div class="container">

  <!-- HERO -->
  <div class="hero">
    <h2>AI-Assisted DevOps Platform</h2>
    <p>An internal tool that automatically generates production-ready Dockerfiles
    using AI, integrated into a full CI/CD pipeline on AWS.</p>
    <div class="tech-stack">
      <span class="tech-pill">Python</span>
      <span class="tech-pill">AWS Bedrock</span>
      <span class="tech-pill">Amazon Nova</span>
      <span class="tech-pill">GitHub Actions</span>
      <span class="tech-pill">Amazon ECR</span>
      <span class="tech-pill">EKS Fargate</span>
      <span class="tech-pill">Trivy</span>
      <span class="tech-pill">OIDC</span>
    </div>
  </div>

  <!-- METRICS -->
  <div class="section">
    <div class="metric-row">
      <div class="metric">
        <div class="number">3</div>
        <div class="label">Python modules built</div>
      </div>
      <div class="metric">
        <div class="number">5</div>
        <div class="label">Pipeline stages</div>
      </div>
      <div class="metric">
        <div class="number">0</div>
        <div class="label">AWS keys stored</div>
      </div>
      <div class="metric">
        <div class="number">14s</div>
        <div class="label">Pipeline runtime</div>
      </div>
    </div>
  </div>

  <!-- THE PROBLEM -->
  <div class="section">
    <h2 class="section-title">The problem</h2>
    <p class="subtitle">What this project solves</p>
    <div class="problem-solution">
      <div class="problem">
        <h4>Before this tool</h4>
        <p>Developers manually write Dockerfiles for every project. They're often
        generic, use 'latest' tags, run as root, skip multi-stage builds,
        and contain security vulnerabilities.</p>
      </div>
      <div class="solution">
        <h4>After this tool</h4>
        <p>Push code. The AI reads your repo, detects the language and framework,
        generates an optimized production-ready Dockerfile specific to your
        project, scans it for vulnerabilities, and deploys it automatically.</p>
      </div>
    </div>
  </div>

  <!-- ARCHITECTURE -->
  <div class="section">
    <h2 class="section-title">Architecture</h2>
    <p class="subtitle">Three Python modules, one pipeline</p>

    <div class="card">
      <h3>src/context_collector.py</h3>
      <p>Reads the pushed repository like a detective. Detects language, 
      dependencies, entry point, ports, and checks if a Dockerfile already exists.</p>
      <ul>
        <li>Detects language from file signatures (requirements.txt, package.json, go.mod)</li>
        <li>Reads dependency file contents (truncated to 2000 chars for token efficiency)</li>
        <li>Finds entry point by checking common patterns (app.py, index.js, main.go)</li>
        <li>Scans source files for port keywords (PORT=, port=, .listen()</li>
        <li>Switches to audit mode if Dockerfile already exists</li>
      </ul>
    </div>

    <div class="card">
      <h3>src/llm_client.py</h3>
      <p>The messenger. Takes the context dictionary, builds a structured prompt,
      calls Amazon Nova via AWS Bedrock, and returns parsed JSON.</p>
      <ul>
        <li>Loads config from config.yaml locally, environment variables in CI</li>
        <li>Builds provider-aware requests (Anthropic format vs Nova format)</li>
        <li>Defensive JSON extraction handles models that add extra text</li>
        <li>Falls back to mock response if Bedrock is unavailable</li>
        <li>Supports Claude and Amazon Nova via the same interface</li>
      </ul>
    </div>

    <div class="card">
      <h3>src/dockerfile_assembler.py</h3>
      <p>Turns the AI JSON spec into a real Dockerfile. Handles formatting,
      fixes model inconsistencies, and writes the file to disk.</p>
      <ul>
        <li>Multi-stage build — separate builder and runtime stages</li>
        <li>Defensive space fixing for copy commands (model sometimes drops spaces)</li>
        <li>Creates non-root appuser for security</li>
        <li>Uses exec format for CMD to avoid shell signal issues</li>
        <li>Writes to Dockerfile.generated so original is never overwritten</li>
      </ul>
    </div>
  </div>

  <!-- PIPELINE -->
  <div class="section">
    <h2 class="section-title">CI/CD Pipeline</h2>
    <p class="subtitle">What happens on every git push</p>

    <div class="pipeline">

      <div class="pipeline-step">
        <div class="pipeline-left">
          <div class="step-circle">1</div>
          <div class="step-line"></div>
        </div>
        <div class="pipeline-content">
          <h4>Code push triggers workflow</h4>
          <p>Developer pushes to main branch. GitHub Actions spins up a fresh
          Ubuntu runner with nothing installed.</p>
          <span class="tag">on: push → branches: main</span>
        </div>
      </div>

      <div class="pipeline-step">
        <div class="pipeline-left">
          <div class="step-circle">2</div>
          <div class="step-line"></div>
        </div>
        <div class="pipeline-content">
          <h4>OIDC authentication — no keys stored</h4>
          <p>GitHub requests a temporary token from AWS using OpenID Connect.
          The IAM role is locked to this specific repo. Token expires in 1 hour.
          Zero long-lived credentials stored anywhere.</p>
          <span class="tag">aws-actions/configure-aws-credentials@v4</span>
        </div>
      </div>

      <div class="pipeline-step">
        <div class="pipeline-left">
          <div class="step-circle">3</div>
          <div class="step-line"></div>
        </div>
        <div class="pipeline-content">
          <h4>AI generates project-specific Dockerfile</h4>
          <p>Python script reads the repo, builds a structured prompt with all
          project details, calls Amazon Nova on AWS Bedrock, receives a JSON spec,
          assembles it into a real Dockerfile.</p>
          <span class="tag">python3 main.py $GITHUB_WORKSPACE</span>
        </div>
      </div>

      <div class="pipeline-step">
        <div class="pipeline-left">
          <div class="step-circle">4</div>
          <div class="step-line"></div>
        </div>
        <div class="pipeline-content">
          <h4>Trivy security scan</h4>
          <p>Image is built and scanned for HIGH and CRITICAL CVEs before
          being pushed anywhere. Pipeline fails and blocks the push if
          unfixed vulnerabilities are found.</p>
          <span class="tag">aquasecurity/trivy-action@master</span>
        </div>
      </div>

      <div class="pipeline-step">
        <div class="pipeline-left">
          <div class="step-circle">5</div>
          <div class="step-line"></div>
        </div>
        <div class="pipeline-content">
          <h4>Push to Amazon ECR</h4>
          <p>Image pushed with two tags — latest for convenience, commit SHA
          for traceability. Every image can be traced back to the exact commit
          that built it. Supports rollbacks to any previous version.</p>
          <span class="tag">:latest + :$GITHUB_SHA</span>
        </div>
      </div>

      <div class="pipeline-step">
        <div class="pipeline-left">
          <div class="step-circle">6</div>
          <div class="step-line"></div>
        </div>
        <div class="pipeline-content">
          <h4>Deploy to EKS Fargate</h4>
          <p>kubectl applies the deployment manifest. Fargate provisions
          micro-VMs per pod — no node management, pay only when running.
          Load Balancer exposes a public URL. Rollout waits for healthy status.</p>
          <span class="tag">kubectl apply → rollout status</span>
        </div>
      </div>

    </div>
  </div>

  <!-- KEY DECISIONS -->
  <div class="section">
    <h2 class="section-title">Key engineering decisions</h2>
    <p class="subtitle">Why we built it this way</p>
    <div class="two-col">
      <div class="decision-card">
        <h4>OIDC over access keys</h4>
        <p>No AWS credentials stored in GitHub. The IAM role is locked to this
        specific repo and branch. Token expires automatically. Industry standard
        for GitHub → AWS authentication.</p>
      </div>
      <div class="decision-card">
        <h4>Structured JSON output</h4>
        <p>The LLM returns JSON, not a raw Dockerfile. This means the assembler
        can validate, fix, and control the output. If the model hallucinates,
        the schema catches it before it breaks the build.</p>
      </div>
      <div class="decision-card">
        <h4>Fargate over EC2 nodes</h4>
        <p>No node management. No paying for idle servers. Fargate sizes itself
        exactly to declared resource requests. Perfect for on-demand workloads
        triggered by code pushes.</p>
      </div>
      <div class="decision-card">
        <h4>Scan before push</h4>
        <p>Trivy runs after build but before ECR push. Vulnerable images never
        reach the registry. The pipeline fails fast and the developer gets
        immediate feedback on what needs fixing.</p>
      </div>
      <div class="decision-card">
        <h4>config.yaml in .gitignore</h4>
        <p>Local config contains AWS account ID and personal preferences. Never
        pushed to GitHub. CI reads from environment variables instead. Clean
        separation between local dev and production config.</p>
      </div>
      <div class="decision-card">
        <h4>Mock fallback in llm_client</h4>
        <p>When Bedrock is unavailable, the pipeline uses a hardcoded spec.
        This is called stubbing — it lets development continue without
        depending on external services being available.</p>
      </div>
    </div>
  </div>

  <!-- HOW TO USE -->
  <div class="section">
    <h2 class="section-title">How to use on any project</h2>
    <p class="subtitle">Three files is all you need</p>

    <div class="card">
      <h3>Option A — Copy into your repo</h3>
      <p>Copy these three things into any project repository:</p>
      <div class="code-block">your-project/
├── src/
│   ├── context_collector.py
│   ├── llm_client.py
│   └── dockerfile_assembler.py
├── main.py
└── .github/
    └── workflows/
        └── ai-dockerize.yml</div>
      <p>Add these GitHub secrets to that repo and every push auto-generates a Dockerfile:</p>
      <div class="code-block">AWS_ROLE_ARN        → your IAM role ARN
AWS_REGION          → ap-south-1
BEDROCK_MODEL_ID    → apac.amazon.nova-lite-v1:0
ECR_REPOSITORY      → your ECR URI
EKS_CLUSTER_NAME    → your cluster name</div>
    </div>

    <div class="card">
      <h3>Option B — Reusable workflow (recommended)</h3>
      <p>Keep the pipeline in one central repo. Any other project calls it
      with three lines:</p>
      <div class="code-block">jobs:
  dockerize:
    uses: YOUR_USERNAME/ai-based-docker-utility/.github/workflows/ai-dockerize.yml@main
    secrets: inherit</div>
      <p>One team owns the pipeline. Every team benefits from updates automatically.</p>
    </div>
  </div>

  <!-- WHAT YOU LEARNED -->
  <div class="section">
    <h2 class="section-title">What was built and learned</h2>
    <p class="subtitle">Skills developed building this project from scratch</p>
    <div class="two-col">
      <div class="card">
        <h3>Python</h3>
        <ul>
          <li>pathlib for filesystem operations</li>
          <li>f-strings and string formatting</li>
          <li>dict.get() for safe key access</li>
          <li>try/except for resilient code</li>
          <li>__name__ == __main__ pattern</li>
          <li>sys.argv for CLI arguments</li>
          <li>Module imports and packages</li>
        </ul>
      </div>
      <div class="card">
        <h3>AWS</h3>
        <ul>
          <li>Bedrock runtime API with boto3</li>
          <li>OIDC trust policy for GitHub</li>
          <li>ECR repository and image tagging</li>
          <li>EKS Fargate cluster setup</li>
          <li>IAM roles and policy attachment</li>
          <li>Inference profiles for model access</li>
          <li>Cross-region routing with apac. prefix</li>
        </ul>
      </div>
      <div class="card">
        <h3>GitHub Actions</h3>
        <ul>
          <li>Workflow triggers and conditions</li>
          <li>Job steps and dependencies</li>
          <li>GitHub secrets management</li>
          <li>Environment variables between steps</li>
          <li>GITHUB_ENV for step outputs</li>
          <li>Artifact upload and storage</li>
          <li>Reusable workflow pattern</li>
        </ul>
      </div>
      <div class="card">
        <h3>DevOps concepts</h3>
        <ul>
          <li>Multi-stage Docker builds</li>
          <li>Non-root container security</li>
          <li>Image scanning with Trivy</li>
          <li>Separation of concerns</li>
          <li>Stubbing external dependencies</li>
          <li>Prompt engineering for structured output</li>
          <li>Internal developer platforms</li>
        </ul>
      </div>
    </div>
  </div>

</div>

<footer>
  Built by Moon Rathi &nbsp;·&nbsp;
  AI-Assisted DevOps Utility &nbsp;·&nbsp;
  Running on EKS Fargate &nbsp;·&nbsp;
  Deployed via GitHub Actions
</footer>

</body>
</html>"""

@app.route("/health")
def health():
    from flask import jsonify
    return jsonify({"status": "healthy", "service": "ai-docker-utility"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 2032))
    app.run(host="0.0.0.0", port=port)