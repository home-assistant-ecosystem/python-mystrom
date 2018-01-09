"""
Copyright (c) 2017-2018 Fabian Affolter <fabian@affolter-engineering.ch>

Licensed under MIT. All rights reserved.
"""
import pymystrom

bulb = pymystrom.MyStromBulb('192.168.0.51', '5CCF7FA0AFB0')

# Get the details of the bulb
print("Current color:", bulb.get_color())
print("Brightness:", bulb.get_brightness())
print("Transition time:", bulb.get_transition_time())
print("Firmware version:", bulb.get_firmware())
