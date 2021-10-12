"""Example code for getting myStrom device info."""
import asyncio

from pymystrom.discovery import get_device_info

IP_ADDRESS = "192.168.0.51"


async def main():
    """Sample code to work with a the get_device_info request."""
    
    # Collect the data 
    info = await get_device_info("192.168.50.6")
        
    # Print all attributes
    print(info.__dict__)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
