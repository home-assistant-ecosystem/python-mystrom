"""Example code for communicating with a myStrom plug/switch."""
import asyncio

from pymystrom.switch import MyStromSwitch

IP_ADDRESS = "192.168.0.40"


async def main():
    """Sample code to work with a myStrom switch."""
    async with MyStromSwitch(IP_ADDRESS) as switch:
        # Collect the data of the current state
        await switch.get_state()

        print("Power consumption:", switch.consumption)
        print("Energy consumed:", switch.consumedWs)
        print("Relay state:", switch.relay)
        print("Temperature:", switch.temperature)
        print("Firmware:", switch.firmware)
        print("MAC address:", switch.mac)

        print("Turn on the switch")
        if not switch.relay:
            await switch.turn_on()

        # print("Toggle the switch")
        # await switch.toggle()

        # Switch relay off if it was off
        if switch.relay:
            await switch.turn_off()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
