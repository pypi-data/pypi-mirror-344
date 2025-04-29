# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["MemoryGetResponse", "Doc"]


class Doc(BaseModel):
    created_at: str = FieldInfo(alias="createdAt")

    updated_at: str = FieldInfo(alias="updatedAt")

    metadata: Optional[Dict[str, object]] = None

    summary: Optional[str] = None

    title: Optional[str] = None


class MemoryGetResponse(BaseModel):
    doc: Doc

    status: Optional[str] = None
