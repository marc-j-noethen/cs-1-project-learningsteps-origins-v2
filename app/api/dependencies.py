import hmac

from fastapi import Depends, HTTPException, Request, status

from config import Settings
from services.workshop_service import WorkshopService


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_workshop_service(request: Request) -> WorkshopService:
    return request.app.state.workshop_service


def _get_client_address(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    if request.client and request.client.host:
        return request.client.host
    return "unknown"


async def require_authenticated(request: Request) -> None:
    if not request.session.get("authenticated"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )


async def require_csrf(request: Request) -> None:
    session_token = request.session.get("csrf_token")
    request_token = request.headers.get("x-csrf-token", "")
    if not session_token or not hmac.compare_digest(session_token, request_token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF validation failed.",
        )


async def enforce_login_rate_limit(
    request: Request,
    settings: Settings = Depends(get_settings),
) -> None:
    limiter = request.app.state.rate_limiter
    key = f"login:{_get_client_address(request)}"
    if not limiter.check(key, settings.login_rate_limit, 600):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Try again in a few minutes.",
        )


async def enforce_write_rate_limit(
    request: Request,
    settings: Settings = Depends(get_settings),
) -> None:
    limiter = request.app.state.rate_limiter
    key = f"write:{_get_client_address(request)}"
    if not limiter.check(key, settings.write_rate_limit, 60):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Write rate limit exceeded. Slow down and try again.",
        )
