# Port Matrix

## Azure Runtime Flows

| Flow | Source | Destination | Port / Protocol | Exposure | Control | Reason |
| --- | --- | --- | --- | --- | --- | --- |
| Client traffic | Internet | API VM (`vm-api-learningsteps`) | `80/TCP` | Public | Effective NSG allow rule | Expose the FastAPI entry point |
| Admin access | Approved admin source `/32` | API VM (`vm-api-learningsteps`) | `22/TCP` | Restricted | SSH rule scoped to a single source | Limit remote administration |
| Application data path | API subnet `10.10.1.0/24` | DB VM (`vm-db-learningsteps`) | `5432/TCP` | Private | DB NSG allow rule from API subnet only | Permit PostgreSQL traffic from the app tier |
| Public access to DB | Internet | DB VM (`vm-db-learningsteps`) | Any | Denied | No public IP and no matching allow rule | Protect the database from direct exposure |

## Local Validation Flows

| Flow | Source | Destination | Port / Protocol | Reason |
| --- | --- | --- | --- | --- |
| Browser to local API | Local workstation | FastAPI app | `8000/TCP` | Validate the application locally |
| App to local PostgreSQL | Local app container / process | PostgreSQL container | `5432/TCP` | Validate CRUD and persistence before Azure deployment |

## Notes

- Exact validation IPs were intentionally removed from the public documentation because they were ephemeral or local-only.
- If the project evolves to HTTPS, add `443/TCP` for the public API path and document certificate ownership and renewal responsibilities.
