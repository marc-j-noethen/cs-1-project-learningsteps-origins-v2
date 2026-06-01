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
- `app/api/requirements.txt` needed `itsdangerous` because the app uses Starlette's `SessionMiddleware`.

## Repeatable Validation Flow

### Option A: Windows / PowerShell

1. Copy [`app/.env.example`](../../app/.env.example) to `app/.env`.
2. Update `DATABASE_URL` in `app/.env` to point to the host-mapped PostgreSQL port:

```env
DATABASE_URL=postgresql://postgres:change-me-locally@localhost:5432/second_workshop_brain
```

3. Fill the required secrets in `app/.env`:

```env
SWB_ADMIN_PASSWORD=<strong-local-password>
SESSION_SECRET=<at-least-32-random-characters>
```

4. Start PostgreSQL from the repository root:

```powershell
docker compose -f app/.devcontainer/docker-compose.yml up -d postgres
```

5. Start the API from `app/api` with local dependencies available on `PYTHONPATH`:

```powershell
$env:PYTHONPATH = "..\..\.codex-test-deps;."
& "<python-path>" -m uvicorn main:app --host 127.0.0.1 --port 8000
```

6. In a second terminal, verify the service is responding:

```powershell
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/docs
```

7. Run the CRUD smoke test from `app/`:

```powershell
$env:SWB_PASSWORD = "<strong-local-password>"
& "<python-path>" .\test_api.py
```

8. When you are done, stop the local database:

```powershell
docker compose -f app/.devcontainer/docker-compose.yml down
```

### Option B: Linux / Dev Container

1. Copy [`app/.env.example`](../../app/.env.example) to `app/.env`.
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
