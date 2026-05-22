import hmac

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field, field_validator

from config import Settings
from dependencies import enforce_login_rate_limit, get_settings, require_authenticated, require_csrf
from security import generate_csrf_token, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("username", mode="before")
    @classmethod
    def normalize_username(cls, value: str) -> str:
        return value.strip()


@router.get("/session")
async def get_session(request: Request) -> dict[str, str | bool | None]:
    authenticated = bool(request.session.get("authenticated"))
    return {
        "authenticated": authenticated,
        "username": request.session.get("username"),
        "csrfToken": request.session.get("csrf_token") if authenticated else None,
    }


@router.post("/login", dependencies=[Depends(enforce_login_rate_limit)])
async def login(
    payload: LoginRequest,
    request: Request,
    settings: Settings = Depends(get_settings),
) -> dict[str, str]:
    valid_username = hmac.compare_digest(payload.username, settings.admin_username)
    valid_password = verify_password(
        payload.password,
        password_hash=settings.admin_password_hash,
        plain_password=settings.admin_password,
    )

    if not valid_username or not valid_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    request.session.clear()
    request.session.update(
        {
            "authenticated": True,
            "username": settings.admin_username,
            "csrf_token": generate_csrf_token(),
        }
    )
    return {"detail": "Login successful."}


@router.post(
    "/logout",
    dependencies=[Depends(require_authenticated), Depends(require_csrf)],
)
async def logout(request: Request) -> dict[str, str]:
    request.session.clear()
    return {"detail": "Logout successful."}
