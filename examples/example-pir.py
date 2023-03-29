"""Example code for communicating with a myStrom PIR unit."""
import asyncio

from pymystrom.pir import MyStromPir

IP_ADDRESS = "192.168.1.225"


async def main():
    """Sample code to work with a myStrom PIR."""
    async with MyStromPir(IP_ADDRESS) as pir:
        # Get the PIR settings
        await pir.get_settings()
        print("Settings:", pir.settings)

        # Get the PIR settings
        await pir.get_pir()
        print("PIR settings:", pir.pir)

        # Collect the sensors
        await pir.get_sensors_state()
        print("Sensors:", pir.sensors)

        # Get the temperature data
        await pir.get_temperatures()
        print("Temperatures:", pir.temperature_raw)
        print("Temperature measured:", pir.temperature_measured)

        # Details of the light sensor
        await pir.get_light()
        print("Brightness:", pir.intensity)
        print("Day?:", pir.day)
        print("Raw light data:", pir.light_raw)

        # Get the action settings
        await pir.get_actions()
        print("Actions:", pir.actions)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
