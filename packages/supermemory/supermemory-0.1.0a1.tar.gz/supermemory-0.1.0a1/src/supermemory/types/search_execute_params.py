# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = ["SearchExecuteParams", "Filters", "FiltersUnionMember0"]


class SearchExecuteParams(TypedDict, total=False):
    q: Required[str]
    """Search query string"""

    categories_filter: Annotated[
        List[Literal["technology", "science", "business", "health"]], PropertyInfo(alias="categoriesFilter")
    ]
    """Optional category filters"""

    chunk_threshold: Annotated[float, PropertyInfo(alias="chunkThreshold")]
    """Maximum number of chunks to return"""

    doc_id: Annotated[str, PropertyInfo(alias="docId")]
    """Optional document ID to search within"""

    document_threshold: Annotated[float, PropertyInfo(alias="documentThreshold")]
    """Maximum number of documents to return"""

    filters: Filters
    """Optional filters to apply to the search"""

    include_summary: Annotated[bool, PropertyInfo(alias="includeSummary")]
    """If true, include document summary in the response.

    This is helpful if you want a chatbot to know the context of the document.
    """

    limit: int
    """Maximum number of results to return"""

    only_matching_chunks: Annotated[bool, PropertyInfo(alias="onlyMatchingChunks")]
    """If true, only return matching chunks without context"""

    user_id: Annotated[str, PropertyInfo(alias="userId")]
    """End user ID this search is associated with"""


class FiltersUnionMember0(TypedDict, total=False):
    and_: Annotated[Iterable[object], PropertyInfo(alias="AND")]

    or_: Annotated[Iterable[object], PropertyInfo(alias="OR")]


Filters: TypeAlias = Union[FiltersUnionMember0, Dict[str, object]]
