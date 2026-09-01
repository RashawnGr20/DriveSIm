import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

_missing = [name for name in ("DATABASE_URL", "SECRET_KEY") if not os.getenv(name)]
if _missing:
    raise RuntimeError(
        "Missing required environment variable(s): "
        + ", ".join(_missing)
        + ". Copy backend/.env.example to backend/.env and fill them in."
    )

from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from backend.database.connection import engine
from backend.database.models import Base
from backend.auth.router import router as auth_router
from backend.sessions.router import router as session_router
from backend.gaze.router import router as gaze_router
from backend.coaching.router import router as coaching_router
from backend.rate_limit import limiter

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

Base.metadata.create_all(engine)

@app.get("/")
def root():
    return{"message": "DriveSim API is running"}

app.include_router(auth_router)
app.include_router(session_router)
app.include_router(gaze_router)
app.include_router(coaching_router)
