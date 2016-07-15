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
        self.consumption = 0

    def set_relay_on(self):
        """Turn the relay on."""
        if not self.get_relay_state():
            try:
                request = requests.get('{}/relay'.format(self.resource),
                                       params={'state': '1'},
                                       timeout=self.timeout)
                if request.status_code == 200:
                    self.data['relay'] = True
            except requests.exceptions.ConnectionError:
                self.data['relay'] = False

    def set_relay_off(self):
        """Turn the relay off."""
        if self.get_relay_state():
            try:
                request = requests.get('{}/relay'.format(self.resource),
                                       params={'state': '0'},
                                       timeout=self.timeout)
                if request.status_code == 200:
                    self.data['relay'] = False
            except requests.exceptions.ConnectionError:
                self.data['relay'] = False

    def get_status(self):
        """Get the details from the switch."""
        try:
            request = requests.get('{}/report'.format(self.resource),
                                   timeout=self.timeout)
            self.data = request.json()
            return self.data
        except (requests.exceptions.ConnectionError, ValueError):
            self.data = {'relay': False, 'power': 0}
            return self.data

    def get_relay_state(self):
        """Get the relay state."""
        self.get_status()
        try:
            self.state = self.data['relay']
        except TypeError:
            self.state = False

        return bool(self.state)

    def get_consumption(self):
        """Get current power consumption in mWh."""
        self.get_status()
        try:
            self.consumption = self.data['power']
        except TypeError:
            self.consumption = 0

        return self.consumption
