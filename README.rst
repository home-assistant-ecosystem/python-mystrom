python-mystrom
==============
Python API for controlling `myStrom <https://mystrom.ch>`_ switches.

Requirements
------------
You need to have `Python <https://www.python.org>`_ installed.

- `myStrom <https://mystrom.ch>`_ switch
- `requests <http://docs.python-requests.org/en/master/>`_
- Network connection

Details
-------
At the moment the following endpoints are covered:

- ``/report``: for getting the current state and the power consumption
- ``/relay``: for setting the relay state

You will still be able to use your device with the smartphone application,
``curl``, or other tools. The samples below shows how to use the switch with
``httpie`` and ``curl`` along with ``python-mystrom``.

.. code:: bash

    $ http http://IP_ADDRESS_PLUG/report
    HTTP/1.1 200 OK
    Content-Length: 39
    Content-Type: application/json
    Date: Mon, 15 Feb 2016 17:52:21 GMT

    {
        "power": 51.630947,
        "relay": true
    }

.. code:: bash

    $ curl -XGET http://IP_ADDRESS_PLUG/relay?state=1

Example
-------
The sample below shows how to use this Python module.

.. code:: python

    import time
    import pymystrom

    plug = pymystrom.MyStromPlug('IP_ADDRESS_PLUG')

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
