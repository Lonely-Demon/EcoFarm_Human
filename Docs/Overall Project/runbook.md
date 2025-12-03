# Runbook for EcoFarm_Human MVP

This runbook is a quick reference for operations, outages, and restart procedures for the Render-hosted FastAPI services and Supabase.

## Quick checks if a service is down
1. Check the Render service dashboard for health checks and recent deployments.
2. Check service logs on Render for exceptions.
3. Check Supabase status & recent errors (query failures, storage errors).
4. Check GitHub Actions to see if a deployment failed.

## Restart a service (Render)
1. Login to Render Dashboard.
2. Navigate to the service, click `Manual Deploy` or `Retry Build`.
3. If the problem is networking or secrets, update environment variables and redeploy.

## Database issues
- If queries are slow or failing, check: 
  - Supabase metrics (connection count, CPU, I/O). 
  - Slow queries & missing indexes. Add indexes then re-run.
- For accidental data deletion:
  - If within retention & backup policies, restore from backups (Supabase snapshots). If snapshots unavailable, use staged data or request a restore.

## Clear cache or re-seed
- Some services use caching (Redis or in-process cache). To re-seed:
  - Use `POST /debug/seed?env=staging` (if implemented) or run migration + seed scripts.

## Handling increased costs or unexpected bills
- Check the provider's usage details (Render Billing dashboard & Hugging Face usage page).
- Enable billing alerts for Supabase and Hugging Face and cap the inference usage per day as a stop-gap measure.

## Quick rollback procedure on failed deploy
1. Use Render's deployment history to roll back to previous working revision.
2. If the DB schema changed and is incompatible, restore a DB snapshot and run migrations on the previous release.

## Viewing logs & errors
- Render shows logs per deployment; use the console to view errors.
- For traceback, check Sentry or the provider of your error capturing tool.

## Regulatory & Data Requests
- For data deletion requests (GDPR-like): follow `docs/data-privacy-and-risk.md` for the steps to remove PII & images.
- Data export requests: run `psql` or Supabase SQL to export user-related data.

## Recovery & Escalation
- If a critical service is failing and not recoverable: escalate to a designated developer and open an incident in a ticketing system (or shared channel).
- Document every step taken and time of actions in a team-run document.

## Contact points
- Primary developer: [TBD]
- Secondary: [TBD]
- Supabase support contact: https://supabase.com/docs/support
- Render support contact: https://render.com/support

## Runbook updates
- Every major deploy or change in infra should update the runbook and the `docs/` folder with new operational instructions.
