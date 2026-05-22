# Security Policy

## Supported use

This project is intended to be run with local or hosted environment variables for admin credentials and session secrets. Do not commit `.env` files or deployment secrets into the repository.

## Reporting a vulnerability

If you discover a security issue:

1. Do not open a public issue with exploit details.
2. Share a private report with reproduction steps, impact, and suggested mitigation.
3. Rotate any affected credentials before and after remediation if secrets were exposed.

## Hardening checklist

- Set `SWB_SESSION_HTTPS_ONLY=true` in HTTPS environments
- Restrict `SWB_ALLOWED_HOSTS` to the real deployment hostnames
- Prefer `SWB_ADMIN_PASSWORD_HASH` over a plain password
- Keep Dependabot and CodeQL enabled on GitHub
- Review pull requests before merging, especially changes touching auth, middleware, or API routes
