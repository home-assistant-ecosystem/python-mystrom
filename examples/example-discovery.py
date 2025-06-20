import asyncio

from pymystrom import discovery


async def main():
    """Sample code to work with discovery."""
    # Discover all bulbs in the network via broadcast datagram (UDP)
    bulbs = await discovery.discover_devices()
    print(f"Number of detected bulbs: {len(bulbs)}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
