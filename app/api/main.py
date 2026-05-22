from contextlib import asynccontextmanager
from pathlib import Path
import logging

import asyncpg
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from config import load_settings
from middleware import BodySizeLimitMiddleware, SecurityHeadersMiddleware
from rate_limit import MemoryRateLimiter
from repositories.postgres_repository import PostgresDB
from routers.auth_router import router as auth_router
from routers.workshop_router import router as workshop_router
from services.workshop_service import WorkshopService

BASE_DIR = Path(__file__).resolve().parent
settings = load_settings()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("swb")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s", settings.app_name)
    pool = await asyncpg.create_pool(
        settings.database_url,
        min_size=1,
        max_size=5,
        command_timeout=15,
    )
    repository = PostgresDB(pool)
    await repository.ensure_schema()

    service = WorkshopService(repository)
    if settings.seed_demo_data:
        await service.seed_default_workshops()

    app.state.db_pool = pool
    app.state.settings = settings
    app.state.rate_limiter = MemoryRateLimiter()
    app.state.workshop_service = service

    try:
        yield
    finally:
        logger.info("Stopping %s", settings.app_name)
        await pool.close()


app = FastAPI(
    title=settings.app_name,
    description="Second-Workshop-Brain secure workshop dashboard",
    docs_url="/docs" if settings.enable_docs else None,
    redoc_url=None,
    openapi_url="/openapi.json" if settings.enable_docs else None,
    lifespan=lifespan,
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret,
    session_cookie="swb_session",
    same_site="lax",
    https_only=settings.session_https_only,
    max_age=settings.session_max_age_seconds,
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)
app.add_middleware(BodySizeLimitMiddleware, max_body_size=settings.max_request_size)
app.add_middleware(SecurityHeadersMiddleware, settings=settings)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.include_router(auth_router)
app.include_router(workshop_router)


@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
    return FileResponse(BASE_DIR / "templates" / "index.html")


@app.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}
