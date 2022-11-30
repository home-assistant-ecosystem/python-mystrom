"""Example code for communicating with a myStrom switch zero."""
import asyncio

from pymystrom.switch_zero import MyStromSwitchZero

IP_ADDRESS = "192.168.1.168"


async def main():
    """Sample code to work with a myStrom switch."""
    async with MyStromSwitchZero(IP_ADDRESS) as switch:

        # Collect the data of the current state
        await switch.get_state()

        print("Relay state:", switch.relay)
        print("Firmware:", switch.firmware)
        print("MAC address:", switch.mac)

        print("Turn on the switch")
        await switch.turn_on()

        await switch.get_state()
        print("Relay state should be on:", switch.relay)

        print("Toggle the switch")
        await switch.toggle()

        await switch.get_state()
        print("Relay state should be off:", switch.relay)

        print("Toggle the switch")
        await switch.toggle()

        await switch.get_state()
        print("Relay state should be on:", switch.relay)

        await switch.turn_off()
        
        await switch.get_state()
        print("Relay state should be off:", switch.relay)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
