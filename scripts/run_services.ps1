# Start services manually (PowerShell)
# Usage: ./scripts/run_services.ps1

$env:DATABASE_URL = "sqlite:///./dev.db"
$env:SUPABASE_URL = ""
$env:SUPABASE_KEY = ""

Start-Process -NoNewWindow uvicorn -ArgumentList "services.auth.main:app --reload --port 8000"
Start-Process -NoNewWindow uvicorn -ArgumentList "services.farms.main:app --reload --port 8002"
Start-Process -NoNewWindow uvicorn -ArgumentList "services.weather.main:app --reload --port 8001"
Start-Process -NoNewWindow uvicorn -ArgumentList "services.ai_recs.main:app --reload --port 8003"
Start-Process -NoNewWindow streamlit -ArgumentList "run services/streamlit_demo/app.py"
