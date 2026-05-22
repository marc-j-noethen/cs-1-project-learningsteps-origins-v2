import asyncpg
from typing import Any, Dict, List

from repositories.interface_repository import DatabaseInterface

class PostgresDB(DatabaseInterface):
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    @staticmethod
    def _serialize_workshop(row: asyncpg.Record) -> Dict[str, Any]:
        return {
            "id": row["id"],
            "slug": row["slug"],
            "title": row["title"],
            "category": row["category"],
            "status": row["status"],
            "difficulty": row["difficulty"],
            "duration_hours": row["duration_hours"],
            "summary": row["summary"],
            "description": row["description"],
            "objectives": list(row["objectives"] or []),
            "stack": list(row["stack"] or []),
            "published": row["published"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }

    async def ensure_schema(self) -> None:
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS workshops (
                    id VARCHAR(64) PRIMARY KEY,
                    slug VARCHAR(160) UNIQUE NOT NULL,
                    title VARCHAR(120) NOT NULL,
                    category VARCHAR(40) NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    difficulty VARCHAR(24) NOT NULL,
                    duration_hours INTEGER NOT NULL CHECK (duration_hours >= 1 AND duration_hours <= 80),
                    summary VARCHAR(280) NOT NULL,
                    description TEXT NOT NULL,
                    objectives TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
                    stack TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
                    published BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMPTZ NOT NULL,
                    updated_at TIMESTAMPTZ NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_workshops_category ON workshops(category);
                CREATE INDEX IF NOT EXISTS idx_workshops_status ON workshops(status);
                CREATE INDEX IF NOT EXISTS idx_workshops_published ON workshops(published);
                """
            )

    async def count_workshops(self) -> int:
        async with self.pool.acquire() as conn:
            return await conn.fetchval("SELECT COUNT(*)::INT FROM workshops")

    async def list_workshops(
        self,
        search_query: str | None = None,
        category: str | None = None,
    ) -> List[Dict[str, Any]]:
        conditions: list[str] = []
        params: list[Any] = []

        if search_query:
            params.append(f"%{search_query}%")
            position = len(params)
            conditions.append(
                f"(title ILIKE ${position} OR summary ILIKE ${position} OR description ILIKE ${position})"
            )

        if category:
            params.append(category)
            conditions.append(f"category = ${len(params)}")

        where_clause = f" WHERE {' AND '.join(conditions)}" if conditions else ""
        query = (
            "SELECT id, slug, title, category, status, difficulty, duration_hours, "
            "summary, description, objectives, stack, published, created_at, updated_at "
            "FROM workshops"
            f"{where_clause} "
            "ORDER BY category ASC, title ASC"
        )

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *params)
            return [self._serialize_workshop(row) for row in rows]

    async def get_workshop(self, workshop_id: str) -> Dict[str, Any] | None:
        query = (
            "SELECT id, slug, title, category, status, difficulty, duration_hours, "
            "summary, description, objectives, stack, published, created_at, updated_at "
            "FROM workshops WHERE id = $1"
        )
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, workshop_id)
            return self._serialize_workshop(row) if row else None

    async def create_workshop(self, workshop_data: Dict[str, Any]) -> Dict[str, Any]:
        query = """
            INSERT INTO workshops (
                id, slug, title, category, status, difficulty, duration_hours,
                summary, description, objectives, stack, published, created_at, updated_at
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
            RETURNING id, slug, title, category, status, difficulty, duration_hours,
                      summary, description, objectives, stack, published, created_at, updated_at
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                workshop_data["id"],
                workshop_data["slug"],
                workshop_data["title"],
                workshop_data["category"],
                workshop_data["status"],
                workshop_data["difficulty"],
                workshop_data["duration_hours"],
                workshop_data["summary"],
                workshop_data["description"],
                workshop_data["objectives"],
                workshop_data["stack"],
                workshop_data["published"],
                workshop_data["created_at"],
                workshop_data["updated_at"],
            )
            return self._serialize_workshop(row)

    async def update_workshop(
        self,
        workshop_id: str,
        workshop_data: Dict[str, Any],
    ) -> Dict[str, Any] | None:
        query = """
            UPDATE workshops
            SET slug = $2,
                title = $3,
                category = $4,
                status = $5,
                difficulty = $6,
                duration_hours = $7,
                summary = $8,
                description = $9,
                objectives = $10,
                stack = $11,
                published = $12,
                updated_at = $13
            WHERE id = $1
            RETURNING id, slug, title, category, status, difficulty, duration_hours,
                      summary, description, objectives, stack, published, created_at, updated_at
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                workshop_id,
                workshop_data["slug"],
                workshop_data["title"],
                workshop_data["category"],
                workshop_data["status"],
                workshop_data["difficulty"],
                workshop_data["duration_hours"],
                workshop_data["summary"],
                workshop_data["description"],
                workshop_data["objectives"],
                workshop_data["stack"],
                workshop_data["published"],
                workshop_data["updated_at"],
            )
            return self._serialize_workshop(row) if row else None

    async def delete_workshop(self, workshop_id: str) -> None:
        async with self.pool.acquire() as conn:
            await conn.execute("DELETE FROM workshops WHERE id = $1", workshop_id)

    async def slug_exists(self, slug: str, exclude_id: str | None = None) -> bool:
        params: list[Any] = [slug]
        query = "SELECT 1 FROM workshops WHERE slug = $1"
        if exclude_id:
            params.append(exclude_id)
            query += " AND id <> $2"
        query += " LIMIT 1"

        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *params)
            return row is not None
