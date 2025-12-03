# GitHub Workflows for Render deployment

This folder contains GitHub Actions workflows used to CI/test and deploy services to Render.

Workflows:
- `deploy-farms.yml`: builds, runs tests, and triggers a Render deployment for the farms service.
- `deploy-auth.yml`: builds, runs tests, and triggers a Render deployment for the auth service.

To use these workflows:
1. Configure repo secrets: `RENDER_API_KEY`, `RENDER_SERVICE_ID_FARMS`, `RENDER_SERVICE_ID_AUTH`, `SUPABASE_URL`, `SUPABASE_KEY`, `HUGGING_FACE_API_KEY`.
2. If you prefer to use resource-specific secrets, set `RENDER_SERVICE_ID_FARMS` and `RENDER_SERVICE_ID_AUTH`.
3. Make sure you select `main` branch for deployments unless you use an alternate branch for staging.

Note: Workflows are conservative and run unit tests before triggering the deploy.
