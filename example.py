"""
Copyright (c) 2015-2016 Fabian Affolter <fabian@affolter-engineering.ch>

Licensed under MIT. All rights reserved.
"""
import time
import pymystrom

plug = pymystrom.MyStromPlug('10.100.0.137')

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
