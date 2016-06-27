"""
Copyright (c) 2015-2016 Fabian Affolter <fabian@affolter-engineering.ch>

Licensed under MIT. All rights reserved.
"""
import requests


class MyStromPlug(object):
    """A class for a myStrom switch."""

    def __init__(self, host):
        """Initialize the switch."""
        self.resource = 'http://{}'.format(host)
        self.timeout = 5
        self.data = None
        self.state = None
        self.consumption = None
        self.update()

    def set_relay_on(self):
        """Turn the relay on."""
        if not self.get_relay_state():
            try:
                request = requests.get('{}/relay'.format(self.resource),
                                       params={'state': '1'},
                                       timeout=self.timeout)
                if request.status_code == 200:
                    self.update()
            except requests.exceptions.ConnectionError:
                raise ConnectionError()

    def set_relay_off(self):
        """Turn the relay off."""
        if self.get_relay_state():
            try:
                request = requests.get('{}/relay'.format(self.resource),
                                       params={'state': '0'},
                                       timeout=self.timeout)
                if request.status_code == 200:
                    self.update()
            except requests.exceptions.ConnectionError:
                raise ConnectionError()

    def get_status(self):
        """Get the details from the switch."""
        try:
            request = requests.get('{}/report'.format(self.resource),
                                   timeout=self.timeout)
            self.data = request.json()
        except requests.exceptions.ConnectionError:
            raise ConnectionError()
        except ValueError:
            raise ConnectionError()

    def get_relay_state(self):
        """Get the relay state."""
        self.update()
        try:
            self.state = self.data['relay']
        except TypeError:
            self.state = None

        return self.state

    def get_consumption(self):
        """Get current power consumption in mWh."""
        self.update()
        try:
            self.consumption = self.data['power']
        except TypeError:
            self.consumption = 'N/A'

        return self.consumption

    def update(self):
        """Get current details from switch."""
        return self.get_status()
