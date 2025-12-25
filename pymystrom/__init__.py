"""Base details for the myStrom Python bindings."""

import asyncio
import socket
from typing import Any, Mapping, Optional

import aiohttp
from yarl import URL

from .exceptions import MyStromConnectionError

TIMEOUT = 10
USER_AGENT = "PythonMyStrom/1.0"


async def _request(
    self,
    uri: str,
    method: str = "GET",
    data: Optional[Any] = None,
    json_data: Optional[dict] = None,
    params: Optional[Mapping[str, str]] = None,
    token: Optional[str] = None,
) -> Any:
    """Handle a request to the myStrom device."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/plain, */*",
    }
    if token:
        headers["Token"] = token

    if self._session is None:
        self._session = aiohttp.ClientSession()
        self._close_session = True

    try:
        response = await asyncio.wait_for(
            self._session.request(
                method,
                uri,
                data=data,
                json=json_data,
                params=params,
                headers=headers,
            ),
            timeout=TIMEOUT,
        )
    except asyncio.TimeoutError as exception:
        raise MyStromConnectionError(
            "Timeout occurred while connecting to myStrom device."
        ) from exception
    except (aiohttp.ClientError, socket.gaierror) as exception:
        raise MyStromConnectionError(
            "Error occurred while communicating with myStrom device."
        ) from exception

    content_type = response.headers.get("Content-Type", "")
    if response.status == 404:
        raise MyStromConnectionError(
            "Error occurred while authenticating with myStrom device."
        )

    elif (response.status // 100) in [4, 5]:
        response.close()

    if "application/json" in content_type:
        response_json = await response.json()
        return response_json

    return response.text


class MyStromDevice:
    """A class for a myStrom device."""

    def __init__(
        self,
        host,
        session: aiohttp.client.ClientSession = None,
    ):
        """Initialize the device."""
        self._close_session = False
        self._host = host
        self._session = session
        self.uri = URL.build(scheme="http", host=self._host)

    async def get_device_info(self) -> dict:
        """Get the device info of a myStrom device."""
        url = URL(self.uri).join(URL("api/v1/info"))
        response = await _request(self, uri=url)
        if not isinstance(response, dict):
            # Fall back to the old API version if the device runs with old firmware
            url = URL(self.uri).join(URL("info.json"))
            response = await _request(self, uri=url)
        return response

    async def close(self) -> None:
        """Close an open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> "MyStromDevice":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close()


async def get_device_info(host: str) -> dict:
    """Get the device info of a myStrom device."""
    async with MyStromDevice(host) as device:
        return await device.get_device_info()
