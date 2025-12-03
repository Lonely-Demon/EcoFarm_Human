# Supabase Setup Plan for EcoFarm_Human MVP

This guide provides step-by-step instructions to setup Supabase projects for the MVP using only cloud-hosted resources (no local Postgres). It assumes you're a beginner with Supabase.

## 1. Create Supabase account & project
1. Sign up at https://app.supabase.com.
2. Create a new project. For region selection, choose one closest to India (e.g., `asia-south1` if available) to reduce latency for Tamil Nadu users.
3. The Supabase CLI is optional - you can use the web dashboard for most operations.

## 2. Copy API keys and connect from FastAPI
1. In the Dashboard -> Settings -> API, copy `SUPABASE_URL`, `anon` key and `service_role` key. The `service_role` key has elevated permissions and should only be used in server-side processes (not client apps).
2. Export environment variables on Windows PowerShell:
```powershell
$Env:SUPABASE_URL = "https://<project>.supabase.co"
$Env:SUPABASE_KEY = "<service_role_key>"
```
3. In FastAPI use `SQLAlchemy` or `databases` to connect to Supabase using a connection string (from the Dashboard -> Database -> Connection string). Save connection string into `DATABASE_URL`.

## 3. Add extensions (PostGIS & UUID)
Use the SQL editor in the Dashboard:
```sql
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

## 4. Create initial tables
Example DDL for `farms` table:
```sql
CREATE TABLE farms (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES auth.users(id),
  name text,
  geom geometry(Polygon, 4326),
  created_at timestamptz DEFAULT now()
);
```
Example `disease_reports`:
```sql
CREATE TABLE disease_reports (
   id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
   user_id uuid REFERENCES auth.users(id),
   farm_id uuid REFERENCES farms(id),
   image_path text,
   result JSONB,
   confidence float,
   created_at timestamptz DEFAULT now()
);
```

## 5. Storage
- Use Supabase Storage for user-uploaded images (disease photos) and static assets. Configure a `public` bucket (or `private` with signed URLs for downloads).
- Example to create a storage bucket in Dashboard -> Storage.

## 6. Authentication
- Use Supabase Auth if desired: supports email/phone OTP and social providers.
- For MVP use JWTs signed by FastAPI or use Supabase Auth with RLS policies on tables.

## 7. Row-Level Security (RLS) & Security
- RLS can be enabled per table; for early MVP you can keep RLS disabled, but add it as soon as PII is needed in production.
- Set `service_role` key for server-side tasks only.

## 8. Migrations & Alembic
- Use Alembic to track schema changes locally and run migrations against Supabase. Example steps:
```powershell
pip install alembic
alembic init alembic
# edit alembic.ini to point to DATABASE_URL
alembic revision --autogenerate -m "create farms disease_reports"
alembic upgrade head
```

## 9. Using Supabase Storage for images & signed URLs
- Upload images via Supabase Storage, then generate a signed URL to pass to the HF inference.
- Store image URL or key in `disease_reports`.

## 10. Best Practices
- Use separate Supabase projects for `dev`, `staging`, and `prod`.
- Use `service_role` only in server environments.
- Keep `anon` key for client non-sensitive operations only.
- Monitor usage & upgrade when needed.

## 11. Useful Tools
- Supabase CLI if desired (some commands require Docker for `supabase start` — not required for cloud): https://supabase.com/docs/guides/cli
- `pysupabase` or `supabase-py` (Python client) to talk to Supabase services (auth & storage).

## 12. Troubleshooting
- If PostGIS is not available in your region (rare), choose a region that supports it.
- If you run into storage permission issues, double-check bucket policies & RLS.

---
If you'd like, I can prepare SQL migration templates and a small `alembic` setup to create the initial `farms` and `disease_reports` tables, and create a minimal FastAPI skeleton to read/write them.