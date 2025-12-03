# Farms Service

The `farms` service provides CRUD for farms and sectors using PostGIS-enabled Supabase Postgres.

Start locally:
```powershell
$Env:DATABASE_URL = "sqlite:///./dev.db"
uvicorn services.farms.main:app --reload --port 8002
```

Endpoints:
- POST `/farms` — create a farm with GeoJSON polygon.
- GET `/farms/{id}` — get farm details and geometry.
- POST `/farms/{id}/sectors` — create a sector polygon in the farm.

Notes:
- This service expects an `x-user-id` header indicating the user's Supabase `id`. In production, this will come from Supabase Auth.
- This is scaffold code; integrate with Supabase JWT and RLS where required for security.
