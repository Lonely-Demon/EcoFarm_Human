# Sprint Plan (MVP) — Render + Supabase

This sprint plan is tuned for the constraints you've provided: FastAPI modular backend, Supabase for DB, Render for hosting, no local Docker, and public/free datasets.

## Sprint cadence & structure
- Sprint length: 2 weeks.
- Focus: each sprint delivers one set of independent services with unit & integration tests and a Streamlit demo hook.
- Team: one or more developers; adjust per capacity.

### Sprint 1 — Foundations & Core Data (2 weeks)
**Goal**: Basic user auth, farms, and weather service; running in local dev & on Render staging.

**Deliverables:**
- `services/auth`: register/login + JWT tokens integrated with Supabase session.
- `services/farms`: CRUD for farms & sectors with GeoJSON and PostGIS support.
- `services/weather`: Open-Meteo & NASA POWER aggregator with cache table in Supabase.
- Streamlit demo skeleton to test endpoints (weather fetch, farm CRUD).
- Setup GitHub repo, `pyproject.toml`, and pre-commit hooks.
- Setup Render staging & link to GitHub.

**Acceptance Criteria**:
- Auth & farms endpoints tested and reachable via Swagger for each service.
- Weather endpoint returns aggregated data from providers & stores cached copy in Supabase.
- Basic Streamlit demo that exercises the above features.

---

### Sprint 2 — AI Recommendations & Market Data (2 weeks)
**Goal**: Add AI recommendations & disease detection wrapper; market aggregator for Tamil Nadu.

**Deliverables:**
- `services/market`: scrape or fetch Tamil Nadu market data (eNAM/Agmarknet) and normalize & cache.
- `services/ai_recs`: prototype to query soil & weather + provide ranked crop suggestions.
- `services/disease_detection`: image upload routes & inference integration with Hugging Face.
- Increase Streamlit demo: add demo forms for `ai_recs` and image upload.
- Add unit & integration tests and basic contract tests.

**Acceptance Criteria:**
- `ai_recs` endpoint returns ranked crop suggestions and rationale (uses at least one public soil dataset + weather + market if available).
- `disease_detection` calls Hugging Face & returns label + confidence; results are stored in Supabase.

---

### Sprint 3 — Polish & Deploy (2 weeks)
**Goal**: Finalize tasks/records module, CI/CD per-service deployment on Render, documentation & runbook.

**Deliverables:**
- `services/tasks_records`: CRUD for tasks & records; basic P&L partials for manual entries.
- Add Streamlit demo for task creation & record entry.
- CI: GitHub Actions flows for tests and Render deployment for each service.
- Final docs: `Docs` assembled; Runbook, Testing Strategy, Data Privacy docs finished.
- Acceptance tests & staging deploy ready for pilot launch.

**Acceptance Criteria:**
- Each service can be deployed independently to Render via GitHub Actions.
- Staging environment built & seeded; staging endpoints functional.
- Smooth Streamlit demo that exercises core flows.

---

## Adjustments & Notes
- Exclude marketplace & community features from the MVP.
- Render-specific: configure auto-deployment on merges to `main`; use separate Render services for each module or group modules logically.
- Keep endpoints versioned and include OpenAPI export per service in `Docs/Overall Project/api_contract_schemas/`.
- Use Supabase staging & production projects to isolate testing.

## Post-MVP (Phase 2)
- Add marketplace features, payments, and community if pilot shows traction.
- Consider migrating to GCP Cloud Run + Vertex AI when the ML workload grows.

---

End of Sprint Plan
