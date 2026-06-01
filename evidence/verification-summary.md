# Verification Summary

## Functional Validation

- On May 22, 2026, the application startup path was revalidated locally with a real PostgreSQL container, a live FastAPI process, and direct HTTP checks against `/`, `/health`, and `/docs`.
- CRUD operations were validated locally with the smoke test in `app/test_api.py`, including login, session creation, workshop creation, and cleanup deletion.
- A live test uncovered a missing `itsdangerous` runtime dependency required by Starlette session handling, and that dependency was added to `app/api/requirements.txt`.
- Persistence was verified after a restart.

## Azure Reachability

- The API tier became externally reachable after correcting the effective HTTP ingress rule.
- Validation used the application endpoint and Azure network tests instead of relying on portal assumptions alone.

## Network Isolation

- The database tier stayed on the private subnet without a public IP.
- PostgreSQL access was limited to the API subnet on port `5432`.
- There was no intended direct internet path to the database tier.

## Administrative Hardening

- SSH access to the API VM was reduced to an approved `/32` source.
- Validation confirmed the approved source was allowed while a foreign source was denied.

## Documentation Hygiene

- Secrets were removed from the publishable surface.
- Ephemeral public IPs and personal admin IPs were intentionally omitted from the public evidence package.
