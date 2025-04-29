# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["SettingUpdateParams", "FilterTag"]


class SettingUpdateParams(TypedDict, total=False):
    categories: List[str]

    exclude_items: Annotated[List[str], PropertyInfo(alias="excludeItems")]

    filter_prompt: Annotated[str, PropertyInfo(alias="filterPrompt")]

    filter_tags: Annotated[Iterable[FilterTag], PropertyInfo(alias="filterTags")]

    include_items: Annotated[List[str], PropertyInfo(alias="includeItems")]

    should_llm_filter: Annotated[bool, PropertyInfo(alias="shouldLLMFilter")]


class FilterTag(TypedDict, total=False):
    score: Required[float]

    tag: Required[str]
