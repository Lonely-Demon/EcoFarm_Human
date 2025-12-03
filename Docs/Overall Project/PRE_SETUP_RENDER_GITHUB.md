# Pre-Setup: Create Render Services & GitHub Repo

Do these **before** following the main Solo Setup Guide.

---

## Part 1: Create GitHub Repository (5 minutes)

### Step 1: Create Empty Repo on GitHub (1 min)
1. Go to https://github.com/new
2. Repository name: `ecofarm-human` (or your preferred name)
3. Description: `Smart farming ecosystem - EcoFarm`
4. **Visibility:** Private (keep your code private)
5. **DO NOT** check "Add a README file"
6. Click **Create repository**

### Step 2: Push Your Existing Code via Terminal (3 min)

Open PowerShell in your project folder and run:

```powershell
# Navigate to your project folder
cd d:\Southern_Ring_Nebula\EcoFarm_Human

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "initial commit: ecofarm services"

# Add remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/ecofarm-human.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Done!** Your code is now on GitHub.

### If Git Isn't Installed
Download from: https://git-scm.com/download/win
Then restart PowerShell and try again.

---

## Part 2: Create Render Services (15 minutes)

You need to create **8 services** on Render:
- 4 for production (main branch): farms, auth, ai-recs, weather
- 4 for staging (dev branch): farms, auth, ai-recs, weather

### Quick Overview
```
Production (main branch)
├─ ecofarm-farms
├─ ecofarm-auth
├─ ecofarm-ai-recs
└─ ecofarm-weather

Staging (dev branch)
├─ ecofarm-farms-staging
├─ ecofarm-auth-staging
├─ ecofarm-ai-recs-staging
└─ ecofarm-weather-staging
```

### Create Each Service (Same Process)

**Repeat this 8 times** (once per service):

1. **Go to Render:** https://dashboard.render.com
2. **Click:** New → Web Service
3. **Connect GitHub:** Select your repo
4. **Set Configuration:**
   - **Name:** `ecofarm-farms` (or auth, ai-recs, weather)
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn services.farms.main:app --host 0.0.0.0 --port $PORT`
     - For auth: `uvicorn services.auth.main:app --host 0.0.0.0 --port $PORT`
     - For ai-recs: `uvicorn services.ai_recs.main:app --host 0.0.0.0 --port $PORT`
     - For weather: `uvicorn services.weather.main:app --host 0.0.0.0 --port $PORT`
   - **Branch:** `main` (for production) or `dev` (for staging)
   - **Plan:** Free (or paid if you prefer)

5. **Click:** Create Web Service

6. **After Deployed:**
   - Click service → Click **More** → Copy **Service ID**
   - Save this ID (you'll need it for GitHub secrets)

### Get Your Service IDs

After creating all 8 services, you should have 8 IDs that look like:
```
srv_1abc2def3ghi4jkl
srv_2def3ghi4jkl5mno
...etc
```

Save them in a text file for the next step.

---

## Environment Variables in Render

For **each service**, go to **Environment** tab and add:

### For All Services
```
SUPABASE_URL = https://your-project.supabase.co
SUPABASE_KEY = your_service_role_key
DATABASE_URL = postgresql://user:pass@host:5432/dbname
SENTRY_DSN = https://your-sentry-dsn@sentry.io/project
SENTRY_ENV = staging (for staging services) or production (for prod)
```

### For Weather Service Only
```
OPEN_METEO_URL = https://api.open-meteo.com
```

### For AI Recs Service Only
```
HUGGING_FACE_API_KEY = hf_your_token
```

**Note:** Don't set `SENTRY_RELEASE` - the CI/CD workflow will set it automatically.

---

## Part 3: Back to Solo Setup Guide

Once you have:
- ✅ GitHub repo created and code pushed
- ✅ 8 Render services created
- ✅ 8 Service IDs saved

**Then go back to [SOLO_SETUP_GUIDE.md](./SOLO_SETUP_GUIDE.md) and continue from Step 1.**

---

## Quick Checklist

### GitHub
- [ ] Repo created at https://github.com
- [ ] Code pushed to main branch
- [ ] Can see files at github.com/username/ecofarm-human

### Render Services Created
- [ ] ecofarm-farms (main branch)
- [ ] ecofarm-auth (main branch)
- [ ] ecofarm-ai-recs (main branch)
- [ ] ecofarm-weather (main branch)
- [ ] ecofarm-farms-staging (dev branch)
- [ ] ecofarm-auth-staging (dev branch)
- [ ] ecofarm-ai-recs-staging (dev branch)
- [ ] ecofarm-weather-staging (dev branch)

### Service IDs Saved
- [ ] All 8 service IDs copied and saved
- [ ] Environment vars added to each service

### Ready for Next Step
- [ ] Go to: [SOLO_SETUP_GUIDE.md](./SOLO_SETUP_GUIDE.md)
- [ ] Follow steps 1-5 with your service IDs

---

**Next:** Follow [SOLO_SETUP_GUIDE.md](./SOLO_SETUP_GUIDE.md) starting from Step 1.
