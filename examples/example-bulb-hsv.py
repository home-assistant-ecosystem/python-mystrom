"""Example code for communicating with a myStrom bulb and HSV values."""
import time

from pymystrom import bulb

bulb = bulb.MyStromBulb("192.168.0.51", "5CCF7FA0AFB0")

bulb.set_color_hex("000000FF")

# Get the details of the bulb
print("Current color details:", bulb.get_color())

# Set color as HSV (Hue, Saturation, Value)
bulb.set_color_hsv(50, 100, 100)
time.sleep(3)

# Shutdown the bulb
bulb.set_off()
