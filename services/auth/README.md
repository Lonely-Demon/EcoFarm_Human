# Auth Service

This service handles user signup and login via Supabase Auth (service role). It also saves user profile data in the `users` table in Supabase Postgres.

Start service locally:
```powershell
$Env:DATABASE_URL = "sqlite:///./dev.db"
$Env:SUPABASE_URL = "https://<your>.supabase.co"
$Env:SUPABASE_KEY = "your_service_role_key"
uvicorn services.auth.main:app --reload --port 8000
```

Endpoints:
- POST /auth/register
- POST /auth/login

Notes:
- This is a skeleton for integrating Supabase Auth. Replace `supabase_client` usage with the official SDK functions appropriately.
