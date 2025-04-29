# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import connection_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.connection_create_response import ConnectionCreateResponse

__all__ = ["ConnectionResource", "AsyncConnectionResource"]


class ConnectionResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ConnectionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/supermemoryai/python-sdk#accessing-raw-response-data-eg-headers
        """
        return ConnectionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConnectionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/supermemoryai/python-sdk#with_streaming_response
        """
        return ConnectionResourceWithStreamingResponse(self)

    def create(
        self,
        app: Literal["notion", "google-drive"],
        *,
        id: str,
        redirect_url: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConnectionCreateResponse:
        """
        Initialize connection and get authorization URL

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not app:
            raise ValueError(f"Expected a non-empty value for `app` but received {app!r}")
        return self._get(
            f"/connect/{app}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "id": id,
                        "redirect_url": redirect_url,
                    },
                    connection_create_params.ConnectionCreateParams,
                ),
            ),
            cast_to=ConnectionCreateResponse,
        )

    def retrieve(
        self,
        connection_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not connection_id:
            raise ValueError(f"Expected a non-empty value for `connection_id` but received {connection_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/connections/{connection_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncConnectionResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncConnectionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/supermemoryai/python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncConnectionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConnectionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/supermemoryai/python-sdk#with_streaming_response
        """
        return AsyncConnectionResourceWithStreamingResponse(self)

    async def create(
        self,
        app: Literal["notion", "google-drive"],
        *,
        id: str,
        redirect_url: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConnectionCreateResponse:
        """
        Initialize connection and get authorization URL

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not app:
            raise ValueError(f"Expected a non-empty value for `app` but received {app!r}")
        return await self._get(
            f"/connect/{app}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "id": id,
                        "redirect_url": redirect_url,
                    },
                    connection_create_params.ConnectionCreateParams,
                ),
            ),
            cast_to=ConnectionCreateResponse,
        )

    async def retrieve(
        self,
        connection_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not connection_id:
            raise ValueError(f"Expected a non-empty value for `connection_id` but received {connection_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/connections/{connection_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class ConnectionResourceWithRawResponse:
    def __init__(self, connection: ConnectionResource) -> None:
        self._connection = connection

        self.create = to_raw_response_wrapper(
            connection.create,
        )
        self.retrieve = to_raw_response_wrapper(
            connection.retrieve,
        )


class AsyncConnectionResourceWithRawResponse:
    def __init__(self, connection: AsyncConnectionResource) -> None:
        self._connection = connection

        self.create = async_to_raw_response_wrapper(
            connection.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            connection.retrieve,
        )


class ConnectionResourceWithStreamingResponse:
    def __init__(self, connection: ConnectionResource) -> None:
        self._connection = connection

        self.create = to_streamed_response_wrapper(
            connection.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            connection.retrieve,
        )


class AsyncConnectionResourceWithStreamingResponse:
    def __init__(self, connection: AsyncConnectionResource) -> None:
        self._connection = connection

        self.create = async_to_streamed_response_wrapper(
            connection.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            connection.retrieve,
        )
