# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from supermemory import Supermemory, AsyncSupermemory
from tests.utils import assert_matches_type
from supermemory.types import (
    MemoryGetResponse,
    MemoryListResponse,
    MemoryCreateResponse,
    MemoryDeleteResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMemory:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Supermemory) -> None:
        memory = client.memory.create(
            content="This is a detailed article about machine learning concepts...",
        )
        assert_matches_type(MemoryCreateResponse, memory, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: Supermemory) -> None:
        memory = client.memory.create(
            content="This is a detailed article about machine learning concepts...",
            id="id",
            metadata={
                "source": "web",
                "category": "technology",
                "tag_1": "ai",
                "tag_2": "machine-learning",
                "readingTime": 5,
                "isPublic": True,
            },
            user_id="user_123",
        )
        assert_matches_type(MemoryCreateResponse, memory, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Supermemory) -> None:
        response = client.memory.with_raw_response.create(
            content="This is a detailed article about machine learning concepts...",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(MemoryCreateResponse, memory, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Supermemory) -> None:
        with client.memory.with_streaming_response.create(
            content="This is a detailed article about machine learning concepts...",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = response.parse()
            assert_matches_type(MemoryCreateResponse, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Supermemory) -> None:
        memory = client.memory.list()
        assert_matches_type(MemoryListResponse, memory, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: Supermemory) -> None:
        memory = client.memory.list(
            filters='{"AND":[{"key":"group","value":"jira_users","negate":false},{"filterType":"numeric","key":"timestamp","value":"1742745777","negate":false,"numericOperator":">"}]}',
            limit="10",
            order="desc",
            page="1",
            sort="createdAt",
        )
        assert_matches_type(MemoryListResponse, memory, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Supermemory) -> None:
        response = client.memory.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(MemoryListResponse, memory, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Supermemory) -> None:
        with client.memory.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = response.parse()
            assert_matches_type(MemoryListResponse, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: Supermemory) -> None:
        memory = client.memory.delete(
            "id",
        )
        assert_matches_type(MemoryDeleteResponse, memory, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: Supermemory) -> None:
        response = client.memory.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(MemoryDeleteResponse, memory, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: Supermemory) -> None:
        with client.memory.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = response.parse()
            assert_matches_type(MemoryDeleteResponse, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: Supermemory) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.memory.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_get(self, client: Supermemory) -> None:
        memory = client.memory.get(
            "id",
        )
        assert_matches_type(MemoryGetResponse, memory, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get(self, client: Supermemory) -> None:
        response = client.memory.with_raw_response.get(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = response.parse()
        assert_matches_type(MemoryGetResponse, memory, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get(self, client: Supermemory) -> None:
        with client.memory.with_streaming_response.get(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = response.parse()
            assert_matches_type(MemoryGetResponse, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get(self, client: Supermemory) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.memory.with_raw_response.get(
                "",
            )


class TestAsyncMemory:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncSupermemory) -> None:
        memory = await async_client.memory.create(
            content="This is a detailed article about machine learning concepts...",
        )
        assert_matches_type(MemoryCreateResponse, memory, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSupermemory) -> None:
        memory = await async_client.memory.create(
            content="This is a detailed article about machine learning concepts...",
            id="id",
            metadata={
                "source": "web",
                "category": "technology",
                "tag_1": "ai",
                "tag_2": "machine-learning",
                "readingTime": 5,
                "isPublic": True,
            },
            user_id="user_123",
        )
        assert_matches_type(MemoryCreateResponse, memory, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.memory.with_raw_response.create(
            content="This is a detailed article about machine learning concepts...",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = await response.parse()
        assert_matches_type(MemoryCreateResponse, memory, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSupermemory) -> None:
        async with async_client.memory.with_streaming_response.create(
            content="This is a detailed article about machine learning concepts...",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = await response.parse()
            assert_matches_type(MemoryCreateResponse, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncSupermemory) -> None:
        memory = await async_client.memory.list()
        assert_matches_type(MemoryListResponse, memory, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSupermemory) -> None:
        memory = await async_client.memory.list(
            filters='{"AND":[{"key":"group","value":"jira_users","negate":false},{"filterType":"numeric","key":"timestamp","value":"1742745777","negate":false,"numericOperator":">"}]}',
            limit="10",
            order="desc",
            page="1",
            sort="createdAt",
        )
        assert_matches_type(MemoryListResponse, memory, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.memory.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = await response.parse()
        assert_matches_type(MemoryListResponse, memory, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSupermemory) -> None:
        async with async_client.memory.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = await response.parse()
            assert_matches_type(MemoryListResponse, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncSupermemory) -> None:
        memory = await async_client.memory.delete(
            "id",
        )
        assert_matches_type(MemoryDeleteResponse, memory, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.memory.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = await response.parse()
        assert_matches_type(MemoryDeleteResponse, memory, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSupermemory) -> None:
        async with async_client.memory.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = await response.parse()
            assert_matches_type(MemoryDeleteResponse, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSupermemory) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.memory.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_get(self, async_client: AsyncSupermemory) -> None:
        memory = await async_client.memory.get(
            "id",
        )
        assert_matches_type(MemoryGetResponse, memory, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get(self, async_client: AsyncSupermemory) -> None:
        response = await async_client.memory.with_raw_response.get(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        memory = await response.parse()
        assert_matches_type(MemoryGetResponse, memory, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncSupermemory) -> None:
        async with async_client.memory.with_streaming_response.get(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            memory = await response.parse()
            assert_matches_type(MemoryGetResponse, memory, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get(self, async_client: AsyncSupermemory) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.memory.with_raw_response.get(
                "",
            )
