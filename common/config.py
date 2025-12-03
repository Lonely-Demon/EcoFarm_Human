import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_KEY", "")
    HUGGING_FACE_API_KEY: str = os.getenv("HUGGING_FACE_API_KEY", "")
    OPEN_METEO_URL: str = os.getenv("OPEN_METEO_URL", "https://api.open-meteo.com")
    # Sentry
    SENTRY_DSN: str = os.getenv('SENTRY_DSN', '')
    SENTRY_ENV: str = os.getenv('SENTRY_ENV', 'development')
    SENTRY_RELEASE: str = os.getenv('SENTRY_RELEASE', os.getenv('GITHUB_SHA', 'dev'))

settings = Settings()
