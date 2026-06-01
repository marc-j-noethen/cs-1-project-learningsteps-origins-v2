# Repository Workbook

## Purpose of This Workbook

This workbook explains the role of every tracked file in the repository so you can:

- understand the current project without guessing
- explain the repo confidently in an interview or review
- reuse the same structure for later portfolio projects
- know what to test, what to edit, and what to leave alone

## How to Read This Repo

The repository has four layers:

1. **Portfolio wrapper** at the root level  
   This is what GitHub visitors see first: README, security policy, automation, architecture docs, reports, and evidence.

2. **Application bundle** under `app/`  
   This is the runnable FastAPI/PostgreSQL workload and its local development tooling.

3. **Operational documentation** under `docs/`, `evidence/`, and `reports/`  
   These files explain architecture, validation, and publishing instead of only shipping source code.

4. **Safety and quality automation** under `.github/` and `scripts/`  
   These files help keep the repo public-safe and easier to maintain.

## File-by-File Workbook

### `.env.example`

Role: Root-level environment template for the whole portfolio project.

Why it matters:
- It shows which environment variables are required without exposing secrets.
- It documents both local and Azure-style usage.
- It acts as the public-facing contract for configuration.

When to edit it:
- When the runtime requires a new environment variable.
- When you change security defaults such as rate limits or docs visibility.
- When the deployment pattern changes between local and Azure.

What to learn from it:
- Good repos never commit real secrets.
- A useful example file is part of developer experience, not an afterthought.

### `.gitattributes`

Role: Cross-platform line-ending control for important file types.

Why it matters:
- It prevents Windows and Linux line-ending drift.
- It protects shell scripts from breaking with CRLF line endings.
- It keeps Markdown, YAML, Python, and PowerShell files predictable.

When to edit it:
- When you add new important text-based file types.
- When a cross-platform tooling issue shows up.

What to learn from it:
- Small platform details can break big workflows.
- DevSecOps includes boring but important reproducibility controls.

### `.gitignore`

Role: Main ignore policy for the public repository.

Why it matters:
- It blocks secrets, local artifacts, editor folders, and reference material.
- It separates the publishable repo from your private working environment.
- It protects you from accidentally pushing `.env`, keys, temp data, or internal prep files.

When to edit it:
- When new local artifacts appear.
- When new tools create caches, reports, or temp folders.
- When you add new evidence or generated directories.

What to learn from it:
- `.gitignore` is a security control, not just a convenience file.

### `README.md`

Role: Primary public landing page of the repository.

Why it matters:
- It tells the story of the project in recruiter-friendly language.
- It explains the architecture, scope, validation, and repo structure.
- It clarifies the naming mismatch between the LearningSteps course wrapper and the SWB app bundle.

When to edit it:
- When the project scope changes.
- When you add stronger evidence, security controls, or deployment steps.
- Before every serious public release review.

What to learn from it:
- The README should explain what the project is, why it matters, and how it was validated.

### `SECURITY.md`

Role: Root-level security policy for the portfolio repository.

Why it matters:
- It signals professional security ownership to reviewers.
- It explains supported use, vulnerability reporting, and baseline controls.
- It documents residual risks and next hardening steps.

When to edit it:
- When you add or remove important controls.
- When the deployment model changes.
- When your disclosure workflow changes.

What to learn from it:
- Public security documentation increases credibility when it is honest and scoped.

### `.github/dependabot.yml`

Role: Dependency update automation for GitHub.

Why it matters:
- It checks Python dependencies in `app/api`.
- It checks GitHub Actions versions at the repo root.
- It helps keep the repo maintained after publication.

When to edit it:
- When dependency paths move.
- When you change update cadence or pull request limits.

What to learn from it:
- Maintenance is part of professionalism; stale dependencies are a real security risk.

### `.github/workflows/ci.yml`

Role: Continuous integration workflow.

Why it matters:
- It installs dependencies in GitHub Actions.
- It compiles the Python sources and runs unit tests.
- It gives reviewers a visible quality gate on every push and pull request.

When to edit it:
- When test commands change.
- When the project layout changes.
- When you add linting or additional checks.

What to learn from it:
- A repo looks much stronger when testing is repeatable and automated.

