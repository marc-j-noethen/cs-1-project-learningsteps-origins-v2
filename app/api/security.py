import base64
import hashlib
import hmac
import os
import re
import secrets
import unicodedata

PBKDF2_ITERATIONS = 390000


def generate_csrf_token() -> str:
    return secrets.token_urlsafe(32)


def generate_password_hash(password: str, iterations: int = PBKDF2_ITERATIONS) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return (
        "pbkdf2_sha256"
        f"${iterations}"
        f"${base64.urlsafe_b64encode(salt).decode('ascii')}"
        f"${base64.urlsafe_b64encode(digest).decode('ascii')}"
    )


def verify_password(
    password: str,
    password_hash: str | None = None,
    plain_password: str | None = None,
) -> bool:
    if password_hash:
        try:
            algorithm, iteration_value, salt_value, digest_value = password_hash.split("$", 3)
        except ValueError:
            return False

        if algorithm != "pbkdf2_sha256":
            return False

        derived = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            base64.urlsafe_b64decode(salt_value.encode("ascii")),
            int(iteration_value),
        )
        expected = base64.urlsafe_b64decode(digest_value.encode("ascii"))
        return hmac.compare_digest(derived, expected)

    if plain_password is None:
        return False

    return hmac.compare_digest(password, plain_password)


def slugify_title(title: str) -> str:
    normalized = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")
    return slug[:80] or "workshop"
