"""Support for communicating with myStrom plugs/switches."""
import aiohttp
from yarl import URL

from . import _request as request


class MyStromSwitch:
    """A class for a myStrom switch."""

    def __init__(self, host: str, session: aiohttp.client.ClientSession = None) -> None:
        """Initialize the switch."""
        self._close_session = False
        self._host = host
        self._session = session
        self._consumption = 0
        self._state = None
        self._temperature = None
        self.uri = URL.build(scheme="http", host=self._host)

    async def turn_on(self) -> None:
        """Turn the relay on."""
        parameters = {"state": "1"}
        url = URL(self.uri).join(URL("relay"))
        await request(self, uri=url, params=parameters)
        await self.get_status()

    async def turn_off(self) -> None:
        """Turn the relay off."""
        parameters = {"state": "0"}
        url = URL(self.uri).join(URL("relay"))
        await request(self, uri=url, params=parameters)
        await self.get_status()

    async def toggle(self) -> None:
        """Toggle the relay."""
        url = URL(self.uri).join(URL("toggle"))
        await request(self, uri=url)
        await self.get_status()

    async def get_status(self) -> None:
        """Get the details from the switch."""
        url = URL(self.uri).join(URL("report"))
        response = await request(self, uri=url)
        self._consumption = response["power"]
        self._state = response["relay"]
        try:
            self._temperature = response["temperature"]
        except KeyError:
            self._temperature = 0

    @property
    def relay(self) -> bool:
        """Return the relay state."""
        return bool(self._state)

    @property
    def consumption(self) -> float:
        """Return the current power consumption in mWh."""
        return round(self._consumption, 1)

    @property
    def temperature(self) -> float:
        """Return the current temperature in celsius."""
        return round(self._temperature, 1)

    async def get_temperature_full(self) -> str:
        """Get current temperature in celsius."""
        url = URL(self.uri).join(URL("temp"))
        response = await request(self, uri=url)
        return response

    async def close(self) -> None:
        """Close an open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> "MyStromSwitch":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close()
