"""Command-line tool for working with myStrom devices."""

import click
import requests
import asyncio

from functools import wraps

from pymystrom.bulb import MyStromBulb

URI = "api/v1/device"
TIMEOUT = 5


def coro(f):
    """Allow to use async in click."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        """Async wrapper."""
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.group()
@click.version_option()
def main():
    """Simple command-line tool to get and set the values of myStrom devices.

    This tool can also set the targets of a myStrom button for the different
    available actions single, double, long and touch.
    """


@main.group("config")
def config():
    """Get and set the configuration of a myStrom device."""


@config.command("read")
@click.option(
    "--ip", prompt="IP address of the device", help="IP address of the device."
)
@click.option(
    "--mac",
    prompt="MAC address of the device",
    help="MAC address of the device.",
)
@click.option("--token", prompt="Token of the device", help="Token of the device.")
def read_config(ip, mac, token):
    """Read the current configuration of a myStrom device."""
    click.echo("Read configuration from %s" % ip)
    try:
        headers = {"Token": token} if token else {}
        request = requests.get(
            "http://{}/{}/{}/".format(ip, URI, mac), timeout=TIMEOUT, headers=headers
        )
        click.echo(request.json())
    except requests.exceptions.ConnectionError:
        click.echo("Communication issue with the device")


@main.group("button")
def button():
    """Get and set details of a myStrom button."""


@button.command("generic")
@click.option(
    "--ip", prompt="IP address of the button", help="IP address of the button."
)
@click.option(
    "--mac",
    prompt="MAC address of the button",
    help="MAC address of the button.",
)
@click.option("--token", prompt="Token of the device", help="Token of the device.")
@click.option(
    "--single",
    prompt="URL for a single tap",
    default="",
    help="URL for a single tap.",
)
@click.option(
    "--double",
    prompt="URL for a double tap",
    default="",
    help="URL for a double tap.",
)
@click.option(
    "--long", prompt="URL for a long tab", default="", help="URL for a long tab."
)
@click.option("--touch", prompt="URL for a touch", default="", help="URL for a touch.")
def write_config(ip, mac, token, single, double, long, touch):
    """Write the current configuration of a myStrom button."""
    click.echo("Write configuration to device %s" % ip)
    data = {
        "single": single,
        "double": double,
        "long": long,
        "touch": touch,
    }
    try:
        headers = {"Token": token} if token else {}
        request = requests.post(
            "http://{}/{}/{}/".format(ip, URI, mac),
            data=data,
            timeout=TIMEOUT,
            headers=headers,
        )

        if request.status_code == 200:
            click.echo("Configuration of %s set" % mac)
    except requests.exceptions.ConnectionError:
        click.echo("Communication issue with the device. No action performed")


@button.command("home-assistant")
@click.option(
    "--ip", prompt="IP address of the button", help="IP address of the button."
)
@click.option(
    "--mac",
    prompt="MAC address of the button",
    help="MAC address of the button.",
)
@click.option("--token", prompt="Token of the device", help="Token of the device.")
@click.option(
    "--hass",
    prompt="IP address of the Home Assistant instance",
    help="IP address of Home Assistant instance to use.",
)
@click.option(
    "--port",
    prompt="Port of Home Assistant instance",
    default="8123",
    help="Port where Home Assistant instance is listening.",
)
@click.option(
    "--id",
    prompt="ID of the button",
    default="",
    help="ID of the myStrom button.",
)
def write_ha_config(ip, mac, token, hass, port, id):
    """Write the configuration for Home Assistant to a myStrom button."""
    click.echo("Write configuration for Home Assistant to device %s..." % ip)

    action = "get://{1}:{2}/api/mystrom?{0}={3}"
    data = {
        "single": action.format("single", hass, port, id),
        "double": action.format("double", hass, port, id),
        "long": action.format("long", hass, port, id),
        "touch": action.format("touch", hass, port, id),
    }
    try:
        headers = {"Token": token} if token else {}
        request = requests.post(
            "http://{}/{}/{}/".format(ip, URI, mac),
            data=data,
            timeout=TIMEOUT,
            headers=headers,
        )

        if request.status_code == 200:
            click.echo("Configuration for %s set" % ip)
            click.echo(
                "After using the push pattern the first time then "
                "the myStrom WiFi Button will show up as %s" % id
            )
    except requests.exceptions.ConnectionError:
        click.echo("Communication issue with the device")


@button.command("reset")
@click.option(
    "--ip",
    prompt="IP address of the WiFi Button",
    help="P address of the WiFi Button.",
)
@click.option(
    "--mac",
    prompt="MAC address of the button",
    help="MAC address of the Wifi Button.",
)
@click.option("--token", prompt="Token of the device", help="Token of the device.")
def reset_config(ip, mac, token):
    """Reset the current configuration of a myStrom WiFi Button."""
    click.echo("Reset configuration of button %s..." % ip)
    data = {
        "single": "",
        "double": "",
        "long": "",
        "touch": "",
    }
    try:
        headers = {"Token": token} if token else {}
        request = requests.post(
            "http://{}/{}/{}/".format(ip, URI, mac),
            data=data,
            timeout=TIMEOUT,
            headers=headers,
        )

        if request.status_code == 200:
            click.echo("Reset configuration of %s" % mac)
    except requests.exceptions.ConnectionError:
        click.echo("Communication issue with the device. No action performed")


@button.command("read")
@click.option(
    "--ip",
    prompt="IP address of the WiFi Button",
    help="P address of the WiFi Button.",
)
@click.option(
    "--mac",
    prompt="MAC address of the button",
    help="MAC address of the Wifi Button.",
)
@click.option("--token", prompt="Token of the device", help="Token of the device.")
def read_config(ip, mac, token):
    """Read the current configuration of a myStrom WiFi Button."""
    click.echo("Read the configuration of button %s..." % ip)
    try:
        headers = {"Token": token} if token else {}
        request = requests.get(
            "http://{}/{}/{}/".format(ip, URI, mac), timeout=TIMEOUT, headers=headers
        )
        click.echo(request.json())
    except requests.exceptions.ConnectionError:
        click.echo("Communication issue with the device. No action performed")


@main.group("bulb")
def bulb():
    """Get and set details of a myStrom bulb."""


@bulb.command("on")
@coro
@click.option("--ip", prompt="IP address of the bulb", help="IP address of the bulb.")
@click.option(
    "--mac", prompt="MAC address of the bulb", help="MAC address of the bulb."
)
@click.option("--token", prompt="Token of the device", help="Token of the device.")
async def on(ip, mac, token):
    """Switch the bulb on."""
    async with MyStromBulb(ip=ip, mac=mac, token=token) as bulb:
        await bulb.set_color_hex("00FFFFFF")


@bulb.command("color")
@coro
@click.option("--ip", prompt="IP address of the bulb", help="IP address of the bulb.")
@click.option(
    "--mac", prompt="MAC address of the bulb", help="MAC address of the bulb."
)
@click.option("--token", prompt="Token of the device", help="Token of the device.")
@click.option(
    "--hue", prompt="Set the hue of the bulb", help="Set the hue of the bulb."
)
@click.option(
    "--saturation",
    prompt="Set the saturation of the bulb",
    help="Set the saturation of the bulb.",
)
@click.option(
    "--value",
    prompt="Set the value of the bulb",
    help="Set the value of the bulb.",
)
async def color(ip, mac, token, hue, saturation, value):
    """Switch the bulb on with the given color."""
    async with MyStromBulb(ip=ip, mac=mac, token=token) as bulb:
        await bulb.set_color_hsv(hue, saturation, value)


@bulb.command("off")
@coro
@click.option("--ip", prompt="IP address of the bulb", help="IP address of the bulb.")
@click.option(
    "--mac", prompt="MAC address of the bulb", help="MAC address of the bulb."
)
@click.option("--token", prompt="Token of the device", help="Token of the device.")
async def off(ip, mac, token):
    """Switch the bulb off."""
    async with MyStromBulb(ip=ip, mac=mac, token=token) as bulb:
        await bulb.set_off()


@bulb.command("flash")
@coro
@click.option("--ip", prompt="IP address of the bulb", help="IP address of the bulb.")
@click.option(
    "--mac", prompt="MAC address of the bulb", help="MAC address of the bulb."
)
@click.option("--token", prompt="Token of the device", help="Token of the device.")
@click.option(
    "--time",
    prompt="Time to flash",
    help="Time to flash the bulb in seconds.",
    default=10,
)
async def flash(ip, mac, token, time):
    """Flash the bulb off."""
    async with MyStromBulb(ip=ip, mac=mac, token=token) as bulb:
        await bulb.set_flashing(time, [100, 50, 30], [200, 0, 71])


@bulb.command("rainbow")
@coro
@click.option("--ip", prompt="IP address of the bulb", help="IP address of the bulb.")
@click.option(
    "--mac", prompt="MAC address of the bulb", help="MAC address of the bulb."
)
@click.option("--token", prompt="Token of the device", help="Token of the device.")
@click.option(
    "--time",
    prompt="Time for the complete rainbow",
    help="Time to perform the rainbow in seconds.",
    default=30,
)
async def rainbow(ip, mac, token, time):
    """Let the buld change the color and show a rainbow."""
    async with MyStromBulb(ip=ip, mac=mac, token=token) as bulb:
        await bulb.set_rainbow(time)
        await bulb.set_transition_time(1000)


if __name__ == "__main__":
    main()
