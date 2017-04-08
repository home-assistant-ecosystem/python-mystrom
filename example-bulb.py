"""
Copyright (c) 2017 Fabian Affolter <fabian@affolter-engineering.ch>

Licensed under MIT. All rights reserved.
"""
import time
import pymystrom

bulb = pymystrom.MyStromBulb('192.168.0.52', '5CCF7FA0AFB0')

# Preserve state
STATE_ON = bulb.get_bulb_state()

#  Switch bulb on if the bulb is currently off
if not STATE_ON:
    print("Bulb will be switched on")
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

# Get the new state of the switch
print("Bulb state:", bulb.get_bulb_state())
print("Power consumption:", bulb.get_power())
print("Current color:", bulb.get_color())
print("Transition time:", bulb.get_transition_time())


# Switch off off if it was on.
#if STATE_ON:
bulb.set_transition_time(100)
print("Play with the colors...")
bulb.set_color_hex('0000FF00')
time.sleep(2)
bulb.set_color_hex('00FFFF00')
time.sleep(2)
bulb.set_color_hex('FFFFFF00')

# Test a fast flashing sequence
print("Flash it...")
bulb.set_transition_time(250)
bulb.set_color_hex('00FF0000')
time.sleep(1)
bulb.set_color_hex('0000FF00')
time.sleep(1)
bulb.set_color_hex('00FF0000')
time.sleep(1)
bulb.set_color_hex('0000FF00')
time.sleep(1)
bulb.set_color_hex('00FF0000')
time.sleep(1)
bulb.set_color_hex('0000FF00')
time.sleep(1)
bulb.set_color_hex('00FF0000')
time.sleep(1)
bulb.set_color_hex('0000FF00')

# Test a fast flashing sequence
print("Rainbow")
bulb.set_off()
bulb.set_rainbow(60)
#bulb.set_sunrise(60)

# Reset trasition time
bulb.set_transition_time(1000)
# Shutdown the bulb
bulb.set_off()
