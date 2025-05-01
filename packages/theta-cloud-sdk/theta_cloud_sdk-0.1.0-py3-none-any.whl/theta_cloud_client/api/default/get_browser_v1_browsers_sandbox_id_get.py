from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.browser_response import BrowserResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    sandbox_id: str,
    *,
    x_api_key: Union[None, Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_api_key, Unset):
        headers["x-api-key"] = x_api_key

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/browsers/{sandbox_id}",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[BrowserResponse, HTTPValidationError]]:
    if response.status_code == 200:
        data = response.json()
        try:
            return BrowserResponse.from_dict(data)
        except KeyError:
            # Fallback if expected fields are missing
            return BrowserResponse(
                id=data.get("id", ""),
                ws_url_http_endpoint=data.get("ws_url_http_endpoint", ""),
                vnc_url=data.get("vnc_url", ""),
            )
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[BrowserResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sandbox_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[BrowserResponse, HTTPValidationError]]:
    """Get Browser

    Args:
        sandbox_id (str):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BrowserResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        x_api_key=x_api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[BrowserResponse, HTTPValidationError]]:
    """Get Browser

    Args:
        sandbox_id (str):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BrowserResponse, HTTPValidationError]
    """

    return sync_detailed(
        sandbox_id=sandbox_id,
        client=client,
        x_api_key=x_api_key,
    ).parsed


async def asyncio_detailed(
    sandbox_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[BrowserResponse, HTTPValidationError]]:
    """Get Browser

    Args:
        sandbox_id (str):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BrowserResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        x_api_key=x_api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    x_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[BrowserResponse, HTTPValidationError]]:
    """Get Browser

    Args:
        sandbox_id (str):
        x_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BrowserResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            sandbox_id=sandbox_id,
            client=client,
            x_api_key=x_api_key,
        )
    ).parsed
