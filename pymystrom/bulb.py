"""Support for communicating with myStrom bulbs."""
import asyncio
import logging

import aiohttp
from yarl import URL

from . import _request as request

_LOGGER = logging.getLogger(__name__)

URI_BULB = URL("api/v1/device")


class MyStromBulb:
    """A class for a myStrom bulb."""

    def __init__(
        self, host: str, mac: str, session: aiohttp.client.ClientSession = None,
    ):
        """Initialize the bulb."""
        self._close_session = False
        self._host = host
        self._mac = mac
        self._session = session
        self.brightness = 0
        self.color = None
        self.consumption = 0
        self.data = None
        self.firmware = None
        self.mode = None
        self.state = None
        self.transition_time = 0
        self.uri = URL.build(scheme="http", host=self._host).join(URI_BULB) / self._mac

    async def get_bulb_state(self) -> object:
        """Get the state of the bulb."""
        response = await request(self, uri=self.uri)
        print(response)
        return bool(response["on"])

    # async def get_power(self):
    #     """Get current power."""
    #     await self.get_status()
    #     try:
    #         self.consumption = self.data['power']
    #     except TypeError:
    #         self.consumption = 0
    #
    #     return self.consumption
    #
    # async def get_firmware(self):
    #     """Get the current firmware version."""
    #     await self.get_status()
    #     try:
    #         self.firmware = self.data['fw_version']
    #     except TypeError:
    #         self.firmware = 'Unknown'
    #
    #     return self.firmware
    #
    # async def get_brightness(self):
    #     """Get current brightness."""
    #     await self.get_status()
    #     try:
    #         self.brightness = self.data['color'].split(';')[-1]
    #     except TypeError:
    #         self.brightness = 0
    #
    #     return self.brightness
    #
    # async def get_transition_time(self):
    #     """Get the transition time in ms."""
    #     await self.get_status()
    #     try:
    #         self.transition_time = self.data['ramp']
    #     except TypeError:
    #         self.transition_time = 0
    #
    #     return self.transition_time
    #
    # async def get_color(self):
    #     """Get current color."""
    #     await self.get_status()
    #     try:
    #         self.color = self.data['color']
    #         self.mode = self.data['mode']
    #     except TypeError:
    #         self.color = 0
    #         self.mode = ''
    #
    #     return {'color': self.color, 'mode': self.mode}
    #
    async def set_on(self):
        """Turn the bulb on with the previous settings."""
        response = await request(
            self, uri=self.uri, method="POST", data={"action": "on"}
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
        response = await request(self, uri=self.uri, method="POST", data=data)
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
        response = await request(self, uri=self.uri, method="POST", data=data)
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
            await request(self, uri=self.uri, method="POST", data=data)
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
            self, uri=self.uri, method="POST", data={"ramp": int(round(value))}
        )
        return response

    async def set_off(self):
        """Turn the bulb off."""
        response = await request(
            self, uri=self.uri, method="POST", data={"action": "off"}
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
