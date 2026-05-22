from datetime import datetime, timezone
from uuid import uuid4

from models.workshop import WorkshopPayload
from repositories.postgres_repository import PostgresDB
from security import slugify_title


SEED_WORKSHOPS = [
    {
        "title": "Fullstack Delivery Sprint",
        "category": "Fullstack",
        "status": "published",
        "difficulty": "intermediate",
        "duration_hours": 16,
        "summary": "Build a production-like fullstack feature from schema design through API delivery and hardened deployment notes.",
        "description": (
            "This workshop trains the end-to-end thinking behind a modern product slice.\n"
            "Participants move from domain modeling to API design, frontend orchestration, "
            "observability, and secure release prep."
        ),
        "objectives": [
            "Model a clean domain and persistence layer.",
            "Ship a frontend and backend feature as one scoped delivery.",
            "Add monitoring, validation, and deployment safeguards.",
        ],
        "stack": ["FastAPI", "PostgreSQL", "HTML/CSS", "Docker"],
        "published": True,
    },
    {
        "title": "SaaS Foundation Blueprint",
        "category": "SaaS",
        "status": "review",
        "difficulty": "advanced",
        "duration_hours": 20,
        "summary": "Design a SaaS foundation covering tenancy, onboarding, billing placeholders, and operational guardrails.",
        "description": (
            "Use this workshop when you want to teach platform thinking instead of isolated coding tasks.\n"
            "The flow covers SaaS fundamentals, service boundaries, and trusted release discipline."
        ),
        "objectives": [
            "Map the core SaaS lifecycle from onboarding to retention.",
            "Explain tenant-aware data and operational isolation.",
            "Document security and governance checkpoints before launch.",
        ],
        "stack": ["Architecture", "Auth", "Billing", "DevSecOps"],
        "published": False,
    },
    {
        "title": "Git Confidence Lab",
        "category": "Git",
        "status": "published",
        "difficulty": "fundamentals",
        "duration_hours": 6,
        "summary": "Teach safe branch workflows, commit hygiene, merge conflict handling, and rollback patterns with confidence.",
        "description": (
            "This lab gives learners repetition on the Git habits that reduce delivery risk.\n"
            "It works well as a foundation before any collaborative engineering workshop."
        ),
        "objectives": [
            "Create clean commits with useful messages.",
            "Practice branching, rebasing, and conflict resolution.",
            "Understand safe rollback and recovery workflows.",
        ],
        "stack": ["Git", "CLI", "Pairing"],
        "published": True,
    },
    {
        "title": "GitHub Collaboration Ops",
        "category": "GitHub",
        "status": "draft",
        "difficulty": "intermediate",
        "duration_hours": 8,
        "summary": "Focus on pull requests, review quality, workflow automation, and repository governance for small teams.",
        "description": (
            "The workshop turns GitHub from a file host into a lightweight engineering system.\n"
            "It is tailored to teaching collaboration rituals and automation hygiene."
        ),
        "objectives": [
            "Run a healthy pull request workflow.",
            "Set repository protections and ownership expectations.",
            "Automate quality checks for repeatable delivery.",
        ],
        "stack": ["GitHub Actions", "PR Reviews", "Branch Protection"],
        "published": False,
    },
    {
        "title": "Docker Workshop Core",
        "category": "Docker",
        "status": "published",
        "difficulty": "intermediate",
        "duration_hours": 10,
        "summary": "Guide learners from local images to multi-container composition with clean operational explanations.",
        "description": (
            "This track mirrors the clarity of the Docker workshop reference layout.\n"
            "Use it to structure hands-on sections, container lifecycle guidance, and compose-based delivery."
        ),
        "objectives": [
            "Explain image, container, and registry concepts clearly.",
            "Containerize an app and add persistent data handling.",
            "Use Compose to define and run a multi-service stack.",
        ],
        "stack": ["Docker", "Compose", "Volumes", "Networking"],
        "published": True,
    },
    {
        "title": "Kubernetes Platform Walkthrough",
        "category": "Kubernetes",
        "status": "review",
        "difficulty": "advanced",
        "duration_hours": 18,
        "summary": "Translate container knowledge into cluster operations, workload design, and secure platform delivery habits.",
        "description": (
            "This workshop introduces the concepts behind Kubernetes without turning into YAML spam.\n"
            "It focuses on workloads, networking, secrets handling, and production readiness."
        ),
        "objectives": [
            "Map Docker concepts to Kubernetes building blocks.",
            "Reason about workloads, services, and ingress boundaries.",
            "Apply safer secret and deployment practices.",
        ],
        "stack": ["Kubernetes", "Helm", "Ingress", "Secrets"],
        "published": False,
    },
]


class WorkshopService:
    def __init__(self, repository: PostgresDB):
        self.repository = repository

    async def seed_default_workshops(self) -> None:
        if await self.repository.count_workshops() > 0:
            return
        for payload in SEED_WORKSHOPS:
            await self.create_workshop(WorkshopPayload(**payload))

    async def get_dashboard_snapshot(
        self,
        search_query: str | None = None,
        category: str | None = None,
    ) -> dict:
        workshops = await self.repository.list_workshops(
            search_query=search_query,
            category=category,
        )
        categories = sorted({workshop["category"] for workshop in workshops})
        stats = {
            "total": len(workshops),
            "published": sum(1 for workshop in workshops if workshop["published"]),
            "draft": sum(1 for workshop in workshops if workshop["status"] == "draft"),
            "review": sum(1 for workshop in workshops if workshop["status"] == "review"),
            "categories": len(categories),
        }
        selected_id = workshops[0]["id"] if workshops else None
        return {
            "workshops": workshops,
            "stats": stats,
            "categories": categories,
            "selectedId": selected_id,
        }

    async def get_workshop(self, workshop_id: str) -> dict | None:
        return await self.repository.get_workshop(workshop_id)

    async def create_workshop(self, payload: WorkshopPayload) -> dict:
        now = datetime.now(timezone.utc)
        slug = await self._build_unique_slug(payload.title)
        record = {
            "id": str(uuid4()),
            "slug": slug,
            "created_at": now,
            "updated_at": now,
            **payload.model_dump(),
        }
        return await self.repository.create_workshop(record)

    async def update_workshop(self, workshop_id: str, payload: WorkshopPayload) -> dict | None:
        existing = await self.repository.get_workshop(workshop_id)
        if not existing:
            return None

        updated_record = {
            "id": workshop_id,
            "slug": await self._build_unique_slug(payload.title, exclude_id=workshop_id),
            "created_at": existing["created_at"],
            "updated_at": datetime.now(timezone.utc),
            **payload.model_dump(),
        }
        return await self.repository.update_workshop(workshop_id, updated_record)

    async def delete_workshop(self, workshop_id: str) -> None:
        await self.repository.delete_workshop(workshop_id)

    async def _build_unique_slug(self, title: str, exclude_id: str | None = None) -> str:
        base_slug = slugify_title(title)
        candidate = base_slug
        suffix = 2

        while await self.repository.slug_exists(candidate, exclude_id=exclude_id):
            candidate = f"{base_slug}-{suffix}"
            suffix += 1

        return candidate
