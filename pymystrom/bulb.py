"""Support for communicating with myStrom bulbs."""

import asyncio
import logging
from typing import Optional

import aiohttp
from yarl import URL

from . import _request as request

_LOGGER = logging.getLogger(__name__)

URI_BULB = URL("api/v1/device")


class MyStromBulb:
    """A class for a myStrom bulb."""

    def __init__(
        self,
        host: str,
        mac: str,
        token: Optional[str] = None,
        session: aiohttp.client.ClientSession = None,
    ) -> None:
        """Initialize the bulb."""
        self._close_session = False
        self._host = host
        self._mac = mac
        self._session = session
        self.brightness = 0
        self._color = None
        self._consumption = 0
        self.data = None
        self._firmware = None
        self._mode = None
        self._bulb_type = None
        self._state = None
        self._transition_time = 0
        self.uri = URL.build(scheme="http", host=self._host).join(URI_BULB) / self._mac
        self.token = token

    async def get_state(self) -> None:
        """Get the state of the bulb."""
        response = await request(self, uri=self.uri, token=self.token)
        self._consumption = response[self._mac]["power"]
        self._firmware = response[self._mac]["fw_version"]
        self._color = response[self._mac]["color"]
        self._mode = response[self._mac]["mode"]
        self._transition_time = response[self._mac]["ramp"]
        self._state = bool(response[self._mac]["on"])
        self._bulb_type = response[self._mac]["type"]

    @property
    def firmware(self) -> Optional[str]:
        """Return current firmware."""
        return self._firmware

    @property
    def mac(self) -> str:
        """Return the MAC address."""
        return self._mac

    @property
    def consumption(self) -> Optional[float]:
        """Return current firmware."""
        return self._consumption

    @property
    def color(self) -> Optional[str]:
        """Return current color settings."""
        return self._color

    @property
    def mode(self) -> Optional[str]:
        """Return current mode."""
        return self._mode

    @property
    def transition_time(self) -> Optional[int]:
        """Return current transition time (ramp)."""
        return self._transition_time

    @property
    def bulb_type(self) -> Optional[str]:
        """Return the type of the bulb."""
        return self._bulb_type

    @property
    def state(self) -> Optional[str]:
        """Return the current state of the bulb."""
        return self._state

    async def set_on(self):
        """Turn the bulb on with the previous settings."""
        response = await request(
            self, uri=self.uri, method="POST", data={"action": "on"}, token=self.token
        )
        return response

    async def set_color_hex(self, value):
        """Turn the bulb on with the given color as HEX.

        white: FF000000
        red:   00FF0000
        green: 0000FF00
        blue:  000000FF
        """
        data = {
            "action": "on",
            "color": value,
        }
        response = await request(
            self, uri=self.uri, method="POST", data=data, token=self.token
        )
        return response

    async def set_color_hsv(self, hue, saturation, value):
        """Turn the bulb on with the given values as HSV."""
        # The current situation doesn't allow to send JSON to the bulb as
        # the firmware wants a string separated by ;. This is was
        # reported in 2018 to myStrom
        # data = {
        #     'action': 'on',
        #     'color': f"{hue};{saturation};{value}",
        # }
        data = "action=on&color={};{};{}".format(hue, saturation, value)
        response = await request(
            self, uri=self.uri, method="POST", data=data, token=self.token
        )
        return response

    async def set_white(self):
        """Turn the bulb on, full white."""
        await self.set_color_hsv(0, 0, 100)

    async def set_rainbow(self, duration):
        """Turn the bulb on and create a rainbow."""
        for i in range(0, 359):
            await self.set_color_hsv(i, 100, 100)
            await asyncio.sleep(duration / 359)

    async def set_sunrise(self, duration):
        """Turn the bulb on and create a sunrise.

        The brightness is from 0 till 100.
        """
        max_brightness = 100
        await self.set_transition_time((duration / max_brightness))
        for i in range(0, duration):
            data = "action=on&color=3;{}".format(i)
            await request(
                self, uri=self.uri, method="POST", data=data, token=self.token
            )
            await asyncio.sleep(duration / max_brightness)

    async def set_flashing(self, duration, hsv1, hsv2):
        """Turn the bulb on, flashing with two colors."""
        await self.set_transition_time(100)
        for step in range(0, int(duration / 2)):
            await self.set_color_hsv(hsv1[0], hsv1[1], hsv1[2])
            await asyncio.sleep(1)
            await self.set_color_hsv(hsv2[0], hsv2[1], hsv2[2])
            await asyncio.sleep(1)

    async def set_transition_time(self, value):
        """Set the transition time in ms."""
        response = await request(
            self,
            uri=self.uri,
            method="POST",
            data={"ramp": int(round(value))},
            token=self.token,
        )
        return response

    async def set_off(self):
        """Turn the bulb off."""
        response = await request(
            self, uri=self.uri, method="POST", data={"action": "off"}, token=self.token
        )
        return response

    async def close(self) -> None:
        """Close an open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> "MyStromBulb":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close()