### `.github/workflows/codeql.yml`

Role: Static code analysis workflow using CodeQL.

Why it matters:
- It adds GitHub-native code scanning for Python.
- It improves the security story of the public repository.
- It helps demonstrate DevSecOps awareness beyond manual review.

When to edit it:
- When language targets change.
- When scan schedules or permissions need adjustment.

What to learn from it:
- Secure repos benefit from both runtime tests and static analysis.

### `app/.devcontainer/devcontainer.json`

Role: VS Code Dev Container definition.

Why it matters:
- It standardizes the local development environment.
- It adds Azure CLI support inside the dev container.
- It makes the project easier to reproduce on a fresh machine.

When to edit it:
- When you add new development tools.
- When the base image or container behavior changes.

What to learn from it:
- A reliable local environment reduces “works on my machine” problems.

### `app/.devcontainer/docker-compose.yml`

Role: Local multi-container setup for development.

Why it matters:
- It defines the PostgreSQL service used by the app locally.
- It mounts the bootstrap SQL file and environment file.
- It includes a corrected healthcheck for `pg_isready`.

When to edit it:
- When database version, ports, or startup logic change.
- When the app needs more local services.

What to learn from it:
- Local dependency orchestration is part of testability.

### `app/.env.example`

Role: Application-local environment template.

Why it matters:
- It is the most direct setup file for running the app locally.
- It documents app-specific defaults and security-sensitive fields.
- It tells a future maintainer exactly what the runtime expects.

When to edit it:
- When app configuration changes.
- When defaults become unsafe or misleading.

What to learn from it:
- Root config and app config can have different audiences; both can be useful.

### `app/.gitignore`

Role: Legacy app-level Python ignore policy.

Why it matters:
- It still blocks common Python artifacts inside the app folder.
- It catches local troubleshooting files specific to the app workspace.

When to edit it:
- When app-local artifacts change.
- When you want to simplify or consolidate ignore rules later.

What to learn from it:
- Sometimes a portfolio repo contains both root-level governance and inherited app-level hygiene.

### `app/README.md`

Role: Application-specific README for the SWB workload.

Why it matters:
- It explains the app independent of the Azure wrapper.
- It documents login, password hashing, local setup, and app behavior.
- It helps separate “portfolio repo” from “runnable app.”

When to edit it:
- When the app changes functionally.
- When setup, security defaults, or local startup steps change.

What to learn from it:
- One repo can have a public project README and a deeper subsystem README.

### `app/SECURITY.md`

Role: Application-specific security policy.

Why it matters:
- It focuses on runtime concerns such as host restrictions and hashed passwords.
- It complements the broader repo-level security file.

When to edit it:
- When app hardening features change.
- When deployment security expectations change.

What to learn from it:
- Security documentation can be layered: repo-level and service-level.

### `app/database_setup.sql`

Role: Database bootstrap schema for the workshops table.

Why it matters:
- It defines the initial persistence structure.
- It creates indexes for common query paths.
- It allows local PostgreSQL initialization without manual SQL steps.

When to edit it:
- When the data model changes.
- When new indexes or constraints are needed.

What to learn from it:
- Database bootstrap files make setup faster and more reproducible.

### `app/start.sh`

Role: Local startup script for the application.

Why it matters:
- It creates a virtual environment if needed.
- It installs dependencies and starts Uvicorn.
- It gives a single, easy command for local launch.

When to edit it:
- When startup commands, dependency install steps, or ports change.
- When you want to add stronger local checks.

What to learn from it:
- A good start script removes friction for testers and reviewers.

### `app/test_api.py`

Role: Manual smoke test for the running API.

Why it matters:
- It verifies login, session handling, CSRF, create, and delete flow.
- It is the closest thing in the repo to an end-to-end API interaction test.

When to edit it:
- When routes or payload structure change.
- When you add additional smoke-test coverage.

What to learn from it:
- Not every useful test needs a large framework; a simple smoke script can still be valuable.

### `app/api/__init__.py`

Role: Lightweight package marker for the API package.

Why it matters:
- It keeps `import api` side-effect free.
- It prevents broken imports from stale legacy modules.

When to edit it:
- Only if you intentionally want package-level exports.

