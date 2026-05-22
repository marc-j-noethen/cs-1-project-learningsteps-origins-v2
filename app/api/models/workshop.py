from datetime import datetime
import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator

CATEGORY_PATTERN = re.compile(r"^[A-Za-z0-9.+#/\- ]{2,40}$")


def _clean_inline_text(value: str) -> str:
    return " ".join(value.split())


def _clean_multiline_text(value: str) -> str:
    cleaned_lines = [line.rstrip() for line in value.splitlines()]
    return "\n".join(cleaned_lines).strip()


def _normalize_list(value: list[str] | str) -> list[str]:
    if isinstance(value, str):
        chunks = [item.strip() for item in value.split(",")]
        return [item for item in chunks if item]
    return value


class WorkshopPayload(BaseModel):
    title: str = Field(..., min_length=3, max_length=120)
    category: str = Field(..., min_length=2, max_length=40)
    status: Literal["draft", "review", "published"] = "draft"
    difficulty: Literal["fundamentals", "intermediate", "advanced"] = "fundamentals"
    duration_hours: int = Field(..., ge=1, le=80)
    summary: str = Field(..., min_length=20, max_length=280)
    description: str = Field(..., min_length=40, max_length=4000)
    objectives: list[str] = Field(default_factory=list, min_length=2, max_length=8)
    stack: list[str] = Field(default_factory=list, min_length=1, max_length=8)
    published: bool = False

    @field_validator("title", "category", "summary", mode="before")
    @classmethod
    def normalize_inline_fields(cls, value: str) -> str:
        cleaned = _clean_inline_text(value)
        if not cleaned:
            raise ValueError("Field must not be empty.")
        return cleaned

    @field_validator("description", mode="before")
    @classmethod
    def normalize_description(cls, value: str) -> str:
        cleaned = _clean_multiline_text(value)
        if not cleaned:
            raise ValueError("Description must not be empty.")
        return cleaned

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str) -> str:
        if not CATEGORY_PATTERN.fullmatch(value):
            raise ValueError("Category contains unsupported characters.")
        return value

    @field_validator("objectives", "stack", mode="before")
    @classmethod
    def normalize_list_fields(cls, value: list[str] | str) -> list[str]:
        return _normalize_list(value)

    @field_validator("objectives")
    @classmethod
    def validate_objectives(cls, value: list[str]) -> list[str]:
        cleaned = [_clean_inline_text(item) for item in value if item and item.strip()]
        if len(cleaned) < 2:
            raise ValueError("Add at least two learning objectives.")
        deduplicated = list(dict.fromkeys(cleaned))
        if len(deduplicated) < 2:
            raise ValueError("Add at least two distinct learning objectives.")
        for item in deduplicated:
            if len(item) < 4 or len(item) > 120:
                raise ValueError("Each learning objective must be 4-120 characters long.")
        return deduplicated

    @field_validator("stack")
    @classmethod
    def validate_stack(cls, value: list[str]) -> list[str]:
        cleaned = [_clean_inline_text(item) for item in value if item and item.strip()]
        if not cleaned:
            raise ValueError("Add at least one stack item.")
        deduplicated = list(dict.fromkeys(cleaned))
        if not deduplicated:
            raise ValueError("Add at least one distinct stack item.")
        for item in deduplicated:
            if len(item) < 2 or len(item) > 40:
                raise ValueError("Each stack item must be 2-40 characters long.")
        return deduplicated

    model_config = {"str_strip_whitespace": True}


class WorkshopRecord(WorkshopPayload):
    id: str
    slug: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "json_encoders": {datetime: lambda value: value.isoformat()},
    }
