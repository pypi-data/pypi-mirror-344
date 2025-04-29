# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["MemoryListResponse", "Memory", "Pagination"]


class Memory(BaseModel):
    id: str
    """Unique identifier of the memory"""

    created_at: datetime = FieldInfo(alias="createdAt")
    """Creation timestamp"""

    metadata: Dict[str, object]
    """Custom metadata associated with the memory"""

    status: Optional[Literal["queued", "extracting", "chunking", "embedding", "indexing", "done", "failed"]] = None
    """Processing status of the memory"""

    summary: Optional[str] = None
    """Summary of the memory content"""

    title: str
    """Title of the memory"""

    updated_at: datetime = FieldInfo(alias="updatedAt")
    """Last update timestamp"""

    url: Optional[str] = None
    """Source URL of the memory"""

    workflow_status: Optional[Literal["PENDING", "IN_PROGRESS", "COMPLETED", "FAILED"]] = FieldInfo(
        alias="workflowStatus", default=None
    )
    """Current workflow status"""


class Pagination(BaseModel):
    current_page: float = FieldInfo(alias="currentPage")

    limit: float

    total_items: float = FieldInfo(alias="totalItems")

    total_pages: float = FieldInfo(alias="totalPages")


class MemoryListResponse(BaseModel):
    memories: List[Memory]

    pagination: Pagination
    """Pagination metadata"""
