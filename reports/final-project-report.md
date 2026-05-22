# Final Project Report

## Executive Summary

`LearningSteps Origins` documents a completed Azure 2-tier deployment pattern for a FastAPI/PostgreSQL workload with a strong DevSecOps emphasis. The final design exposes only the application tier to the internet, keeps the PostgreSQL tier private, and captures the implementation in a GitHub-ready evidence package.

## Objectives

- deploy a working FastAPI workload to Azure
- isolate the database tier from the public internet
- enforce least-privilege connectivity between tiers
- prove the result with validation evidence and reproducible documentation

## Delivered Architecture

- Azure resource group: `rg-learningsteps-dev`
- VNet: `vnet-learningsteps` (`10.10.0.0/16`)
- Public subnet: `snet-public-api` (`10.10.1.0/24`)
- Private subnet: `snet-private-db` (`10.10.2.0/24`)
- API VM: `vm-api-learningsteps`
- DB VM: `vm-db-learningsteps`

The API tier is internet-reachable. The database tier has no public IP and is reachable only from the API subnet over PostgreSQL.

## Security Controls Implemented

1. Public/private subnet separation
2. Database isolation with no public exposure
3. DB ingress restricted to the API subnet on port `5432`
4. SSH restricted to an approved admin source
5. Effective-path NSG validation and cleanup
6. Application-level protections in the sanitized app bundle:
   session controls, trusted hosts, CSRF validation, security headers, and rate limiting

## Validation Results

- Local environment worked after targeted fixes to the health check and script line endings.
- CRUD functionality was verified locally.
- External API reachability in Azure was restored and confirmed after correcting the effective NSG path.
- Internal PostgreSQL connectivity from the API tier was verified.
- Administrative access restrictions were confirmed with allow and deny tests.

## Key Lessons

### Effective security paths matter

The main operational lesson was that the intended subnet NSG did not fully represent the real enforcement path. The actual ingress behavior was controlled through a NIC-bound NSG. This reinforced the need to validate effective policy, not just planned configuration.

### Repo hygiene is part of DevSecOps

Preparing the project for publication required separating local-only material from the public repo surface: nested Git history, virtual environments, environment files, and internal course reference folders all had to remain outside the release boundary.

### Honest documentation improves credibility

The public repo now states clearly that the course wrapper is `LearningSteps Origins` while the sanitized application artifact is a hardened FastAPI/PostgreSQL workload variant named `SWB | Second-Workshop-Brain`.

## Recommended Next Steps

1. Add HTTPS termination and certificate management
2. Move secrets to Azure Key Vault
3. Replace direct SSH with Bastion or Just-in-Time access
4. Add centralized monitoring, logging, and backup/restore drills

## Release Position

The repository is ready for GitHub publication after local git initialization, remote creation, and a final human review of screenshots and metadata.
