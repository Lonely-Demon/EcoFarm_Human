# Pre-Launch Verification Checklist

Complete this checklist before going live with the CI/CD pipeline.

## GitHub Secrets ✅

### Render Configuration
- [ ] `RENDER_API_KEY` - Retrieved from Render API tokens page
- [ ] `RENDER_SERVICE_ID_FARMS` - Verified in Render dashboard
- [ ] `RENDER_SERVICE_ID_AUTH` - Verified in Render dashboard
- [ ] `RENDER_SERVICE_ID_AI_RECS` - Verified in Render dashboard
- [ ] `RENDER_SERVICE_ID_FARMS_STAGING` - Verified in Render dashboard
- [ ] `RENDER_SERVICE_ID_AUTH_STAGING` - Verified in Render dashboard
- [ ] `RENDER_SERVICE_ID_AI_RECS_STAGING` - Verified in Render dashboard
- [ ] `RENDER_SERVICE_ID_WEATHER_STAGING` - Verified in Render dashboard

### Monitoring & Alerting
- [ ] `SLACK_WEBHOOK` - Created and tested in Slack workspace
- [ ] `STAGING_BASE_URL` - Points to actual staging environment
- [ ] `PROD_BASE_URL` - Points to actual production environment

### Verification Steps for Each Secret
```bash
# For RENDER_API_KEY - Test with curl:
curl -H "Authorization: Bearer YOUR_RENDER_API_KEY" \
  https://api.render.com/v1/services | jq '.services | length'
# Should return a number > 0

# For service IDs - Visit Render UI and verify each service:
# https://dashboard.render.com → Select Service → Settings → Copy ID

# For URLs - Test endpoints:
curl https://staging-base-url.com/healthz  # Should return 200
curl https://prod-base-url.com/healthz      # Should return 200
```

## Environment Variables in Render ✅

For **each service** (farms, auth, weather, ai-recs), verify these are set:

### Required for All Services
- [ ] `SUPABASE_URL` - Set and matches your Supabase project
- [ ] `SUPABASE_KEY` - Set (service role key, never expose to client)
- [ ] `SENTRY_DSN` - (Optional) Sentry project DSN if using error tracking
- [ ] `SENTRY_ENV` - (Optional) Set to "staging" or "production"

### Per-Service Specific
**Weather Service:**
- [ ] `OPEN_METEO_URL` - Set to `https://api.open-meteo.com`

**AI Recs Service:**
- [ ] `HUGGING_FACE_API_KEY` - Set if using Hugging Face models

**All Services:**
- [ ] Verify `SENTRY_RELEASE` is NOT manually set (workflows will set it)

## Health Check Endpoints ✅

Test each health check endpoint manually:

```bash
# Replace with your actual URLs
BASE_URL_STAGING="https://staging-api.ecofarm.com"
BASE_URL_PROD="https://api.ecofarm.com"

# Staging
curl -i $BASE_URL_STAGING/healthz
curl -i "$BASE_URL_STAGING/weather?lat=12.9&lon=80.2"
curl -X POST -H "Content-Type: application/json" \
  -d '{"lat":12.9,"lon":80.2,"preferred_crops":["tomato"]}' \
  -i $BASE_URL_STAGING/ai/rec/

# Production
curl -i $BASE_URL_PROD/healthz
curl -i "$BASE_URL_PROD/weather?lat=12.9&lon=80.2"
curl -X POST -H "Content-Type: application/json" \
  -d '{"lat":12.9,"lon":80.2,"preferred_crops":["tomato"]}' \
  -i $BASE_URL_PROD/ai/rec/
```

**Expected Results:**
- [ ] All `/healthz` endpoints return `200 OK`
- [ ] `/weather` endpoints return `200 OK` with weather data
- [ ] `/ai/rec` endpoints return `200 OK` with crop recommendations
- [ ] No `401`, `403`, or `500` errors

## Workflow Dry Runs ✅