What to learn from it:
- Empty or minimal package initializers are often safer than clever ones.

### `app/api/config.py`

Role: Central configuration loader and validator.

Why it matters:
- It loads environment variables.
- It validates required secrets and safety settings before startup.
- It converts raw strings into a structured `Settings` object.

When to edit it:
- When you add config keys.
- When you tighten validation rules.

What to learn from it:
- Centralized configuration is cleaner and safer than scattered `os.getenv()` calls.

### `app/api/dependencies.py`

Role: Shared FastAPI dependency helpers and request guards.

Why it matters:
- It exposes app settings and service access.
- It enforces authentication, CSRF, and rate-limit behavior.
- It extracts a client identity for rate limiting.

When to edit it:
- When auth logic changes.
- When new shared dependencies are introduced.

What to learn from it:
- Dependency injection is a clean way to enforce shared security rules.

### `app/api/main.py`

Role: Main FastAPI application entrypoint.

Why it matters:
- It creates the FastAPI app.
- It builds the PostgreSQL pool on startup.
- It registers middleware, routers, static files, and the `/health` endpoint.

When to edit it:
- When app startup, middleware, routers, or global state change.

What to learn from it:
- `main.py` should be orchestration glue, not business logic.

### `app/api/middleware.py`

Role: Custom middleware for body-size limits and security headers.

Why it matters:
- It adds HTTP hardening in one place.
- It blocks oversized requests early.
- It injects CSP, referrer policy, frame protection, and related headers.

When to edit it:
- When headers need tightening.
- When request-size expectations change.

What to learn from it:
- Middleware is a strong place for cross-cutting security rules.

### `app/api/models/__init__.py`

Role: Package marker for API models.

Why it matters:
- It keeps the models package explicit and importable.

When to edit it:
- Only if you intentionally want model re-exports.

What to learn from it:
- Sometimes a file exists mainly to make module boundaries clean.

### `app/api/models/workshop.py`

Role: Pydantic schema definitions and validation rules for workshops.

Why it matters:
- It validates incoming payloads.
- It normalizes text and list fields.
- It defines the contract between frontend, API, and database service layer.

When to edit it:
- When workshop fields change.
- When validation rules need strengthening or relaxing.

What to learn from it:
- Strong data validation prevents many downstream bugs and bad input states.

### `app/api/rate_limit.py`

Role: In-memory rate limiter implementation.

Why it matters:
- It gives simple protection against rapid login or write abuse.
- It is easy to understand and works without external infrastructure.

When to edit it:
- When you move to distributed rate limiting.
- When rate-limit behavior must become more advanced.

What to learn from it:
- Even simple in-memory controls can add meaningful safety in small apps.

### `app/api/repositories/__init__.py`

Role: Package marker for persistence implementations.

Why it matters:
- It makes the repository layer explicit and structured.

When to edit it:
- Only if you want top-level repository exports later.

What to learn from it:
- Clear package boundaries help keep architecture understandable.

### `app/api/repositories/interface_repository.py`

Role: Abstract database interface.

Why it matters:
- It defines the contract the service layer expects from persistence.
- It makes the design cleaner and easier to swap or mock later.

When to edit it:
- When repository capabilities change.
- When new persistence operations are introduced.

What to learn from it:
- Interfaces help separate business logic from storage details.

### `app/api/repositories/postgres_repository.py`

Role: PostgreSQL-backed repository implementation.

Why it matters:
- It contains SQL for create, read, update, delete, count, search, and slug checks.
- It maps asyncpg rows into Python dictionaries used by the service layer.

When to edit it:
- When schema or query behavior changes.
- When performance or filtering requirements change.

What to learn from it:
- Keep SQL-focused persistence logic separate from API and business rules.

### `app/api/requirements.txt`

Role: Runtime dependency list for the app.

Why it matters:
- It defines what CI and local startup install.
- It now explicitly includes `itsdangerous`, which the app needs because `main.py` uses Starlette's `SessionMiddleware`.
- FastAPI pulls in Pydantic transitively, which is why model validation works once dependencies are installed.

When to edit it:
- When you add, remove, or pin dependencies.

What to learn from it:
- Small requirement files are easier to reason about, but transitive dependencies should still be understood.

### `app/tests/test_app_import.py`

