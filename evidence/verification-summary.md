# Verification Summary

## Functional Validation

- The application started successfully in the local environment after the container health check and shell line-ending issues were fixed.
- CRUD operations were validated locally.
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
