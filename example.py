"""
Copyright (c) 2015-2016 Fabian Affolter <fabian@affolter-engineering.ch>

Licensed under MIT. All rights reserved.
"""
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
