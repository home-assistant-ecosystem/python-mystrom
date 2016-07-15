"""
Copyright (c) 2015-2016 Fabian Affolter <fabian@affolter-engineering.ch>

Licensed under MIT. All rights reserved.
"""


class MyStromError(Exception):
    """General MyStromError exception occurred."""

    pass


class MyStromConnectionError(MyStromError):
    """When a connection error is encountered."""

    pass
