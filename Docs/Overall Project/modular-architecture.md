# Modular Architecture

This doc describes the repo layout and how to run each service locally without Docker, which is essential for your laptop constraints.

## Repo Structure (suggested)
```
services/
  auth/
    main.py
    routers/
    models/
    schemas/
    requirements.txt
  users/
  farms/
  weather/
  market/
  ai_recs/
  disease_detection/
  tasks_records/
  streamlit_demo/
common/
  config.py
  db.py
  utils.py
tests/
ci/
Docs/
README.md
pyproject.toml
```

## How each service runs locally (no Docker)
- Each service is a small FastAPI app with `main.py` file exposing `app`.
- Run using Uvicorn: `uvicorn services.<service>.main:app --reload --port 800X`.
- Each service requires a minimal `.env` (or environment variables set) to connect to the cloud Supabase Postgres and provider keys.

## Example environment variables per service (add in `.env.example`)
```
SUPABASE_URL=https://<your-proj>.supabase.co
SUPABASE_KEY=<service_role_key>
OPEN_METEO_API_URL=https://api.open-meteo.com
HUGGING_FACE_API_KEY=hf_...
```

## Database & Geo (PostGIS)
- Use PostGIS functions for spatial queries and storing GeoJSON in `geometry` column.
- Example table:
```sql
CREATE TABLE farms (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES auth.users(id),
  name text,
  geom geometry(Polygon, 4326),
  created_at timestamptz DEFAULT now()
);
```
- Example insert using GeoJSON:
```sql
INSERT INTO farms (user_id, name, geom) VALUES (
  'user-uuid', 'My Farm', ST_SetSRID(ST_GeomFromGeoJSON('{...geojson...}'), 4326)
);
```

## Module independence & interfaces
- Provide a clear OpenAPI schema per service with example payloads.
- Keep database schemas partitioned by `schema` if required, or create logical table prefixes per service.
- Use REST APIs for inter-service communication. Avoid direct DB reads/writes across services; instead, use read-only endpoints.

## Local dev (PowerShell)
1. Create virtual env and install deps:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r services/auth/requirements.txt
```
2. Start a service:
```powershell
$Env:SUPABASE_URL="https://<your-proj>.supabase.co"
$Env:SUPABASE_KEY="<service_role_key>"
uvicorn services.farms.main:app --reload --port 8002
```
3. Test with Swagger: `http://localhost:8002/docs`

## Database Migrations
- Use Alembic for migrations and track schema changes per service.
- Keep one `alembic` config per service or a centralized migrations with naming conventions to prevent conflicts.

## CI/CD Considerations
- Each service should have an independent GitHub Actions workflow file to run tests and deploy the service.
- Prefer a `deploy/service_name.yml` that runs on push to `main` and calls the remote deploy provider CLI/API.

## Service Contracts
- Maintain OpenAPI JSON per service and publish to `docs/api_contracts` or a central place for contract tests.

## Security
- Use JWT signed tokens or Supabase Auth session tokens for requests.
- Keep service_role key only in server environments and avoid using it in client apps.
