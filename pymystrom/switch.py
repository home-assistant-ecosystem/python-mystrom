"""Support for communicating with myStrom plugs/switches."""

from typing import Optional, Union

import aiohttp
from yarl import URL

from . import _request as request
from .device_types import DEVICE_MAPPING_LITERAL, DEVICE_MAPPING_NUMERIC


class MyStromSwitch:
    """A class for a myStrom switch/plug."""

    def __init__(
        self,
        host: str,
        session: aiohttp.client.ClientSession = None,
        token: Optional[str] = None,
    ) -> None:
        """Initialize the switch."""
        self._close_session = False
        self._host = host
        self._token = token
        self._session = session
        self._consumption = 0
        self._consumedWs = 0
        self._boot_id = None
        self._energy_since_boot = None
        self._time_since_boot = None
        self._state = None
        self._temperature = None
        self._firmware = None
        self._mac = None
        self._device_type: Optional[Union[str, int]] = None
        self.uri = URL.build(scheme="http", host=self._host)

    async def turn_on(self) -> None:
        """Turn the relay on."""
        parameters = {"state": "1"}
        url = URL(self.uri).join(URL("relay"))
        await request(self, uri=url, params=parameters, token=self._token)
        await self.get_state()

    async def turn_off(self) -> None:
        """Turn the relay off."""
        parameters = {"state": "0"}
        url = URL(self.uri).join(URL("relay"))
        await request(self, uri=url, params=parameters, token=self._token)
        await self.get_state()

    async def toggle(self) -> None:
        """Toggle the relay."""
        url = URL(self.uri).join(URL("toggle"))
        await request(self, uri=url, token=self._token)
        await self.get_state()

    async def get_state(self) -> None:
        """Get the details from the switch/plug."""
        url = URL(self.uri).join(URL("report"))
        response = await request(self, uri=url, token=self._token)
        try:
            self._consumption = response["power"]
        except KeyError:
            self._consumption = None
        try:
            self._consumedWs = response["Ws"]
        except KeyError:
            self._consumedWs = None
        try:
            self._boot_id = response["boot_id"]
        except KeyError:
            self._boot_id = None
        try:
            self._energy_since_boot = response["energy_since_boot"]
        except KeyError:
            self._energy_since_boot = None
        try:
            self._time_since_boot = response["time_since_boot"]
        except KeyError:
            self._time_since_boot = None
        self._state = response["relay"]
        try:
            self._temperature = response["temperature"]
        except KeyError:
            self._temperature = None

        # Try the new API (Devices with newer firmware)
        url = URL(self.uri).join(URL("api/v1/info"))
        response = await request(self, uri=url, token=self._token)
        if not isinstance(response, dict):
            # Fall back to the old API version if the device runs with old firmware
            url = URL(self.uri).join(URL("info.json"))
            response = await request(self, uri=url, token=self._token)

        # Tolerate missing keys on legacy firmware (e.g., v1 devices)
        self._firmware = response.get("version")
        self._mac = response.get("mac")
        self._device_type = response.get("type")

    @property
    def device_type(self) -> Optional[str]:
        """Return the device type as string (e.g. "Switch CH v1" or "Button+")."""
        if isinstance(self._device_type, int):
            return DEVICE_MAPPING_NUMERIC.get(self._device_type)
        elif isinstance(self._device_type, str):
            return DEVICE_MAPPING_LITERAL.get(self._device_type)
        return None

    @property
    def relay(self) -> bool:
        """Return the relay state."""
        return bool(self._state)

    @property
    def consumption(self) -> Optional[float]:
        """Return the current power consumption in mWh."""
        if self._consumption is not None:
            return round(self._consumption, 1)

        return self._consumption

    @property
    def consumedWs(self) -> Optional[float]:
        """The average of energy consumed per second since last report call."""
        if self._consumedWs is not None:
            return round(self._consumedWs, 1)

        return self._consumedWs

    @property
    def boot_id(self) -> Optional[str]:
        """A unique identifier to distinguish whether the energy counter has been reset."""
        return self._boot_id

    @property
    def energy_since_boot(self) -> Optional[float]:
        """The total energy in watt seconds (Ws) that has been measured since the last power-up or restart of the device."""
        if self._energy_since_boot is not None:
            return round(self._energy_since_boot, 2)

        return self._energy_since_boot

    @property
    def time_since_boot(self) -> Optional[int]:
        """The time in seconds that has elapsed since the last start or restart of the device."""
        return self._time_since_boot

    @property
    def firmware(self) -> Optional[str]:
        """Return the current firmware."""
        return self._firmware

    @property
    def mac(self) -> Optional[str]:
        """Return the MAC address."""
        return self._mac

    @property
    def temperature(self) -> Optional[float]:
        """Return the current temperature in Celsius."""
        if self._temperature is not None:
            return round(self._temperature, 1)

        return self._temperature

    async def get_temperature_full(self) -> str:
        """Get current temperature in celsius."""
        url = URL(self.uri).join(URL("temp"))
        response = await request(self, uri=url, token=self._token)
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
