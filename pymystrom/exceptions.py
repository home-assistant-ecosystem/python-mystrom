"""All exceptions for the myStrom Python bindings."""


class MyStromError(Exception):
    """General MyStromError exception occurred."""

    pass


class MyStromConnectionError(MyStromError):
    """When a connection error is encountered."""

    pass


class MyStromNotVersionTwoSwitch(MyStromError):
    """When version 2 function is not supported."""

    pass
