# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["SettingUpdateResponse", "Settings", "SettingsFilterTag"]


class SettingsFilterTag(BaseModel):
    score: float

    tag: str


class Settings(BaseModel):
    categories: Optional[List[str]] = None

    exclude_items: Optional[List[str]] = FieldInfo(alias="excludeItems", default=None)

    filter_prompt: Optional[str] = FieldInfo(alias="filterPrompt", default=None)

    filter_tags: Optional[List[SettingsFilterTag]] = FieldInfo(alias="filterTags", default=None)

    include_items: Optional[List[str]] = FieldInfo(alias="includeItems", default=None)

    should_llm_filter: Optional[bool] = FieldInfo(alias="shouldLLMFilter", default=None)


class SettingUpdateResponse(BaseModel):
    message: str

    settings: Settings
