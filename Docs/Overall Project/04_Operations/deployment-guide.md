# Deployment Guide

This deployment guide explains the CI/CD and hosting options for the FastAPI modular backend and how to deploy with no Docker on local machine.

## Key concepts
- Services (each module) are deployed individually.
- Services are tested via GitHub Actions, which builds & deploys from the runner (no local Docker required).
- Database is Supabase-managed Postgres (dev/staging/prod) with a separate project per environment.

## Nice provider options
- Fly.io
- Render
- Railway
- DigitalOcean App Platform
- Alternatives: GCP Cloud Run (if you want to pay later), Azure App Service, Heroku (paid)

## Provider comparison (short)
- **Fly.io**: Easy global-edge small deployments; good for small microservices; limited free plan; CLI `flyctl` client. Good latency for global users. May require understanding of VMs and regional placement.
- **Render**: Simple to use, has a friendly UI, good for web & background workers, built-in TLS. Free tier and reasonable pricing.
- **Railway**: Developer-focused, quick to spin-up integrations (Supabase, DB); useful for prototype. Pricing can grow as you use more features.
- **DigitalOcean App Platform**: Developer-friendly and predictable pricing; supports multiple languages.
- **GCP Cloud Run**: Pay for what you use, high availability, best integration with Vertex AI and other GCP services. May be overkill and costly for early pilot.

## Render (chosen provider)
Render is a simple, reliable platform with a developer-friendly interface and robust free/low-tier offerings. It's a great fit for the MVP when combined with Supabase.

### Pros
- Simplicity: Easy deploy from GitHub with quick setup. 
- Built-in TLS & managed domains.
- Reasonable scaling for small-to-medium workloads.
- Good logs, basic monitoring. 

### Cons
- Limited advanced networking features compared to Cloud Run.
- May require paid plans for heavier inference workloads.

### Render Deployment Steps (for a FastAPI service)
1. Connect Render to GitHub and choose the repo.
2. Create a new Web Service: select Python, set the root directory to the service folder (e.g., `services/farms`).
3. Set the start command: `uvicorn services.farms.main:app --host 0.0.0.0 --port $PORT`.
4. Add environment variables via the Render Dashboard (e.g., `SUPABASE_URL`, `SUPABASE_KEY`, `HUGGING_FACE_API_KEY`).
5. Configure resource limits as needed.
6. Deploy and watch logs; use the `Manual Deploy` option for staging.

### Start commands (per service)
- Auth service: `uvicorn services.auth.main:app --host 0.0.0.0 --port $PORT`
- Farms service: `uvicorn services.farms.main:app --host 0.0.0.0 --port $PORT`
- Weather service: `uvicorn services.weather.main:app --host 0.0.0.0 --port $PORT`
 - AI Recommendations: `uvicorn services.ai_recs.main:app --host 0.0.0.0 --port $PORT`

When you create each service on Render, set the `Start Command` in the service settings to one of the above commands and provide env vars via the `Environment` tab.

### GitHub Actions sample for Render deploy
Add `RENDER_API_KEY` into GitHub Secrets. For multi-service deployments add service-specific secrets `RENDER_SERVICE_ID_FARMS` and `RENDER_SERVICE_ID_AUTH` and point each GH Action to the corresponding secret.

```yaml
name: CI & Deploy - Render

on:
  push:
    branches: [ main ]

jobs:
  build-test-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.10
      - name: Install dependencies
        run: |
          pip install -r services/farms/requirements.txt
      - name: Run unit tests
        run: |
          pytest services/farms -q
      - name: Deploy to Render
        uses: render-examples/deploy@v1
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
          RENDER_SERVICE_ID: ${{ secrets.RENDER_SERVICE_ID }}
        with:
          serviceId: ${{ secrets.RENDER_SERVICE_ID }}
          region: "iad"  # choose region; set according to Render
          path: "services/farms"
```

Note: You may instead use Render's REST API to trigger builds and deploys if you prefer to script the process. The `render-examples/deploy` action is an example and can be replaced with Render's official action or workflow.

### Environment & Secrets
- Add Render env vars in the service settings (SUPABASE_URL, SUPABASE_KEY, HF key). Keep these secrets in GitHub as well for Action runs.
- For environment-based deployments, set a `staging` vs `production` Render service and deploy the respective branch.

### Monitoring & Logs
- Use Render's logs and request metrics for quick insights.
- Add Sentry or similar for error monitoring (Sentry DSN as an environment variable in Render).


## CI/CD (GitHub Actions) outline
1. PRs: Lint, unit tests, contract tests.
2. Merge to `main`: Create a release artifact; run integration tests against a test Supabase instance; deploy to staging.
3. Manual approval/Promote to production.

### Example: Deploying Service to Fly.io
- Configure GitHub secrets: `FLY_API_TOKEN`, `SUPABASE_URL`, `SUPABASE_KEY`, `HUGGING_FACE_API_KEY`.
- Sample action steps:
  - Checkout
  - Setup Python
  - Install deps
  - Run unit tests
  - Build & push (Fly builds via the builder)
  - Deploy via `flyctl deploy`

## Secrets management
- Keep keys in GitHub Secrets for deployment.
- For runtime storage, use each provider's secret manager (Render/ Fly / Railway) or keep them set in supabase config where appropriate.

## Environment variables & config
- Each service must read the following minimum environment variables:
  - `SUPABASE_URL` and `SUPABASE_KEY` or `DATABASE_URL`
  - `HUGGING_FACE_API_KEY` if used
  - `OPEN_METEO_URL` (default: https://api.open-meteo.com)
  - `EXTERNAL_PROVIDER_API_KEYS` for any market scraping or APIs.

## Choosing region for India/Tamil Nadu
- Try to pick deployment regions closest to Tamil Nadu (e.g., `asia-south1` or `asia-south-east` depending on provider) and choose the same region for Supabase and services where possible to reduce latency.

## Rolling back & troubleshooting
- Keep per-service versions in hosted provider dashboard and perform rollback from the UI or via CLI.
- Monitor logs via the hosting provider console; use Sentry or similar for stack traces.

## Cost control guidelines
- Start with free tiers (Fly/Render/Railway) and monitor usage; gauge cost of inference API and model calls.
- Cache expensive calls (inference results/market data) and set limits on inference per user to reduce cost.

## Recommendations
- For MVP: Use Render or Fly.io for deployments (both are simple to use, support multiple services, and have free/low-cost tiers).
- Later: Migrate services to GCP Cloud Run for production scaling and Vertex AI integration if you need advanced ML operations.