### Test Deploy Workflow
1. [ ] Create a test branch: `git checkout -b test/ci-setup`
2. [ ] Make a trivial change: `echo "# test" >> README.md`
3. [ ] Push: `git push origin test/ci-setup`
4. [ ] Create PR to `main` (don't merge yet)
5. [ ] Verify workflow runs in **Actions** tab
6. [ ] Check for errors (should show green or expected failures)
7. [ ] Delete branch

**What to check in workflow output:**
- [ ] Tests pass (or are skipped if no tests)
- [ ] No "401 Unauthorized" errors on Render API calls
- [ ] "Set Sentry Release in Render Config Vars" step succeeds
- [ ] Deploy to Render is triggered

### Test Synthetic Checks Manually
```bash
# Navigate to your repo
cd /path/to/repo

# Manually trigger the synthetic checks workflow
gh workflow run synthetic-checks.yml

# Wait ~2 minutes, then check results
gh run list --workflow=synthetic-checks.yml --limit=1

# View details
gh run view <RUN_ID> --log
```

**What to check:**
- [ ] Both staging and production checks run
- [ ] All three endpoint checks pass (or expected failure for one)
- [ ] Slack notification arrives in your test channel
- [ ] No GitHub Issue is created (unless checks actually fail)

## Slack Integration ✅

1. [ ] Test webhook manually:
```bash
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test message from CI/CD"}' \
  $YOUR_SLACK_WEBHOOK_URL
# Should see message appear in Slack channel
```

2. [ ] Configure notification channel:
   - [ ] Create #deploys or #alerts channel in Slack
   - [ ] (Optional) Set up Do Not Disturb rules for off-hours
   - [ ] Invite team members who should monitor

3. [ ] Test rich message format:
   - [ ] Run synthetic checks manually and verify Slack message displays correctly
   - [ ] Check that color coding works (green/red/orange)
   - [ ] Verify links are clickable

## GitHub Issues Setup ✅

1. [ ] Create label in GitHub:
   - [ ] Go to repo → Issues → Labels
   - [ ] Create `synthetic-check-failure` label (red color)
   - [ ] Create `urgent` label (red/dark color)

2. [ ] Test issue creation:
   - [ ] Manually edit synthetic-checks.yml to always fail (for testing)
   - [ ] Push and trigger workflow twice
   - [ ] Verify GitHub Issue is created automatically with correct labels
   - [ ] Revert the test changes

## Documentation ✅

- [ ] `render-setup.md` is updated and accurate
- [ ] `GITHUB_SECRETS_SETUP.md` is reviewed
- [ ] `SYNTHETIC_CHECKS_RUNBOOK.md` is available to team
- [ ] Team members know where to find these docs
- [ ] All URLs in docs are current (staging, prod, dashboard links)

## Team Readiness ✅

- [ ] Assign an on-call rotation for handling synthetic check failures
- [ ] Brief team on the runbook procedures
- [ ] Set up Slack channel alerts
- [ ] Create incident response template (if doesn't exist)
- [ ] Document escalation path (who to notify if prod is down)

## Production Rollout ✅

1. [ ] All checks above are passing
2. [ ] Team is confident with the runbook
3. [ ] Slack notifications are being received
4. [ ] Test a real deploy to ensure no surprises:
   - [ ] Make a small, safe change to a service
   - [ ] Push to `main` or `dev` (depending on target)
   - [ ] Observe deploy workflow complete successfully
   - [ ] Verify service deployed on Render
   - [ ] Verify Sentry release was tagged
   - [ ] Monitor next synthetic check run

## Go/No-Go Decision

**Go Live:**
- All checkboxes above are complete ✅
- No blocker issues identified
- Team is trained and confident

**Not Ready / Hold:**
- Any security concerns (secrets exposed, permissions too broad)
- Endpoints failing health checks
- Team feedback indicates need for more preparation

---

**Sign-Off**

| Role | Name | Date | Status |
|------|------|------|--------|
| Engineer | | | ☐ Approve |
| Tech Lead | | | ☐ Approve |
| On-Call | | | ☐ Acknowledge |

Once all sign-offs are complete, the CI/CD pipeline is ready for production! 🚀
