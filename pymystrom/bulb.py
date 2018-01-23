"""
Copyright (c) 2015-2018 Fabian Affolter <fabian@affolter-engineering.ch>

Licensed under MIT. All rights reserved.
"""
import time

import requests

from . import exceptions
from . import URI


class MyStromBulb(object):
    """A class for a myStrom bulb."""

    def __init__(self, host, mac):
        """Initialize the bulb."""
        self.resource = 'http://{}'.format(host)
        self._mac = mac
        self.timeout = 5
        self.data = None
        self.state = None
        self.consumption = 0
        self.brightness = 0
        self.color = None
        self.firmware = None
        self.mode = None
        self.transition_time = 0

    def get_status(self):
        """Get the details from the bulb."""
        try:
            request = requests.get(
                '{}/{}/'.format(self.resource, URI), timeout=self.timeout)
            raw_data = request.json()
            # Doesn't always work !!!!!
            #self._mac = next(iter(self.raw_data))
            self.data = raw_data[self._mac]
            return self.data
        except (requests.exceptions.ConnectionError, ValueError):
            raise exceptions.MyStromConnectionError()

    def get_bulb_state(self):
        """Get the relay state."""
        self.get_status()
        try:
            self.state = self.data['on']
        except TypeError:
            self.state = False

        return bool(self.state)

    def get_power(self):
        """Get current power."""
        self.get_status()
        try:
            self.consumption = self.data['power']
        except TypeError:
            self.consumption = 0

        return self.consumption

    def get_firmware(self):
        """Get the current firmware version."""
        self.get_status()
        try:
            self.firmware = self.data['fw_version']
        except TypeError:
            self.firmware = 'Unknown'

        return self.firmware

    def get_brightness(self):
        """Get current brightness."""
        self.get_status()
        try:
            self.brightness = self.data['color'].split(';')[-1]
        except TypeError:
            self.brightness = 0

        return self.brightness

    def get_transition_time(self):
        """Get the transition time in ms."""
        self.get_status()
        try:
            self.transition_time = self.data['ramp']
        except TypeError:
            self.transition_time = 0

        return self.transition_time

    def get_color(self):
        """Get current color."""
        self.get_status()
        try:
            self.color = self.data['color']
            self.mode = self.data['mode']
        except TypeError:
            self.color = 0
            self.mode = ''

        return {'color': self.color, 'mode': self.mode}

    def set_on(self):
        """Turn the bulb on with the previous settings."""
        try:
            request = requests.post(
                '{}/{}/{}/'.format(self.resource, URI, self._mac),
                data={'action': 'on'}, timeout=self.timeout)
            if request.status_code == 200:
                pass
        except requests.exceptions.ConnectionError:
            raise exceptions.MyStromConnectionError()

    def set_color_hex(self, value):
        """Turn the bulb on with the given color as HEX.

        white: FF000000
        red:   00FF0000
        green: 0000FF00
        blue:  000000FF
        """
        data = {
            'action': 'on',
            'color': value,
        }

        try:
            request = requests.post(
                '{}/{}/{}/'.format(self.resource, URI, self._mac),
                json=data, timeout=self.timeout)
            if request.status_code == 200:
                pass
        except requests.exceptions.ConnectionError:
            raise exceptions.MyStromConnectionError()

    def set_color_hsv(self, hue, saturation, value):
        """Turn the bulb on with the given values as HSV."""
        try:
            data = "action=on&color={};{};{}".format(hue, saturation, value)
            request = requests.post(
                '{}/{}/{}'.format(self.resource, URI, self._mac),
                data=data, timeout=self.timeout)
            if request.status_code == 200:
                self.data['on'] = True
        except requests.exceptions.ConnectionError:
            raise exceptions.MyStromConnectionError()

    def set_white(self):
        """Turn the bulb on, full white."""
        self.set_color_hsv(0, 0, 100)

    def set_rainbow(self, duration):
        """Turn the bulb on and create a rainbow."""
        for i in range(0, 359):
            self.set_color_hsv(i, 100, 100)
            time.sleep(duration/359)

    def set_sunrise(self, duration):
        """Turn the bulb on and create a sunrise."""
        self.set_transition_time(duration/100)
        for i in range(0, duration):
            try:
                data = "action=on&color=3;{}".format(i)
                request = requests.post(
                    '{}/{}/{}'.format(self.resource, URI, self._mac),
                    data=data, timeout=self.timeout)
                if request.status_code == 200:
                    self.data['on'] = True
            except requests.exceptions.ConnectionError:
                raise exceptions.MyStromConnectionError()
            time.sleep(duration/100)

    def set_flashing(self, duration, hsv1, hsv2):
        """Turn the bulb on, flashing with two colors."""
        self.set_transition_time(100)
        for step in range(0, int(duration/2)):
            self.set_color_hsv(hsv1[0], hsv1[1], hsv1[2])
            time.sleep(1)
            self.set_color_hsv(hsv2[0], hsv2[1], hsv2[2])
            time.sleep(1)

    def set_transition_time(self, value):
        """Set the transition time in ms."""
        try:
            request = requests.post(
                '{}/{}/{}/'.format(self.resource, URI, self._mac),
                data={'ramp': value}, timeout=self.timeout)
            if request.status_code == 200:
                pass
        except requests.exceptions.ConnectionError:
            raise exceptions.MyStromConnectionError()

    def set_off(self):
        """Turn the bulb off."""
        try:
            request = requests.post(
                '{}/{}/{}/'.format(self.resource, URI, self._mac),
                data={'action': 'off'}, timeout=self.timeout)
            if request.status_code == 200:
                pass
        except requests.exceptions.ConnectionError:
            raise exceptions.MyStromConnectionError()
