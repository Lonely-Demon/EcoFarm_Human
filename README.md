```markdown
# EcoFarm

Backend (FastAPI) — EcoFarm_Human

This repository contains the modular FastAPI backend used for the EcoFarm_Human MVP. Services are designed to be modular and independently deployable.

## Quick start (local dev - no Docker)
1. Create a Python environment:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
2. Copy `.env.example` to `.env` and populate values (use a Supabase dev project for `DATABASE_URL` and `SUPABASE_KEY`).
3. Start a service (run each in its own terminal):
```powershell
uvicorn services.auth.main:app --reload --port 8000
uvicorn services.weather.main:app --reload --port 8001
uvicorn services.farms.main:app --reload --port 8002
uvicorn services.ai_recs.main:app --reload --port 8003
```
4. Use the `/docs` endpoint on each service to explore the OpenAPI/Swagger docs.

## Tests
Run the test suite with:
```powershell
pytest -q
```

## Notes
- This skeleton targets Supabase for DB & Auth. To run the full functionality, create a Supabase project and set the `DATABASE_URL`/`SUPABASE_KEY` env variables.
- The `alembic` folder contains migrations and env configuration; run migrations with the `alembic` CLI with `DATABASE_URL` set to the Supabase connection string.
- Run the AI Recommendations service as a separate FastAPI process (port 8003). The Streamlit demo posts to `http://localhost:8003/ai/rec/` for recommendations.

```
