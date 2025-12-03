# Render Setup & CI/CD (Auth + Farms Services)

This doc walks through connecting your repo to Render and configuring CI via GitHub Actions to deploy services automatically.

## Prerequisites
- A Render account
- GitHub repository (this repo)
- A GitHub user with `repo` and `admin` permissions to set repository secrets
- Supabase project with `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`

## Create Services in Render
1. Sign in to Render and select **New -> Web Service**.
2. Connect to GitHub and pick this repository.
3. Set the **Root Directory** to the service path (e.g., `services/auth` or `services/farms`).
4. Runtime: choose Python and set the command:
   - Auth: `uvicorn services.auth.main:app --host 0.0.0.0 --port $PORT`
   - Farms: `uvicorn services.farms.main:app --host 0.0.0.0 --port $PORT`
5. Choose the branch to deploy (e.g., `main`).
6. Environment: Add necessary env vars under the service's **Environment** tab (see `ENV VARS` section below).
7. Deploy and check the logs when the initial build runs.

## ENV VARS (Minimal required per service)
- `SUPABASE_URL` (shared across services)
- `SUPABASE_KEY` (service_role; server-side only)
- `DATABASE_URL` (use the Supabase connection string)
- `HUGGING_FACE_API_KEY` (optional, only for AI services)
 - `SENTRY_DSN` (optional - Sentry DSN for error aggregation)
 - `SENTRY_ENV` (optional - e.g., staging, production)
 - `SENTRY_RELEASE` (optional - set to a commit SHA or release tag)
- `OPEN_METEO_URL` (weather service only)

Set these in Render’s Environment section for each service, and in GitHub repo secrets for CI.

## GitHub Secrets (minimum)
- `RENDER_API_KEY` (your Render API key) - repo-level secret
- `RENDER_SERVICE_ID_FARMS` - service ID (Render UI -> service -> `More` -> `Service ID`)
- `RENDER_SERVICE_ID_AUTH` - same as above for the auth service
 - `RENDER_SERVICE_ID_FARMS_STAGING` - service ID for staging farms service
 - `RENDER_SERVICE_ID_AUTH_STAGING` - service ID for staging auth service
 - `RENDER_SERVICE_ID_AI_RECS_STAGING` - service ID for staging ai_recs service
 - `RENDER_SERVICE_ID_WEATHER_STAGING` - service ID for staging weather service
 - `SLACK_WEBHOOK` - Slack incoming webhook URL for synthetic check notifications (optional but recommended)
 - `STAGING_BASE_URL` - Base URL for staging environment health checks (e.g., `https://staging.ecofarm.com`)
 - `PROD_BASE_URL` - Base URL for production environment health checks (e.g., `https://api.ecofarm.com`)
## Recommended GitHub Secrets naming and usage
- `RENDER_API_KEY` - Render API key used to trigger deployments
- `RENDER_SERVICE_ID_FARMS` - Render Service ID for `ecofarm-farms`
- `RENDER_SERVICE_ID_AUTH` - Render Service ID for `ecofarm-auth`
- `SUPABASE_URL` - Supabase URL
- `SUPABASE_KEY` - Supabase service role key
- `HUGGING_FACE_API_KEY` - Hugging Face key (if using HF)

When you configure the GitHub Actions workflows, use the service-specific secret names (e.g., `RENDER_SERVICE_ID_FARMS` for the farms service). This lets the deploy job target the specific service on Render, and avoids accidental deploys to the wrong service.

- `SUPABASE_URL` and `SUPABASE_KEY`
- `HUGGING_FACE_API_KEY`

## Triggering via GitHub Actions
We use the Render REST API to trigger a deploy on push to `main` (see `.github/workflows/deploy-farms.yml` and `.github/workflows/deploy-auth.yml`). The GH Workflows install dependencies, run tests, and then trigger a deploy by POSTing to `https://api.render.com/v1/services/{serviceId}/deploys` with Authorization header `Bearer <RENDER_API_KEY>`.

### Sentry Release Tagging
Each deploy workflow automatically sets `SENTRY_RELEASE` via the Render Config Vars API using the current GitHub SHA before deployment. This ensures every deployed version is tagged in Sentry for accurate error tracking and source map resolution.

**How it works:**
1. Workflow runs and tests pass
2. "Set Sentry Release in Render Config Vars" step PATCHes the service environment with `SENTRY_RELEASE=<github.sha>`
3. Render deploys with the correct release identifier
4. Sentry error events are automatically grouped by release

No manual configuration needed — it happens automatically on every deploy.

## Tips
- Keep `SUPABASE_KEY` only as a Render environment variable and GitHub secret — do not expose it to the client.
- To set up staging vs production, create separate Render services or branches and map them to staging/prod.

## Synthetic Health Checks & Monitoring

The repository includes an automated synthetic health check workflow (`.github/workflows/synthetic-checks.yml`) that runs every 6 hours to verify service availability.

### What Gets Checked
- **Health endpoint**: `/healthz` (200 response required)
- **Weather service**: `GET /weather?lat=12.9&lon=80.2` 
- **AI recommendations**: `POST /ai/rec/` with sample crop data
- **Environments**: Both staging and production are checked independently

### Slack Notifications
When synthetic checks complete, a rich notification is sent to Slack with:
- **Status**: ✅ PASSED, ❌ FAILED, or ⚠️ PARTIAL
- **Color coding**: Green for success, red for failures, orange for partial
- **Per-environment breakdown**: Separate status for staging and production
- **Direct link**: Click through to the workflow run for details

**Setup**: Add `SLACK_WEBHOOK` secret to your GitHub repo with your Slack incoming webhook URL.

### GitHub Issues Escalation
When synthetic checks fail consecutively (2+ failures):
1. A GitHub Issue is automatically created with the `synthetic-check-failure` and `urgent` labels
2. Subsequent failures add comments to the existing issue with latest run details
3. Issues include:
   - Affected environments (staging/production)
   - Links to failing workflow runs
   - Guidance to investigate service health

**No additional setup required** — uses the default `GITHUB_TOKEN` from the workflow.

### Failure Recovery
- Open issues automatically close when checks pass again (manual closure recommended after investigating root cause)
- Each failure run includes a direct link to logs for debugging

## Rollbacks
- You can trigger a rollback to the last working release via the Render UI: `Service -> Deploys -> Revert`.

---
**End of Render setup**
