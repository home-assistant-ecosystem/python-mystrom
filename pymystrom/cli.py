"""
Copyright (c) 2017-2018 Fabian Affolter <fabian@affolter-engineering.ch>

Licensed under MIT. All rights reserved.
"""
import requests
import click

from pymystrom.bulb import MyStromBulb

URI = 'api/v1/device'
TIMEOUT = 5


@click.group()
@click.version_option()
def main():
    """Simple command-line tool to get and set the values of a myStrom devices.

    This tool can set the targets of a myStrom button for the different
    available actions single, double, long and touch.
    """


@main.group('config')
def config():
    """Get and set the configuration of a myStrom device."""


@config.command('read')
@click.option('--ip', prompt="IP address of the device",
              help="IP address of the device.")
@click.option('--mac', prompt="MAC address of the device",
              help="MAC address of the device.")
def read_config(ip, mac):
    """Read the current configuration of a myStrom device."""
    click.echo("Read configuration from %s" % ip)
    request = requests.get(
        'http://{}/{}/{}/'.format(ip, URI, mac), timeout=TIMEOUT)
    print(request.json())


@main.group('button')
def button():
    """Get and set details of a myStrom button."""


@button.command('generic')
@click.option('--ip', prompt="IP address of the button",
              help="IP address of the button.")
@click.option('--mac', prompt="MAC address of the button",
              help="MAC address of the button.")
@click.option('--single', prompt="URL for a single tap", default="",
              help="URL for a single tap.")
@click.option('--double', prompt="URL for a double tap", default="",
              help="URL for a double tap.")
@click.option('--long', prompt="URL for a long tab", default="",
              help="URL for a long tab.")
@click.option('--touch', prompt="URL for a touch", default="",
              help="URL for a touch.")
def write_config(ip, mac, single, double, long, touch):
    """Write the current configuration of a myStrom button."""
    click.echo("Write configuration to device %s" % ip)
    data = {
        'single': single,
        'double': double,
        'long': long,
        'touch': touch,
    }
    request = requests.post(
        'http://{}/{}/{}/'.format(ip, URI, mac), data=data, timeout=TIMEOUT)

    if request.status_code == 200:
        click.echo("Configuration of %s set" % mac)


@button.command('home-assistant')
@click.option('--ip', prompt="IP address of the button",
              help="IP address of the button.")
@click.option('--mac', prompt="MAC address of the button",
              help="MAC address of the button.")
@click.option('--hass', prompt="IP address of the Home Assistant instance",
              help="IP address of Home Assistant instance to use.")
@click.option('--port', prompt="Port of Home Assistant instance",
              default="8123",
              help="Port where Home Assistant instance is listening.")
@click.option('--id', prompt="ID of the button", default="",
              help="ID of the myStrom button.")
def write_ha_config(ip, mac, hass, port, id):
    """Write the configuration for Home Assistant to a myStrom button."""
    click.echo("Write configuration for Home Assistant to device %s..." % ip)

    action = "get://{1}:{2}/api/mystrom?{0}={3}"
    data = {
        'single': action.format('single', hass, port, id),
        'double':  action.format('double', hass, port, id),
        'long':  action.format('long', hass, port, id),
        'touch':  action.format('touch', hass, port, id),
    }
    request = requests.post(
        'http://{}/{}/{}/'.format(ip, URI, mac), data=data, timeout=TIMEOUT)

    if request.status_code == 200:
        click.echo("Configuration for %s set" % ip)
        click.echo("After using the push pattern the first time then "
                   "the myStrom WiFi Button will show up as %s" % id)


@button.command('reset')
@click.option('--ip', prompt="IP address of the WiFi Button",
              help="P address of the WiFi Button.")
@click.option('--mac', prompt="MAC address of the button",
              help="MAC address of the Wifi Button.")
def reset_config(ip, mac):
    """Reset the current configuration of a myStrom WiFi Button."""
    click.echo("Reset configuration of button %s..." % ip)
    data = {
        'single': "",
        'double': "",
        'long': "",
        'touch': "",
    }
    request = requests.post(
        'http://{}/{}/{}/'.format(ip, URI, mac), data=data, timeout=TIMEOUT)

    if request.status_code == 200:
        click.echo("Reset configuration of %s" % mac)


@main.group('bulb')
def bulb():
    """Get and set details of a myStrom bulb."""


@bulb.command('on')
@click.option('--ip', prompt="IP address of the bulb",
              help="IP address of the bulb.")
@click.option('--mac', prompt="MAC address of the bulb",
              help="MAC address of the bulb.")
def on(ip, mac):
    """Switch the bulb on."""
    bulb = MyStromBulb(ip, mac)
    bulb.set_color_hex('000000FF')


@bulb.command('color')
@click.option('--ip', prompt="IP address of the bulb",
              help="IP address of the bulb.")
@click.option('--mac', prompt="MAC address of the bulb",
              help="MAC address of the bulb.")
@click.option('--hue', prompt="Set the hue of the bulb",
              help="Set the hue of the bulb.")
@click.option('--saturation', prompt="Set the saturation of the bulb",
              help="Set the saturation of the bulb.")
@click.option('--value', prompt="Set the value of the bulb",
              help="Set the value of the bulb.")
def color(ip, mac, hue, saturation, value):
    """Switch the bulb on with the given color."""
    bulb = MyStromBulb(ip, mac)
    bulb.set_color_hsv(hue, saturation, value)


@bulb.command('off')
@click.option('--ip', prompt="IP address of the bulb",
              help="IP address of the bulb.")
@click.option('--mac', prompt="MAC address of the bulb",
              help="MAC address of the bulb.")
def off(ip, mac):
    """Switch the bulb off."""
    bulb = MyStromBulb(ip, mac)
    bulb.set_off()


if __name__ == '__main__':
    main()
