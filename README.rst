python-mystrom |License| |PyPI|
===================================

Asynchronous Python API client for interacting with `myStrom <https://mystrom.ch>`_
devices.

This module is not official, developed, supported or endorsed by myStrom AG.
For questions and other inquiries, use the issue tracker in this repo please.

Without the support of myStrom AG it would have taken much longer to create
this module which is the base for the integration into
`Home Assistant <https://home-assistant.io>`_. myStrom AG has provided hardware.
Their continuous support make further development of this module possible.

Requirements
------------

You need to have `Python <https://www.python.org>`_ installed.

- `myStrom <https://mystrom.ch>`_ device (bulb, plug or button)
- The ``python-mystrom`` requirements
- Network connection
- Devices connected to your network

Installation
------------

The package is available in the `Python Package Index <https://pypi.python.org/>`_ .

.. code:: bash

    $ pip3 install python-mystrom

On a Fedora-based system or on a CentOS/RHEL machine which has EPEL enabled.

.. code:: bash

    $ sudo dnf -y install python3-mystrom

For Nix or NixOS users is a package available. Keep in mind that the lastest releases might only
be present in the ``unstable`` channel.

.. code:: bash

    $ nix-env -iA nixos.python3Packages.python-mystrom


Plug/switch
-----------

At the moment the following endpoints are covered according `https://api.mystrom.ch <https://api.mystrom.ch>`_:

- ``/report``: for getting the current state and the power consumption
- ``/relay``: for setting the relay state

You will still be able to use your device with the smartphone application,
``curl`` or other tools. The samples below shows how to use the switch with
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


Bulb
----

If the bulb is on then you should be able to retrieve the current state of
the bulb.

Browse to http://IP_ADDRESS_BULB/api/v1/device/MAC_ADDRESS_BULB or use a
command-line tool.

.. code:: bash

    $ curl -d "color=0;0;100" -d "action=on" http://IP_ADDRESS_BULB/api/v1/device/MAC_ADDRESS_BULB
    {
	"5DFF7FAHZ987": 	{
		"on": true,
		"color": "0;0;100",
		"mode": "hsv",
		"ramp": 100,
		"notifyurl": ""
	    }
    }

The bulbs are not able to handle payload formatted as JSON. It's required to
use ``application/x-www-form-urlencoded``. Keep that in mind if something is
not working, especially around setting the color with HSV.

If you are planning to use your bulbs with `Home Assistant <https://home-assistant.io>`_
set the bulb to a state from `Colors` with the app or use the command below.

.. code:: bash

    $ curl -d "color=0;0;100" IP_ADDRESS_BULB/api/v1/device/MAC_ADDRESS_BULB


Set State
`````````

You can set the state with a POST request and a payload.

- **on**: ``curl -d "action=on" http://IP_ADDRESS_BULB/api/v1/device/MAC_ADDRESS_BULB``
- **off**:  ``curl -d "action=off" http://IP_ADDRESS_BULB/api/v1/device/MAC_ADDRESS_BULB``
- **toggle**: ``$ curl -d "action=toggle" http://IP_ADDRESS_BULB/api/v1/device/MAC_ADDRESS_BULB``

Set Color RGB
`````````````

One of the supported modes for setting the color is **RBG**.

- **white**: ``$ curl -d "color=FF000000" http://IP_ADDRESS_BULB/api/v1/device/MAC_ADDRESS_BULB``
- **red**: ``$ curl -d "color=00FF0000" http://IP_ADDRESS_BULB/api/v1/device/MAC_ADDRESS_BULB``
- **green**: ``$ curl -d "color=0000FF00" http://IP_ADDRESS_BULB/api/v1/device/MAC_ADDRESS_BULB``
- **blue**: ``$ curl -d "color=000000FF" http://IP_ADDRESS_BULB/api/v1/device/MAC_ADDRESS_BULB``

Set Color HSV (Hue, Saturation, Value)
``````````````````````````````````````

It's also possible to use **HSV**.

.. code:: bash

    $ curl -d "color=0;0;100" http://IP_ADDRESS_BULB/api/v1/device/MAC_ADDRESS_BULB

While "color=" is composed with hue, saturation, and value.

Set Mono (white)
````````````````

If you only want to set the "white" color of the bulb, use **mono**.

.. code:: bash

    $ curl -d "color=10;100" http://IP_ADDRESS_BULB/api/v1/device/MAC_ADDRESS_BULB

"color=" contains the value for the color temperature (from 1 to 18) and the
brightness (from 0 to 100).

Dimming (ramp)
``````````````

Add **ramp** and an interval to set up the transition time while changing
colors.

.. code:: bash

    $ curl -d "action=on&ramp=1000&color=00FF0000" http://IP_ADDRESS_BULB/api/v1/device/MAC_ADDRESS_BULB

The unit of measurement for ramp is milliseconds (ms).

Button
------

The buttons can be set with the myStrom app or directly via HTTP requests.

To set the configuration the payload must contains the relevant details for
the actions:

``$ curl -v -d "single=<url>&double=<url>&long=<url>&touch=<url>" http://IP_ADDRESS_BUTTON/api/v1/device/MAC_ADDRESS_BUTTON``

Available actions:

- **single**: Short push (approx. 1/2 seconds)
- **double**: 2x sequential short pushes (within 2 seconds)
- **long**: Long push (approx. 2 seconds)
- **touch**: Touch of the button's surface (only affective for the WiFi
  Button +)

The button is set up to extend the life span of the battery as much as
possible. This means that only within the first 3 minutes or when connected
to an USB port/USB charger and the battery is not full, the button is able
to receive configuration information or publish its details.

``mystrom`` helper tool
-----------------------

The command-line tool ``mystrom`` can help to set up the buttons and get the
details from bulbs and plugs.

.. code:: bash

   $ mystrom
   Usage: mystrom [OPTIONS] COMMAND [ARGS]...

     Simple command-line tool to get and set the values of a myStrom devices.

     This tool can set the targets of a myStrom button for the different
     available actions single, double, long and touch.

   Options:
     --version  Show the version and exit.
     --help     Show this message and exit.

   Commands:
     bulb    Get and set details of a myStrom bulb.
     button  Get and set details of a myStrom button.
     config  Get and set the configuration of a myStrom...

The examples shows how to get the details of a given bulb.

.. code:: bash

   $ mystrom config read
   IP address of the myStrom device: IP_ADDRESS_BULB
   MAC address of the device: MAC_ADDRESS_BULB
   Read configuration from IP_ADDRESS_BULB
   {
      'MAC_ADDRESS_BULB':{
         'type':'rgblamp',
         'battery':False,
         'reachable':True,
         'meshroot':False,
         'on':True,
         'color':'191;90;14',
         'mode':'hsv',
         'ramp':100,
         'power':0.953,
         'fw_version':'2.25'
      }
   }

Example usage of the module
---------------------------

Examples for the bulb can be found in the directory ``examples``.

License
-------

``python-mystrom`` is licensed under MIT, for more details check LICENSE.

.. |License| image:: https://img.shields.io/badge/License-MIT-green.svg
   :target: https://pypi.python.org/pypi/python-mystrom
   :alt: License

.. |PyPI| image:: https://img.shields.io/pypi/v/python-mystrom.svg
   :target: https://pypi.python.org/pypi/python-mystrom
   :alt: PyPI release
