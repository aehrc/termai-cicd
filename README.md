# termai-cicd

CI/CD testing project for Termai, using a simple FastAPI service with one endpoint:

- `GET /health` returns `status` and `time` (UTC ISO-8601 format).

## Requirements

- Python 3.11+

## Install

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install app and test dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
```

## Build / Checks

Compile source and tests:

```bash
python -m compileall app tests
```

Run tests:

```bash
python -m pytest -q
```
Run tests with info

```bash
python -m pytest -vv -s -rA --log-cli-level=INFO
```

## Run Service

Start FastAPI with Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Health endpoint:

```bash
curl http://127.0.0.1:8000/health
```

## CI/CD Pipeline

The GitHub Actions workflow at `.github/workflows/ci.yml` runs on every push to `main` and performs:

1. Python setup and dependency installation from `requirements.txt` and `requirements-test.txt`.
2. Unit/integration test execution with `pytest`.
3. Docker image build.
4. Image push to GitHub Container Registry (GHCR) with tags:
   - `ghcr.io/<owner>/<repo>:<commit-sha>`
   - `ghcr.io/<owner>/<repo>:latest`

Required GitHub setup:

- Repository Actions must have `packages: write` permission.
- Registry auth is handled with `${{ secrets.GITHUB_TOKEN }}` in the workflow.

## Kubernetes Deploy

Manifests are under `k8s/`:

- `deployment.yaml`
- `service.yaml`
- `ingress.yaml`

These files use placeholders so namespace/image/host are configurable:

- `${NAMESPACE}`
- `${IMAGE}`
- `${INGRESS_HOST}`

Apply them with `envsubst`:

```bash
export NAMESPACE=termai
export IMAGE=ghcr.io/<owner>/<repo>:<commit-sha>
export INGRESS_HOST=termai.internal.example.com

kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -
envsubst < k8s/deployment.yaml | kubectl apply -f -
envsubst < k8s/service.yaml | kubectl apply -f -
envsubst < k8s/ingress.yaml | kubectl apply -f -
```

## Updating Image And Triggering Deployment

1. Push code to `main` to trigger CI and publish a new image tag (commit SHA).
2. Update deployment to the new image:

```bash
export NAMESPACE=termai
export IMAGE=ghcr.io/<owner>/<repo>:<new-commit-sha>
envsubst < k8s/deployment.yaml | kubectl apply -f -
kubectl -n "$NAMESPACE" rollout status deploy/termai-cicd
```

## Suggested Project Structure

```text
.
├── app/                         # FastAPI application code
├── tests/                       # Pytest test suite
├── Dockerfile                   # Container build definition
├── .dockerignore
├── requirements.txt             # Runtime dependencies
├── requirements-test.txt        # Test dependencies
├── k8s/                         # Kubernetes manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
└── .github/
    └── workflows/
        └── ci.yml               # CI pipeline (test, build, push)
```
