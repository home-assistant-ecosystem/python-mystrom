"""
Copyright (c) 2015-2017 Fabian Affolter <fabian@affolter-engineering.ch>

Licensed under MIT. All rights reserved.
"""


class MyStromError(Exception):
    """General MyStromError exception occurred."""

    pass


class MyStromConnectionError(MyStromError):
    """When a connection error is encountered."""

    pass


class MyStromNotVersionTwoSwitch(MyStromError):
    """When version 2 function is not supported."""

    pass
