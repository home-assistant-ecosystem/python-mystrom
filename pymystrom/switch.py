"""Support for communicating with myStrom plugs/switches."""
import aiohttp
from yarl import URL
from typing import Any, Dict, Iterable, List, Optional, Union

from . import _request as request


class MyStromSwitch:
    """A class for a myStrom switch/plug."""

    def __init__(
        self,
        host: str,
        token: Optional[str] = None,
        session: aiohttp.client.ClientSession = None
    ) -> None:
        """Initialize the switch."""
        self._close_session = False
        self._host = host
        self._session = session
        self._consumption = 0
        self._consumedWs = 0
        self._state = None
        self._temperature = None
        self._firmware = None
        self._mac = None
        self.uri = URL.build(scheme="http", host=self._host)
        self.token = token

    async def turn_on(self) -> None:
        """Turn the relay on."""
        parameters = {"state": "1"}
        url = URL(self.uri).join(URL("relay"))
        await request(self, uri=url, params=parameters, token=self.token)
        await self.get_state()

    async def turn_off(self) -> None:
        """Turn the relay off."""
        parameters = {"state": "0"}
        url = URL(self.uri).join(URL("relay"))
        await request(self, uri=url, params=parameters, token=self.token)
        await self.get_state()

    async def toggle(self) -> None:
        """Toggle the relay."""
        url = URL(self.uri).join(URL("toggle"))
        await request(self, uri=url, token=self.token)
        await self.get_state()

    async def get_state(self) -> None:
        """Get the details from the switch/plug."""
        url = URL(self.uri).join(URL("report"))
        response = await request(self, uri=url, token=self.token)
        self._consumption = response["power"]
        self._consumedWs = response["Ws"]
        self._state = response["relay"]
        try:
            self._temperature = response["temperature"]
        except KeyError:
            self._temperature = None

        url = URL(self.uri).join(URL("info.json"))
        response = await request(self, uri=url, token=self.token)
        self._firmware = response["version"]
        self._mac = response["mac"]

    @property
    def relay(self) -> bool:
        """Return the relay state."""
        return bool(self._state)

    @property
    def consumption(self) -> float:
        """Return the current power consumption in mWh."""
        return round(self._consumption, 1)

    @property
    def consumedWs(self) -> float:
        """The average of energy consumed per second since last report call."""
        return round(self._consumedWs, 1)

    @property
    def firmware(self) -> float:
        """Return the current firmware."""
        return self._firmware

    @property
    def mac(self) -> float:
        """Return the MAC address."""
        return self._mac

    @property
    def temperature(self) -> float:
        """Return the current temperature in celsius."""
        if self._temperature is not None:
            return round(self._temperature, 1)

        return self._temperature

    async def get_temperature_full(self) -> str:
        """Get current temperature in celsius."""
        url = URL(self.uri).join(URL("temp"))
        response = await request(self, uri=url, token=self.token)
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
