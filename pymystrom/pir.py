"""Support for communicating with myStrom PIRs."""

from typing import Any, Dict, Iterable, List, Optional, Union

import aiohttp
from yarl import URL

from . import _request as request

URI_PIR = URL("api/v1/")


class MyStromPir:
    """A class for a myStrom PIR."""

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
        self._intensity = None
        self._day = None
        self._light_raw = None
        self._sensors = None
        self._temperature_measured = None
        self._temperature_compensated = None
        self._temperature_compensation = None
        self._temperature_raw = None
        self._motion = None
        self._settings = None
        self._pir = None

        self._actions = None
        self.uri = URL.build(scheme="http", host=self._host).join(URI_PIR)

    async def get_settings(self) -> None:
        """Get the current settings from the PIR."""
        url = URL(self.uri).join(URL("settings"))
        response = await request(self, uri=url, token=self._token)
        self._settings = response

    async def get_actions(self) -> None:
        """Get the current action settings from the PIR."""
        url = URL(self.uri).join(URL("action"))
        response = await request(self, uri=url, token=self._token)
        self._actions = response

    async def get_pir(self) -> None:
        """Get the current PIR settings."""
        url = URL(self.uri).join(URL("settings/pir"))
        response = await request(self, uri=url, token=self._token)
        self._pir = response

    async def get_sensors_state(self) -> None:
        """Get the state of the sensors from the PIR."""
        url = URL(self.uri).join(URL("sensors"))
        response = await request(self, uri=url, token=self._token)
        # The return data has the be re-written as the temperature is not rounded
        self._sensors = {
            "motion": response["motion"],
            "light": response["light"],
            "temperature": round(response["temperature"], 2),
        }

    async def get_temperatures(self) -> None:
        """Get the temperatures from the PIR."""
        # There is a different URL for the temp endpoint
        url = URL.build(scheme="http", host=self._host) / "temp"
        response = await request(self, uri=url, token=self._token)
        self._temperature_raw = response
        self._temperature_measured = round(response["measured"], 2)
        self._temperature_compensated = round(response["compensated"], 2)
        self._temperature_compensation = round(response["compensation"], 3)

    async def get_motion(self) -> None:
        """Get the state of the motion sensor from the PIR."""
        url = URL(self.uri).join(URL("motion"))
        response = await request(self, uri=url, token=self._token)
        self._motion = response["motion"]

    async def get_light(self) -> None:
        """Get the state of the light sensor from the PIR."""
        url = URL(self.uri).join(URL("light"))
        response = await request(self, uri=url, token=self._token)
        self._intensity = response["intensity"]
        self._day = response["day"]
        self._light_raw = response["raw"]

    @property
    def settings(self) -> Optional[dict]:
        """Return current settings."""
        return self._settings

    @property
    def actions(self) -> Optional[dict]:
        """Return current action settings."""
        return self._actions

    @property
    def pir(self) -> Optional[dict]:
        """Return current PIR settings."""
        return self._pir

    @property
    def sensors(self) -> Optional[dict]:
        """Return current sensor values."""
        return self._sensors

    @property
    def temperature_measured(self) -> Optional[str]:
        """Return current measured temperature."""
        return self._temperature_measured

    @property
    def temperature_compensated(self) -> Optional[str]:
        """Return current compensated temperature."""
        return self._temperature_compensated

    @property
    def temperature_compensation(self) -> Optional[str]:
        """Return current temperature compensation."""
        return self._temperature_compensation

    @property
    def temperature_raw(self) -> Optional[dict]:
        """Return current raw temperature values."""
        return self._temperature_raw

    @property
    def motion(self) -> Optional[str]:
        """Return the state of the motion sensor."""
        return self._motion

    @property
    def intensity(self) -> Optional[str]:
        """Return the intensity reported by the light sensor."""
        return self._intensity

    @property
    def day(self) -> Optional[str]:
        """Return the information based on the thresholds set."""
        return self._day

    @property
    def light_raw(self) -> Optional[str]:
        """Return the raw data from the ADC."""
        return {
            "visible": self._light_raw["adc0"],
            "infrared": self._light_raw["adc1"],
        }

    async def close(self) -> None:
        """Close an open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> "MyStromPir":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close()
