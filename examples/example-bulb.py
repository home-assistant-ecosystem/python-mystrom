"""Example code for communicating with a myStrom bulb."""
import asyncio
import logging 

from pymystrom.bulb import MyStromBulb
from pymystrom.discovery import discover_devices

IP_ADDRESS = "192.168.0.51"
MAC_ADDRESS = "5CCF7FA0AFB0"


async def main():
    """Sample code to work with a myStrom bulb."""
    # Discover myStrom bulbs devices
    devices = await discover_devices()

    print(f"Found {len(devices)} bulb(s)")
    for device in devices:
        print(
            f"  IP address: {device.host}, MAC address: {device.mac}"
        )

    async with MyStromBulb(IP_ADDRESS, MAC_ADDRESS) as bulb:
        print("Get the details from the bulb...")
        await bulb.get_state()

        print("Power consumption:", bulb.consumption)
        print("Firmware:", bulb.firmware)
        print("Current state:", "off" if bulb.state is False else "on")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
