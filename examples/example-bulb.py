"""
Copyright (c) 2017-2018 Fabian Affolter <fabian@affolter-engineering.ch>

Licensed under MIT. All rights reserved.
"""
import time

from pymystrom import bulb

bulb = bulb.MyStromBulb('192.168.0.51', '5CCF7FA0AFB0')

# Preserve state
STATE_ON = bulb.get_bulb_state()

#  Switch bulb on if the bulb is currently off
if not STATE_ON:
    print("Bulb will be switched on with their previous setting")
    bulb.set_on()
    print("Waiting for a couple of seconds...")
    time.sleep(2)
    print("Bulb will be set to white")
    bulb.set_white()
    # Wait a few seconds to get a reading of the power consumption
    print("Waiting for a couple of seconds...")
    time.sleep(2)
    # Set transition time to 2 s
    bulb.set_transition_time(2000)
    # Set to blue as HEX
    bulb.set_color_hex('000000FF')
    time.sleep(3)
    # Set color as HSV (Hue, Saturation, Value)
    bulb.set_color_hsv(50, 100, 100)
    time.sleep(3)

# Test a fast flashing sequence
print("Flash it for 10 seconds")
bulb.set_flashing(10, [100, 50, 30], [200, 0, 71])
bulb.set_off()

# Test a fast flashing sequence
print("Show a sunrise")
bulb.set_sunrise(60)

# Show a rainbow for 60 seconds
print("Show a rainbow")
bulb.set_rainbow(60)

# Reset transition time
bulb.set_transition_time(1000)

# Shutdown the bulb
bulb.set_off()
