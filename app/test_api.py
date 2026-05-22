#!/usr/bin/env python3
"""
Minimal smoke test for the SWB API.

Usage:
1. Start the app locally.
2. Export SWB_USERNAME and SWB_PASSWORD in your shell.
3. Run: python test_api.py
"""

from http.cookiejar import CookieJar
import json
import os
from urllib.error import HTTPError
from urllib.request import HTTPCookieProcessor, Request, build_opener

BASE_URL = os.getenv("SWB_BASE_URL", "http://localhost:8000")
USERNAME = os.getenv("SWB_USERNAME", "swb-admin")
PASSWORD = os.getenv("SWB_PASSWORD", "")


def build_client():
    jar = CookieJar()
    return build_opener(HTTPCookieProcessor(jar))


def request_json(client, path, method="GET", payload=None, csrf_token=None):
    body = None
    headers = {"Content-Type": "application/json"}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
    if csrf_token:
        headers["X-CSRF-Token"] = csrf_token

    request = Request(f"{BASE_URL}{path}", data=body, headers=headers, method=method)
    with client.open(request) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    if not PASSWORD:
        raise SystemExit("Set SWB_PASSWORD before running the smoke test.")

    client = build_client()

    session = request_json(client, "/api/auth/session")
    print("Initial session:", session)

    request_json(
        client,
        "/api/auth/login",
        method="POST",
        payload={"username": USERNAME, "password": PASSWORD},
    )

    session = request_json(client, "/api/auth/session")
    csrf_token = session["csrfToken"]
    print("Authenticated session:", session)

    workshops = request_json(client, "/api/workshops")
    print("Workshop count:", workshops["stats"]["total"])

    created = request_json(
        client,
        "/api/workshops",
        method="POST",
        csrf_token=csrf_token,
        payload={
            "title": "Smoke Test Workshop",
            "category": "Testing",
            "status": "draft",
            "difficulty": "fundamentals",
            "duration_hours": 2,
            "summary": "A quick CRUD smoke test entry for the SWB dashboard.",
            "description": "This workshop exists purely to validate the local CRUD path.\nIt should be safe to delete afterwards.",
            "objectives": [
                "Validate login and CSRF handling.",
                "Create a workshop through the API."
            ],
            "stack": ["FastAPI", "Testing"],
            "published": False
        },
    )
    print("Created workshop:", created["workshop"]["title"])

    request_json(
        client,
        f"/api/workshops/{created['workshop']['id']}",
        method="DELETE",
        csrf_token=csrf_token,
    )
    print("Deleted smoke test workshop.")


if __name__ == "__main__":
    try:
        main()
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {error.code}: {body}")
