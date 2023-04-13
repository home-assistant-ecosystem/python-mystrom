"""Example code for communicating with a myStrom plug/switch."""
import asyncio

from pymystrom import get_device_info, MyStromDeviceType

IP_ADDRESS = "192.168.1.62"


async def main():
    """Sample code to work with a myStrom switch."""
    info = await get_device_info(IP_ADDRESS)
    # Collect the data of the current state
    print(info)
    if info["type"] == MyStromDeviceType.SWITCH_CH_V2:
        print("found switch v2")



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
