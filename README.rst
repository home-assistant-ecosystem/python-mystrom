python-mystrom |License| |PyPI|
===================================

Python API for controlling `myStrom <https://mystrom.ch>`_ switches/plugs.

Requirements
------------
You need to have `Python <https://www.python.org>`_ installed.

- `myStrom <https://mystrom.ch>`_ switch
- `requests <http://docs.python-requests.org/en/master/>`_
- Network connection

Installation
------------
The package is available in the `Python Package Index <https://pypi.python.org/>`_ .

.. code:: bash

    $ pip install python-mystrom

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

    $ curl -X GET http://IP_ADDRESS_PLUG/relay?state=1

Example
-------
The sample below shows how to use this Python module.

.. code:: python

    import pymystrom

    plug = pymystrom.MyStromPlug('IP_ADDRESS_PLUG')

    # Preserve state
    STATE_ON = plug.get_relay_state()

    # Switch relay on if the plug is currently off
    if not STATE_ON:
        print('Relay will be switched on.')
        plug.set_relay_on()
        # Wait a few seconds to get a reading of the power consumption
        print('Waiting for a couple of seconds...')
        time.sleep(10)

    # Get the new state of the switch
    print('Relay state: ', plug.get_relay_state())
    print('Power consumption:', plug.get_consumption())

    # Switch relay off if it was off.
    if not STATE_ON:
        plug.set_relay_off()

License
-------
``python-mystrom`` is licensed under MIT, for more details check LICENSE.

.. |License| image:: https://img.shields.io/pypi/l/python-mystrom.svg
   :target: https://github.com/fabaff/python-mystrom/blob/master/LICENSE
   :alt: License
.. |PyPI| image:: https://img.shields.io/pypi/v/python-mystrom.svg
   :target: https://pypi.python.org/pypi/python-mystrom
   :alt: PyPI release
