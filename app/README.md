# SWB | Second-Workshop-Brain

SWB is a secure workshop dashboard and knowledge base for building, curating, and maintaining your own workshop library. The interface is inspired by the three-column structure of the Docker Docs workshop pages and is tailored for topics such as Fullstack, SaaS, Git, GitHub, Docker, and Kubernetes.

## What you get

- Docker-Docs-inspired UI with left workshop navigation, central workshop content, and right-side metadata plus security notes
- Authenticated CRUD for workshops with create, edit, and delete flows
- Dark and light mode with local theme persistence
- FastAPI backend with PostgreSQL storage
- Security defaults for GitHub-ready sharing:
  session auth, CSRF validation, trusted hosts, strict security headers, request size limits, and write/login rate limiting
- Demo seed content so the dashboard looks complete on first run

## Stack

- FastAPI
- asyncpg
- PostgreSQL
- Plain HTML, CSS, and JavaScript served by the API

## Quick start

1. Copy `.env.example` to `.env`.
2. Fill in these required values locally:
   - `SWB_ADMIN_PASSWORD` or `SWB_ADMIN_PASSWORD_HASH`
   - `SESSION_SECRET`
3. Start the database via the included devcontainer/docker-compose setup.
4. Run `./start.sh`.
5. Open [http://localhost:8000](http://localhost:8000).

## Local security setup

The app intentionally refuses to start if the admin credential or session secret is missing.

### Option A: simple local password

Set this in `.env`:

```env
SWB_ADMIN_USERNAME=swb-admin
SWB_ADMIN_PASSWORD=your-strong-local-password
SESSION_SECRET=replace-this-with-a-long-random-secret
```

### Option B: hashed password

Generate a password hash locally:

```bash
python api/tools/generate_password_hash.py "your-strong-password"
```

Then place the output into:

```env
SWB_ADMIN_PASSWORD_HASH=pbkdf2_sha256$...
SESSION_SECRET=replace-this-with-a-long-random-secret
```

## GitHub-ready security defaults

- No secrets are committed; `.env` stays ignored
- No open write endpoints without authentication
- All write routes require CSRF headers
- `Content-Security-Policy`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`, and `nosniff` headers are sent on every response
- Login attempts and write actions are rate-limited
- The frontend uses safe DOM APIs instead of injecting raw HTML from workshop content
- API docs are disabled by default

## GitHub automation

This repo now includes:

- Dependabot config for Python dependencies and GitHub Actions
- CI workflow for syntax and unit checks
- CodeQL workflow for static security analysis
- `SECURITY.md` for responsible disclosure guidance

## Useful files

- [api/main.py](api/main.py)
- [api/static/styles.css](api/static/styles.css)
- [api/static/app.js](api/static/app.js)
- [api/models/workshop.py](api/models/workshop.py)
- [api/security.py](api/security.py)

## Notes for deployment

- Set `SWB_SESSION_HTTPS_ONLY=true` behind HTTPS
- Replace `SWB_ALLOWED_HOSTS` with your real domain list
- Keep `SWB_ENABLE_DOCS=false` unless you explicitly need OpenAPI docs
- Prefer `SWB_ADMIN_PASSWORD_HASH` over a plain password in hosted environments
