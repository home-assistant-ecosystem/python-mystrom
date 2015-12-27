"""
Copyright (c) 2015 Fabian Affolter <fabian@affolter-engineering.ch>

Licensed under MIT. All rights reserved.
"""
import requests


class MyStromPlug(object):
    """ A class for a myStrom switch. """

    def __init__(self, host):
        self.resource = 'http://{}'.format(host)
        self.timeout = 10
        self.data = None
        self.consumption = 0
        self.update()

    def get_status(self):
        """ Gets the details from the switch. """
        try:
            request = requests.get('{}/report'.format(self.resource),
                                   timeout=10)
            self.data = request.json()
        except requests.exceptions.ConnectionError:
            print("No route to device: ", self.resource)
        except ValueError:
            print("No route to device: ", self.resource)
