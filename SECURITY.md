# Security Policy

## Supported Use

This repository is intended for portfolio review, local reproduction, and educational Azure deployment practice.

- Do not commit `.env` files, private keys, certificates, or cloud credentials.
- Treat the shipped environment examples as templates, not production values.
- Prefer managed secret storage such as Azure Key Vault for hosted environments.

## Reporting a Vulnerability

If you discover a vulnerability in the application bundle or the documented deployment pattern:

1. Do not open a public issue with exploit details.
2. Share a private report with impact, reproduction steps, and the affected files or controls.
3. Rotate any exposed credentials before and after remediation if secrets were involved.

## Baseline Controls Documented in This Repo

- Public/private subnet separation for the Azure workload
- No public IP on the PostgreSQL tier
- Restricted SSH source instead of broad administrative exposure
- NSG validation against the effective enforcement path
- Application-level controls for sessions, CSRF, trusted hosts, rate limiting, and security headers
- GitHub automation through CI, Dependabot, and CodeQL

## Residual Risks and Next Hardening Steps

The current portfolio phase intentionally stops short of full production hardening. Recommended follow-up work:

1. Add HTTPS termination and certificate management.
2. Move runtime secrets to Azure Key Vault.
3. Replace direct SSH with Bastion or Just-in-Time access.
4. Add centralized logging, alerting, and backup/restore validation.
