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

## Run Service

Start FastAPI with Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Health endpoint:

```bash
curl http://127.0.0.1:8000/health
```
