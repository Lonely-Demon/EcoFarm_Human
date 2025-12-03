# Synthetic Checks Failure Runbook

Quick reference guide for responding to synthetic health check failures.

## Alert Flow

```
Synthetic Checks Run (every 6 hours)
    ↓
[Endpoint Checks: /healthz, /weather, /ai/rec]
    ↓
    ├─ PASS → ✅ Slack: Green "PASSED" message
    │
    └─ FAIL → ❌ Slack: Red "FAILED" message
              ↓
         [Count consecutive failures]
              ↓
         2+ failures? → Create/Update GitHub Issue
              ↓
         Issue labeled: "synthetic-check-failure" + "urgent"
```

## Response Checklist

### When You Get a Slack Alert

1. **Check the Status** 
   - ✅ PASSED → No action needed
   - ❌ FAILED → Investigate
   - ⚠️ PARTIAL → One environment down

2. **Read the Message Details**
   - Which environment failed? (Staging / Production / Both)
   - Click the workflow link for logs
   - Find which endpoint failed (healthz, weather, or ai/rec)

3. **Get More Info**
   - Click the workflow link to see detailed error logs
   - Look for HTTP status codes and error messages
   - Check if it's consistent across both check runs

### If Failure is Isolated (Single run)

**Likely Causes:**
- Temporary network glitch
- Service brief downtime
- Rate limiting

**Action:**
- Wait for next scheduled run (6 hours) to confirm
- Check Render dashboard for recent deployments
- Monitor Sentry for error spikes

### If Failure is Repeated (2+ consecutive runs)

**A GitHub Issue will be automatically created.** Severity: 🚨 URGENT

**Immediate Response:**

1. **Open the GitHub Issue** 
   - Issue title: "🚨 Synthetic Health Checks Failing"
   - Labels: `synthetic-check-failure`, `urgent`

2. **Identify Affected Endpoints** (from issue body)
   ```
   Staging: failure
   Production: success  ← Only staging down
   ```
   or
   ```
   Staging: failure
   Production: failure  ← Both environments down (critical!)
   ```

3. **Determine Root Cause**

   **Is it a deployment issue?**
   - Check Render dashboard → Latest deploy status
   - Look for failed builds or crashes
   - Review recent commits that deployed
   
   **Is it a resource issue?**
   - Check Render service metrics (CPU, memory, disk)
   - Look for any resource limit warnings
   
   **Is it an external dependency?**
   - Check if Supabase/database is accessible
   - Verify API keys haven't expired
   - Test Hugging Face / Open Meteo connectivity
   
   **Is it a code issue?**
   - Check recent changes to:
     - `/healthz` endpoint handler
     - `/weather` endpoint
     - `/ai/rec` endpoint
   - Run tests locally to confirm

4. **Implement Fix**

   **If it's a code issue:**
   ```bash
   # Fix the issue
   git checkout -b fix/health-check-failure
   # Make changes
   git push origin fix/health-check-failure
   # Create PR, get review
   # Merge to main (or dev for staging)
   ```

   **If it's a deployment/config issue:**
   - Fix environment variables in Render
   - Restart the service
   - Monitor next synthetic check run

   **If it's an external API issue:**
   - Update fallback logic or circuit breakers
   - Add retry logic if missing
   - Update status page / notify users

5. **Verify Recovery**
   - Monitor next scheduled check run (within 6 hours)
   - Or manually trigger: `gh workflow run synthetic-checks.yml`
   - When fixed: GitHub Issue will still be open → close manually with comment:
     ```
     **Resolution**: Fixed via [PR #123]
     - Issue: [Brief description]
     - Root Cause: [What was wrong]
     - Solution: [What was done]
     ```

## Accessing Logs

### From Slack Alert
- Click "View Details" link in the Slack message
- Goes directly to the workflow run

### From GitHub
- Repository → **Actions** tab
- Select **Synthetic Health Checks** workflow
- Click the failed run
- Scroll down to see individual step output

### Look For These Details in Logs

```
❌ Health check failed for https://api.example.com
   └─ HTTP Status: 503 (vs expected 200)
   └─ Response body: [error details]

❌ Weather check failed for https://api.example.com/weather?lat=12.9&lon=80.2
   └─ HTTP Status: 500
   └─ This suggests: Database error, API key invalid, or service crashed

❌ AI recs check failed for https://api.example.com/ai/rec/
   └─ HTTP Status: 502 (Bad Gateway)
   └─ This suggests: Hugging Face API down or timeout
```

## Common Failure Scenarios

### Scenario 1: "Connection refused" or 503
**Likely Issue:** Service crashed or isn't running

**Steps:**
1. Go to Render dashboard → Select service
2. Check service status (should be "Live")
3. Look at deploy history — did it just deploy?
4. Check logs for startup errors
5. Restart service if hung: **Settings** → **Restart**

### Scenario 2: "Endpoint not found" (404)
**Likely Issue:** Health check endpoint path is wrong or changed

**Steps:**
1. Verify endpoint exists in your code:
   ```python
   @app.get("/healthz")
   def health_check():
       return {"status": "ok"}
   ```
2. Check if path was recently renamed
3. Update synthetic-checks.yml if endpoint changed
4. Redeploy

### Scenario 3: "Request timeout"
**Likely Issue:** Service is too slow or hanging

**Steps:**
1. Check Render service metrics for high CPU/memory
2. Look at request logs — are requests hanging?
3. Check if database queries are slow
4. Scale up resource limits in Render if needed

### Scenario 4: "500 Server Error"
**Likely Issue:** Code error, bad config, or missing dependency

**Steps:**
1. Check Sentry error dashboard (if configured) — see actual error
2. Review logs for Python stack trace
3. Check environment variables are set correctly
4. Run tests locally to reproduce

### Scenario 5: Only Staging Failing, Prod OK
**Likely Issue:** Staging has stale deploy or different config

**Steps:**
1. Compare Render env vars between staging and prod
2. Check if staging service needs redeploy
3. Verify staging branch (usually `dev`) is in sync
4. Check if test data is missing

## Escalation

**If you can't fix it in 30 minutes:**
1. Post in #incidents Slack channel (if exists)
2. Tag the team lead or on-call engineer
3. Document what you've tried so far
4. Create a note in the GitHub Issue

**If it's a production outage lasting 10+ minutes:**
1. Consider automated rollback via Render UI
2. Notify stakeholders of ongoing incident
3. Keep GitHub Issue updated with status

## Prevention

### Before Pushing to Main
```bash
# Run all tests locally
pytest -v

# Check endpoints manually
curl http://localhost:8000/healthz
curl http://localhost:8000/weather?lat=12.9&lon=80.2
```

### In Code Reviews
- Ensure `/healthz` is always responsive and lightweight
- Watch for newly added external API calls that could fail
- Verify all env vars have sensible defaults

### Configuration
- Keep `SENTRY_DSN` and `HUGGING_FACE_API_KEY` in secrets, never hardcoded
- Set resource limits in Render appropriate to expected load
- Enable autoscaling if traffic spikes are expected

---

**Questions?** Check `render-setup.md` for architecture overview or reach out to the team.
