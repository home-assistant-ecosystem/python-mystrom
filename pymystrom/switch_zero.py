"""Support for communicating with myStrom switch zero."""
import aiohttp
from yarl import URL

from . import _request as request


class MyStromSwitchZero:
    """A class for a myStrom switch zero plug."""

    def __init__(
        self, host: str, session: aiohttp.client.ClientSession = None
    ) -> None:
        """Initialize the switch."""
        self._close_session = False
        self._host = host
        self._session = session
        self._state = None
        self._firmware = None
        self._mac = None
        self.uri = URL.build(scheme="http", host=self._host)

    async def turn_on(self) -> None:
        """Turn the relay on."""
        parameters = {"state": "1"}
        url = URL(self.uri).join(URL("relay"))
        await request(self, uri=url, params=parameters)
        await self.get_state()

    async def turn_off(self) -> None:
        """Turn the relay off."""
        parameters = {"state": "0"}
        url = URL(self.uri).join(URL("relay"))
        await request(self, uri=url, params=parameters)
        await self.get_state()

    async def toggle(self) -> None:
        """Toggle the relay."""
        url = URL(self.uri).join(URL("toggle"))
        await request(self, uri=url)
        await self.get_state()

    async def get_state(self) -> None:
        """Get the details from the switch/plug."""
        url = URL(self.uri).join(URL("report"))
        response = await request(self, uri=url)
        self._state = response["relay"]

        url = URL(self.uri).join(URL("/api/v1/info"))
        response = await request(self, uri=url)
        self._firmware = response["version"]
        self._mac = response["mac"]

    @property
    def relay(self) -> bool:
        """Return the relay state."""
        return bool(self._state)

    @property
    def firmware(self) -> float:
        """Return the current firmware."""
        return self._firmware

    @property
    def mac(self) -> float:
        """Return the MAC address."""
        return self._mac

    async def close(self) -> None:
        """Close an open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> "MyStromSwitchZero":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close()
