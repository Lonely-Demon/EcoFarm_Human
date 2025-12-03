# Developer Onboarding (No Docker Required)

This onboarding guide helps a new developer set up the environment for the EcoFarm_Human MVP on a low-capacity laptop (no Docker) and on remote development platforms.

## Prerequisites
- Python 3.10+ installed on the machine.
- Windows PowerShell (the default); use Git Bash if you prefer.
- Git and a GitHub account.
- Supabase account for cloud DB & storage.
- Optionally: GitHub Codespaces or Gitpod account for remote dev (recommended if your machine is limited).

## Local Setup (PowerShell)
1. Clone repository:
```powershell
git clone https://github.com/yourorg/EcoFarm_Human.git
cd EcoFarm_Human
```
2. Create virtual env & activate:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
3. Install dependencies (use `pyproject.toml` or `requirements.txt`):
```powershell
pip install -r services/auth/requirements.txt
```

4. Create environment variables (or edit `.env`):
```powershell
$Env:SUPABASE_URL = "https://<project>.supabase.co"
$Env:SUPABASE_KEY = "<your_service_role_key>"
$Env:OPEN_METEO_URL = "https://api.open-meteo.com"
$Env:HUGGING_FACE_API_KEY = "hf_..."
$Env:SENTRY_DSN = ""
$Env:SENTRY_ENV = "development"
$Env:SENTRY_RELEASE = "dev"
```

5. Run a service (example, farms):
```powershell
uvicorn services.farms.main:app --reload --port 8002
```
To run all services needed for MVP locally (auth, weather, farms, ai_recs), start them in separate shells or use the provided `scripts/run_services.ps1` script.

Start AI Recommendations service locally:
```powershell
uvicorn services.ai_recs.main:app --reload --port 8003
```
6. Access Swagger: `http://localhost:8002/docs`

## Connecting to Supabase
1. Create a Supabase project at https://app.supabase.com/
2. From the Supabase Project Dashboard -> Settings -> API -> copy `SUPABASE_URL` and create a `service_role` key. Save these as secrets in GitHub.
3. In SQL editor, enable PostGIS:
```sql
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```
4. Create your initial tables using the SQL editor or migration scripts (use Alembic): see `Docs/Overall Project/modular-architecture.md`.

## Streamlit demo
- Streamlit is a local QA interface used for quick tests and demos; it is not required to be deployed.
- To run:
```powershell
pip install -r services/streamlit_demo/requirements.txt
streamlit run services/streamlit_demo/app.py
```

## Using GitHub Codespaces or Gitpod
- For limited hardware, Codespaces or Gitpod provide remote dev environments where you can run containers and the full toolchain.
- Add `.devcontainer` or `.gitpod.yml` to the repo so that you can boot a consistent environment.

## Migrations & DB seeds
- Use Alembic to create and run migrations; document the process in `Docs/Overall Project/modular-architecture.md`.

## PR Workflow & CI
- Create a PR: Run lint & unit tests locally (or in Codespaces), then push to GitHub for GH Actions.
- On `main` merges, GitHub Actions will run tests and deploy to staging if configured.

## Helpful Links
- Supabase: https://supabase.com
- FastAPI: https://fastapi.tiangolo.com
- Uvicorn: https://www.uvicorn.org
- Streamlit: https://streamlit.io
- Fly.io: https://fly.io
- Render: https://render.com
