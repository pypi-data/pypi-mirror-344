# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["MemoryCreateParams"]


class MemoryCreateParams(TypedDict, total=False):
    content: Required[str]
    """Content of the memory"""

    id: str

    metadata: Dict[str, Union[str, float, bool]]
    """Optional metadata for the memory"""

    user_id: Annotated[str, PropertyInfo(alias="userId")]
    """Optional end user ID this memory belongs to"""
