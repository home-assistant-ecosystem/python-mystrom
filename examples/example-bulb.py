"""Example code for communicating with a myStrom bulb."""
import asyncio

from pymystrom.bulb import MyStromBulb

IP_ADDRESS = "192.168.0.50"
MAC_ADDRESS = "5CCF7FA0C93B"


async def main():
    """Sample code to work with a myStrom bulb."""
    async with MyStromBulb(IP_ADDRESS, MAC_ADDRESS) as bulb:
        print("Get the details from the bulb")
        print(await bulb.get_bulb_state())
        print("Bulb will be switched on with their previous setting")
        await bulb.set_on()
        # print("Waiting for a couple of seconds...")
        await asyncio.sleep(2)
        print("Bulb will be set to white")
        await bulb.set_white()
        # Wait a few seconds to get a reading of the power consumption
        print("Waiting for a couple of seconds...")

        await asyncio.sleep(2)
        # Set transition time to 2 s
        await bulb.set_transition_time(2000)

        # Set to blue as HEX
        await bulb.set_color_hex("000000FF")
        await asyncio.sleep(3)

        # Set color as HSV (Hue, Saturation, Value)
        await bulb.set_color_hsv(0, 0, 100)
        await asyncio.sleep(3)

        # Test a fast flashing sequence
        print("Flash it for 10 seconds...")
        await bulb.set_flashing(10, [100, 50, 30], [200, 0, 71])
        await bulb.set_off()

        # Show a sunrise within a minute
        print("Show a sunrise for 60 s")
        await bulb.set_sunrise(60)

        # Show a rainbow for 60 seconds
        print("Show a rainbow")
        await bulb.set_rainbow(60)
        # Reset transition time
        await bulb.set_transition_time(1000)

        # Shutdown the bulb
        await bulb.set_off()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
