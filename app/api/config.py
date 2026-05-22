from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


def _to_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _to_list(value: str | None, default: list[str]) -> list[str]:
    if not value:
        return default
    items = [item.strip() for item in value.split(",")]
    return [item for item in items if item]


def _is_placeholder(value: str | None) -> bool:
    if not value:
        return True
    return value.lower() in {"change-me", "change-me-now", "replace-me", "your-secret"}


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_env: str
    database_url: str
    admin_username: str
    admin_password: str | None
    admin_password_hash: str | None
    session_secret: str
    session_https_only: bool
    session_max_age_seconds: int
    allowed_hosts: list[str]
    seed_demo_data: bool
    enable_docs: bool
    max_request_size: int
    login_rate_limit: int
    write_rate_limit: int


def load_settings() -> Settings:
    app_name = os.getenv("SWB_APP_NAME", "SWB | Second-Workshop-Brain")
    app_env = os.getenv("APP_ENV", "development").strip().lower()
    database_url = os.getenv("DATABASE_URL", "").strip()
    admin_username = os.getenv("SWB_ADMIN_USERNAME", "swb-admin").strip()
    admin_password = os.getenv("SWB_ADMIN_PASSWORD")
    admin_password_hash = os.getenv("SWB_ADMIN_PASSWORD_HASH")
    session_secret = os.getenv("SESSION_SECRET", "").strip()

    if not database_url:
        raise ValueError("DATABASE_URL environment variable is required.")

    if _is_placeholder(session_secret) or len(session_secret) < 32:
        raise ValueError(
            "SESSION_SECRET must be set to a strong value with at least 32 characters."
        )

    if not admin_username:
        raise ValueError("SWB_ADMIN_USERNAME must not be empty.")

    if not admin_password_hash and not admin_password:
        raise ValueError(
            "Set SWB_ADMIN_PASSWORD or SWB_ADMIN_PASSWORD_HASH before starting the app."
        )

    return Settings(
        app_name=app_name,
        app_env=app_env,
        database_url=database_url,
        admin_username=admin_username,
        admin_password=admin_password,
        admin_password_hash=admin_password_hash,
        session_secret=session_secret,
        session_https_only=_to_bool(os.getenv("SWB_SESSION_HTTPS_ONLY"), False),
        session_max_age_seconds=int(os.getenv("SWB_SESSION_MAX_AGE_SECONDS", "43200")),
        allowed_hosts=_to_list(
            os.getenv("SWB_ALLOWED_HOSTS"),
            ["localhost", "127.0.0.1", "testserver"],
        ),
        seed_demo_data=_to_bool(os.getenv("SWB_SEED_DEMO_DATA"), True),
        enable_docs=_to_bool(os.getenv("SWB_ENABLE_DOCS"), False),
        max_request_size=int(os.getenv("SWB_MAX_REQUEST_SIZE", "65536")),
        login_rate_limit=int(os.getenv("SWB_LOGIN_RATE_LIMIT", "5")),
        write_rate_limit=int(os.getenv("SWB_WRITE_RATE_LIMIT", "45")),
    )