Role: Import smoke test for the FastAPI application entrypoint.

Why it matters:
- It verifies that `main.py` can build the app object with realistic environment variables.
- It catches missing runtime dependencies during CI before you discover them manually.
- It protects against configuration regressions at the import/startup boundary.

When to edit it:
- When startup configuration changes.
- When the entrypoint moves or new required environment variables are added.

What to learn from it:
- A tiny startup smoke test can prevent surprisingly expensive debugging later.

### `app/api/routers/__init__.py`

Role: Package marker for API routers.

Why it matters:
- It makes the router package explicit.

When to edit it:
- Only if you intentionally want router re-exports.

What to learn from it:
- Consistent package structure keeps repos easier to navigate.

### `app/api/routers/auth_router.py`

Role: Authentication routes.

Why it matters:
- It handles session introspection, login, and logout.
- It compares usernames and passwords safely.
- It sets the CSRF token after successful authentication.

When to edit it:
- When auth flow or session design changes.

What to learn from it:
- Even small apps benefit from clear route separation by responsibility.

### `app/api/routers/workshop_router.py`

Role: CRUD routes for workshop data.

Why it matters:
- It defines the public API surface for the dashboard.
- It enforces auth, CSRF, and write-rate protection through dependencies.

When to edit it:
- When API endpoints or payload behavior change.

What to learn from it:
- Routers should stay thin and delegate business logic to services.

### `app/api/security.py`

Role: Security utility functions.

Why it matters:
- It generates CSRF tokens.
- It hashes and verifies passwords using PBKDF2.
- It creates clean slugs from workshop titles.

When to edit it:
- When password strategy or slug rules change.

What to learn from it:
- Security helpers should be centralized, testable, and explicit.

### `app/api/services/__init__.py`

Role: Package marker for business logic services.

Why it matters:
- It keeps the service layer organized and importable.

When to edit it:
- Only if you want package-level exports later.

What to learn from it:
- Clear architecture layers make mentorship and maintenance easier.

### `app/api/services/workshop_service.py`

Role: Core business logic for workshops.

Why it matters:
- It seeds demo workshops.
- It builds dashboard snapshots and statistics.
- It creates slugs, assigns IDs, and coordinates persistence.

When to edit it:
- When business rules or dashboard behavior change.
- When seeding or slug behavior changes.

What to learn from it:
- Services are where application behavior should live, not routers or repositories.

### `app/api/static/app.js`

Role: Frontend application logic.

Why it matters:
- It drives login, dashboard loading, filters, modal behavior, CRUD actions, and clipboard export.
- It binds the UI to the backend API.

When to edit it:
- When UI behavior or API payloads change.

What to learn from it:
- Even a plain JavaScript frontend can be structured and state-driven.

### `app/api/static/styles.css`

Role: Frontend styling.

Why it matters:
- It defines the visual system, layout, light/dark theming, and component appearance.
- It makes the app feel intentional rather than purely functional.

When to edit it:
- When branding, layout, or component styling changes.

What to learn from it:
- A portfolio app should communicate craftsmanship visually as well as technically.

### `app/api/templates/index.html`

Role: Single HTML entry template for the UI.

Why it matters:
- It provides the DOM structure that the JavaScript controls.
- It includes the login gate, dashboard, metadata panels, modal form, and security panel.

When to edit it:
- When layout, accessible structure, or top-level UI sections change.

What to learn from it:
- A clear HTML skeleton makes frontend behavior easier to reason about.

### `app/api/tools/generate_password_hash.py`

Role: Utility script to generate a hashed admin password.

Why it matters:
- It helps you avoid storing plain passwords in hosted environments.
- It turns the security helper into a practical operator tool.

When to edit it:
- When hashing behavior or CLI usage changes.

What to learn from it:
- Small operator scripts increase usability without bloating the main app.

### `app/tests/test_security.py`

Role: Unit tests for password hashing and slug generation.

Why it matters:
- It checks that password roundtrips work.
- It confirms slug creation behaves predictably.

When to edit it:
- When security helper behavior changes.

What to learn from it:
- Security-sensitive helpers deserve direct tests.

### `app/tests/test_workshop_model.py`

Role: Unit tests for workshop payload validation.

