python-mystrom
==============

Python API for controlling `myStrom <https://mystrom.ch>`_ switches.

Requirements
------------

- `myStrom <https://mystrom.ch>`_ switch
- `requests <http://docs.python-requests.org/en/master/>`_
- Network connection

Example
-------
The sample below shows how to use this Python module.

.. code:: python

    import time
    import pymystrom

    plug = pymystrom.MyStromPlug('10.100.0.137')

    # Switch relay on
    plug.set_relay_on()

    # Get the state of the switch
    print('Relay state: ', plug.get_relay_state())
    print('Power consumption:', plug.get_consumption())

    # Switch relay off
    time.sleep(10)
    plug.set_relay_off()

License
-------
``python-mystrom`` licensed under MIT, for more details check LICENSE.