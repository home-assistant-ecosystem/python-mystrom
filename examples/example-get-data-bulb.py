"""Example code for getting the data from a myStrom bulb."""
from pymystrom import bulb

bulb = bulb.MyStromBulb("192.168.0.51", "5CCF7FA0AFB0")

# Get the details of the bulb
print("Bulb state:", bulb.get_bulb_state())
print("Current color:", bulb.get_color())
print("Brightness:", bulb.get_brightness())
print("Power consumption:", bulb.get_power())
print("Transition time:", bulb.get_transition_time())
print("Firmware version:", bulb.get_firmware())
