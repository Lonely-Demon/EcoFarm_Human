# Solo Setup Guide: CI/CD for One Developer

**For:** Solo developer deploying to Render  
**Time:** ~1 hour setup, then automatic  
**Complexity:** Low - most things run automatically

---

## What You're Getting

**3 Automatic Features:**
1. ✅ **Sentry Release Tagging** - Every deploy auto-tags with commit SHA
2. ✅ **Slack Alerts** - Get notified every 6 hours if services are down
3. ✅ **GitHub Issues** - Auto-create issues if services fail 2+ times

All three work without you having to do anything after setup.

---

## Quick Start (30 Minutes)

### 1. Get Your Render API Key (2 min)
- Go to https://dashboard.render.com/api-tokens
- Create new token (keep it safe)
- Copy it

### 2. Get Your Service IDs (5 min)
For each service (farms, auth, ai-recs, weather):
1. Go to https://dashboard.render.com
2. Click service name
3. Click **More** → copy Service ID
4. Paste somewhere (you'll need 8 total)

### 3. Add GitHub Secrets (10 min)
Go to your repo → **Settings** → **Secrets and variables** → **Actions**

Add these 11 secrets:
```
RENDER_API_KEY = [your token from step 1]

RENDER_SERVICE_ID_FARMS = [from step 2]
RENDER_SERVICE_ID_AUTH = [from step 2]
RENDER_SERVICE_ID_AI_RECS = [from step 2]
RENDER_SERVICE_ID_FARMS_STAGING = [from step 2]
RENDER_SERVICE_ID_AUTH_STAGING = [from step 2]
RENDER_SERVICE_ID_AI_RECS_STAGING = [from step 2]
RENDER_SERVICE_ID_WEATHER_STAGING = [from step 2]

STAGING_BASE_URL = https://your-staging-domain.com
PROD_BASE_URL = https://your-prod-domain.com

SLACK_WEBHOOK = [optional - see below]
```

### 4. Create GitHub Labels (3 min - optional)
1. Go to repo → **Issues** → **Labels**
2. Create: `synthetic-check-failure` (red)
3. Create: `urgent` (red)

### 5. Test It (10 min)
```bash
# Make a test deploy
git push origin main

# Check GitHub Actions - should show green ✅
# Check Render dashboard - service should update ✅
```

**Done!** Now it runs automatically.

---

## How It Works (After Setup)

### Every Deploy
```
You: git push origin main
  ↓
Tests run ✅
  ↓
Sentry release tagged with commit SHA ✅
  ↓
Service deploys to Render ✅
  ↓
Errors in Sentry now grouped by version ✅
```

**Your action:** Nothing - it happens automatically

### Every 6 Hours
```
Synthetic checks run automatically ✅
  ↓
Tests: /healthz, /weather, /ai/rec ✅
  ↓
If all pass: Slack message says ✅ PASSED (green)
  ↓
If any fail: Slack message says ❌ FAILED (red)
  ↓
If fails 2+ times: GitHub Issue created automatically
```

**Your action:** Check Slack, click link to see what's wrong

---

## Slack Setup (Optional but Recommended)

### Get Slack Webhook URL
1. Go to https://api.slack.com/apps
2. Click "Create New App" → "From scratch"
3. Name: "EcoFarm CI/CD"
4. Choose your workspace
5. Go to **Incoming Webhooks** → Toggle ON
6. Click "Add New Webhook to Workspace"
7. Choose a channel (e.g., #alerts or #dev)
8. Copy the webhook URL
9. Add to GitHub secrets as `SLACK_WEBHOOK`

**Test it:**
```bash
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test message"}' \
  YOUR_WEBHOOK_URL
# Should see message in Slack ✅
```

---

## What to Do When Services Go Down

**Scenario:** You get a Slack alert saying ❌ FAILED

### Steps:
1. **Click the link** in the Slack message → See what failed
2. **Check which endpoint** is down (healthz, weather, or ai/rec)
3. **Go to Render dashboard** → Click service
4. **Look at logs** - see what's wrong
5. **Common fixes:**
   - Service crashed? Restart in Render UI
   - Code error? Check logs, fix code, push
   - Missing env var? Add to Render environment
   - External API down? Wait or switch to fallback

### If It Fails Twice:
- GitHub Issue auto-creates
- You get GitHub notification too
- Issue has direct links to failed runs
- Close issue after you fix it

---

## Manual Health Checks

### Test Your Endpoints
```bash
# Replace with your actual domains
STAGING="https://staging-api.ecofarm.com"
PROD="https://api.ecofarm.com"

# Test staging
curl -i $STAGING/healthz
curl -i "$STAGING/weather?lat=12.9&lon=80.2"
curl -X POST -H "Content-Type: application/json" \
  -d '{"lat":12.9,"lon":80.2,"preferred_crops":["tomato"]}' \
  -i $STAGING/ai/rec/

# Test production
curl -i $PROD/healthz
curl -i "$PROD/weather?lat=12.9&lon=80.2"
curl -X POST -H "Content-Type: application/json" \
  -d '{"lat":12.9,"lon":80.2,"preferred_crops":["tomato"]}' \
  -i $PROD/ai/rec/
```

All should return `200 OK`.

---

## Troubleshooting

### Deploy workflow failing
**Check:** GitHub Actions log → Look for error message
- `401 Unauthorized` → `RENDER_API_KEY` wrong or missing
- Tests failing → Fix code, push again
- Service ID wrong → Get correct ID from Render, update secret

### Slack not working
**Check:** Is `SLACK_WEBHOOK` set? Test it:
```bash
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test"}' \
  YOUR_WEBHOOK_URL
```
Should see message in Slack.

### Sentry not getting release tags
**Check:** Is `SENTRY_DSN` set in your Render service environment?

### GitHub Issue not creating
**Check:** Are the labels created in your repo? Create them manually if not.

---

## Customization

### Change Check Frequency
Edit `.github/workflows/synthetic-checks.yml`:
```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # Change 6 to your preferred hours
```

### Change Alert Threshold
Edit `.github/workflows/synthetic-checks.yml`:
```yaml
if [ "$FAILED_RUNS" -ge 2 ]; then  # Change 2 to your preferred number
```

### Disable Slack Alerts
Comment out in `.github/workflows/synthetic-checks.yml`:
```yaml
# - name: Post to Slack (optional)
```

### Disable GitHub Issues
Comment out in `.github/workflows/synthetic-checks.yml`:
```yaml
# - name: Check for repeated failures and escalate to GitHub Issues
```

---

## Monthly Maintenance

**Once a month, check:**
- [ ] GitHub secrets still valid (haven't rotated Render key?)
- [ ] Slack webhook still works
- [ ] Services deployed successfully last 30 days
- [ ] No recurring failures

---

## Daily Workflow

### Make a Deploy
```bash
# Your normal workflow
git add .
git commit -m "feature: something"
git push origin main

# That's it - deployment happens automatically
# Monitor in GitHub Actions tab
```

### Check Health
- **Slack:** Get alert every 6 hours automatically
- **GitHub Actions:** See all workflow runs
- **Render Dashboard:** Manual check anytime

### If Something's Wrong
1. Click Slack link → See logs
2. Go to Render → Check service status
3. Look at GitHub Actions for error details
4. Fix in code or Render config
5. Push and try again

---

## Files Modified by This Setup

**Automatically updated (you don't touch these):**
- `.github/workflows/deploy-farms.yml`
- `.github/workflows/deploy-auth.yml`
- `.github/workflows/deploy-ai-recs.yml`
- `.github/workflows/deploy-farms-staging.yml`
- `.github/workflows/deploy-auth-staging.yml`
- `.github/workflows/deploy-ai-recs-staging.yml`
- `.github/workflows/deploy-weather-staging.yml`
- `.github/workflows/synthetic-checks.yml`

**You configure manually (GitHub secrets only):**
- GitHub repository secrets (11 total)
- GitHub repository labels (2 total, optional)

---

## Emergency Procedures

### Service Down and You Can't Fix It
1. Go to Render dashboard
2. Click service
3. Go to **Deploys**
4. Find last known good version
5. Click **Revert** to go back
6. Fix the issue in code
7. Deploy again

### Want to Disable Monitoring Temporarily
Comment out in `.github/workflows/synthetic-checks.yml`:
```yaml
# All three can be independently disabled
# - name: Post to Slack (optional)
# - name: Check for repeated failures...
```

Then push and monitoring stops until you re-enable.

---

## Summary

**Setup Time:** 30 minutes (one-time)  
**Daily Action:** Just push code normally  
**Monitoring:** Automatic, alerted via Slack  
**Fixes:** Click link, check logs, fix code, push  

**You get:**
- ✅ Every deploy tagged in Sentry
- ✅ Automatic health checks every 6 hours
- ✅ Slack notifications when something's wrong
- ✅ GitHub issues for recurring problems
- ✅ Zero overhead after setup

---

## Questions?

**General help:** Check GitHub Actions workflow files to see what's happening  
**Render help:** https://render.com/docs  
**Sentry help:** https://docs.sentry.io/  
**Slack webhooks:** https://api.slack.com/messaging/webhooks

---

**That's it!** You're ready to deploy. 🚀
