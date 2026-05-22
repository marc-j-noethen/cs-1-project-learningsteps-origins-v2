from abc import ABC, abstractmethod
from typing import Any, Dict, List


class DatabaseInterface(ABC):
    """Abstract interface for workshop persistence."""

    @abstractmethod
    async def ensure_schema(self) -> None:
        """Ensure the database schema exists."""

    @abstractmethod
    async def count_workshops(self) -> int:
        """Return the total number of persisted workshops."""

    @abstractmethod
    async def list_workshops(
        self,
        search_query: str | None = None,
        category: str | None = None,
    ) -> List[Dict[str, Any]]:
        """Return workshops filtered by the supplied criteria."""

    @abstractmethod
    async def get_workshop(self, workshop_id: str) -> Dict[str, Any] | None:
        """Return a single workshop by ID."""

    @abstractmethod
    async def create_workshop(self, workshop_data: Dict[str, Any]) -> Dict[str, Any]:
        """Persist and return a newly created workshop."""

    @abstractmethod
    async def update_workshop(
        self,
        workshop_id: str,
        workshop_data: Dict[str, Any],
    ) -> Dict[str, Any] | None:
        """Persist and return an updated workshop."""

    @abstractmethod
    async def delete_workshop(self, workshop_id: str) -> None:
        """Delete a workshop."""

    @abstractmethod
    async def slug_exists(self, slug: str, exclude_id: str | None = None) -> bool:
        """Return whether a slug already exists."""
