# GitHub Publishing

## Recommended Repository Metadata

- **Suggested name:** `learningsteps-origins-azure`
- **Suggested description:** `Security-focused Azure 2-tier deployment for a FastAPI/PostgreSQL workload with evidence, runbooks, and GitHub-ready automation.`
- **Suggested topics:** `devsecops`, `azure`, `fastapi`, `postgresql`, `cloud-security`, `nsg`, `github-actions`, `codeql`, `dependabot`, `portfolio`
- **Initial visibility:** `private`
- **Default branch:** `main`

## Before You Push

Run the local preflight:

```powershell
pwsh -File .\scripts\repo-readiness-check.ps1
```

Check:

- README and docs are public-safe
- no `.env` or secrets are present
- `Project-Dev/` and `Project-Info/` stay local-only
- the repository still compiles cleanly

## Local Git Bootstrap

```bash
git init
git branch -M main
git status
git add .
git commit -m "chore: prepare portfolio repo for GitHub"
```

## Create the GitHub Repository

1. Create a new repository on GitHub with the metadata above.
2. Leave visibility on `private` until the final review is complete.
3. Enable Issues, Pull Requests, and Code scanning.

## Connect and Push

```bash
git remote add origin https://github.com/<username>/learningsteps-origins-azure.git
git push -u origin main
```

## Immediate Post-Push Checks

1. Confirm that GitHub rendered the Mermaid diagram in the README.
2. Confirm that `app/.env` and local-only reference folders were not uploaded.
3. Open the Actions tab and verify CI and CodeQL start successfully.
4. Confirm Dependabot is enabled for both Python dependencies and GitHub Actions.

## Recommended Follow-Up Commits

Use small, intention-revealing commits:

- `docs: add final evidence and report cross-links`
- `chore: enable portfolio repo automation`
- `docs: polish architecture and lessons learned`
- `chore: prepare public release`

## Public Release Checklist

Switch the repository from private to public only after you have:

- removed anything you would not want a recruiter or stranger to see
- double-checked screenshots and command output for accidental leakage
- reviewed the repo description, topics, and README once more
