"""Base details for the myStrom Python bindings."""
import asyncio
import json
import aiohttp
import async_timeout
from typing import Any, Mapping, Optional
import socket
from .exceptions import MyStromConnectionError, MyStromError

import pkg_resources

try:
    __version__ = pkg_resources.get_distribution("setuptools").version
except Exception:
    __version__ = "unknown"

TIMEOUT = 10
USER_AGENT = f"PythonMyStrom/{__version__}"


async def _request(
    self,
    uri: str,
    method: str = "GET",
    data: Optional[Any] = None,
    json_data: Optional[dict] = None,
    params: Optional[Mapping[str, str]] = None,
) -> Any:
    """Handle a request to the myStrom device."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/plain, */*",
    }

    if self._session is None:
        self._session = aiohttp.ClientSession()
        self._close_session = True

    try:
        with async_timeout.timeout(TIMEOUT):
            response = await self._session.request(
                method, uri, data=data, json=json_data, params=params, headers=headers,
            )
    except asyncio.TimeoutError as exception:
        raise MyStromConnectionError(
            "Timeout occurred while connecting to myStrom bulb."
        ) from exception
    except (aiohttp.ClientError, socket.gaierror) as exception:
        raise MyStromConnectionError(
            "Error occurred while communicating with myStrom bulb."
        ) from exception

    content_type = response.headers.get("Content-Type", "")
    if (response.status // 100) in [4, 5]:
        contents = await response.read()
        response.close()

        if content_type == "application/json":
            raise MyStromError(response.status, json.loads(contents.decode("utf8")))
        raise MyStromError(response.status, {"message": contents.decode("utf8")})
    if "application/json" in content_type:
        response_json = await response.json()
        return response_json

    return response.text
