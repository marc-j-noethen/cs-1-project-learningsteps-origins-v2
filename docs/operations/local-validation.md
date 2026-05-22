# Local Validation

## Goal

Prove the application works locally before troubleshooting Azure.

## What Was Validated

1. The PostgreSQL service could run healthy in the local container workflow.
2. The startup script could launch the FastAPI application successfully.
3. CRUD operations worked end to end.
4. Data persisted after a restart.

## Key Fixes Captured During Local Work

- The PostgreSQL health check needed to call `pg_isready` with an explicit user.
- `start.sh` needed Unix line endings so it could execute correctly inside the Linux-based Dev Container.

## Repeatable Validation Flow

1. Copy [`.env.example`](../../.env.example) to `app/.env`.
2. Start the local PostgreSQL dependency from `app/.devcontainer/docker-compose.yml`.
3. In `app/`, run:

```bash
./start.sh
```

4. Open the app locally at `http://localhost:8000`.
5. If `SWB_ENABLE_DOCS=true`, verify:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

6. Run the smoke test with local credentials:

```bash
export SWB_PASSWORD="<local-admin-password>"
python test_api.py
```

## Expected Outcomes

- FastAPI reports successful startup
- `GET /health` returns `{"status":"ok",...}`
- Create/read/delete flows succeed through `test_api.py`
- Restarting the app does not lose persisted data

## Why This Phase Matters

Local validation reduces false assumptions in the cloud phase. If the application, environment variables, or persistence model are already broken locally, Azure only hides the real problem behind more layers.