Why it matters:
- It confirms valid payloads parse.
- It checks that bad objective lists are rejected.

When to edit it:
- When validation rules or fields change.

What to learn from it:
- Validation logic should be proven, not assumed.

### `docs/architecture/target-architecture.md`

Role: Main architecture explanation for the Azure design.

Why it matters:
- It explains the trust boundaries, tiers, and resource roles.
- It gives a narrative version of the diagram.

When to edit it:
- When infrastructure design changes.

What to learn from it:
- Architecture docs should explain both shape and reasoning.

### `docs/architecture/port-matrix.md`

Role: Connectivity matrix for the system.

Why it matters:
- It documents allowed flows clearly.
- It translates “secure architecture” into concrete network rules.

When to edit it:
- When ports, flows, or exposure levels change.

What to learn from it:
- Port matrices are one of the clearest forms of security documentation.

### `docs/operations/deployment-runbook.md`

Role: Step-by-step Azure deployment guide.

Why it matters:
- It turns the architecture into repeatable operations.
- It captures sequencing, validation, and post-deploy checks.

When to edit it:
- When deployment steps or service names change.

What to learn from it:
- A strong runbook bridges architecture and real operations.

### `docs/operations/github-publishing.md`

Role: GitHub publication guide.

Why it matters:
- It defines metadata, pre-push checks, and post-push review steps.
- It makes the publishing process repeatable across future projects.

When to edit it:
- When your repo naming scheme, topics, or release workflow changes.

What to learn from it:
- Publishing is a process worth documenting just like deployment.

### `docs/operations/local-validation.md`

Role: Guide for local runtime validation.

Why it matters:
- It documents what “working locally” actually means.
- It captures the specific fixes that stabilized local execution.

When to edit it:
- When startup steps or validation methods change.

What to learn from it:
- Testing instructions are more useful when they include expected outcomes.

### `evidence/README.md`

Role: Index of the evidence folder.

Why it matters:
- It explains what the evidence package contains and what should be added later.
- It sets a public-safe evidence standard.

When to edit it:
- When you add new screenshots or proof artifacts.

What to learn from it:
- Evidence is stronger when it is curated, not dumped.

### `evidence/local-ui-overview.png`

Role: Screenshot asset showing the local UI.

Why it matters:
- It proves the app rendered visually.
- It gives GitHub visitors immediate context.

When to edit it:
- When the UI changes enough that the screenshot becomes misleading.

What to learn from it:
- Visual proof is part of a strong portfolio.

### `evidence/verification-summary.md`

Role: Short proof summary for validation outcomes.

Why it matters:
- It captures the main successful checks in one quick-read file.
- It gives reviewers a compact verification overview.

When to edit it:
- When you add new proof or refine what was validated.

What to learn from it:
- A short summary helps people orient before reading full reports.

### `reports/SUBMISSION-CHECKLIST.md`

Role: Release-readiness checklist for the repository.

Why it matters:
- It tracks what has already been prepared for publication.
- It highlights remaining final review actions before a public push.

When to edit it:
- When a release step is completed or added.

What to learn from it:
- Checklists reduce last-minute mistakes.

### `reports/final-project-report.md`

Role: Formal project report.

Why it matters:
- It gives a compact executive narrative of goals, controls, validation, and lessons learned.
- It is useful for portfolio review, interviews, or a submission handoff.

When to edit it:
- When new validation results or lessons learned are available.

What to learn from it:
- A strong final report tells the story of decisions, not only outcomes.

### `scripts/repo-readiness-check.ps1`

Role: Local preflight script for publication readiness.

Why it matters:
- It checks required files, obvious secret leakage, unfinished markers, and Python compileability.
- It is your fast “am I safe to push?” command.

When to edit it:
- When the required file set changes.
- When you want stronger checks.

What to learn from it:
- Good repos automate the boring review steps before humans push.

## Workbook Summary

If you remember only one mental model, use this one:

- root level = portfolio presentation and governance
- `app/` = runnable workload
- `docs/` = architecture and operations
- `evidence/` = proof
- `reports/` = polished narrative
- `.github/` and `scripts/` = automation and safety rails

That structure is reusable for your next projects with only small changes in naming and tech stack.
