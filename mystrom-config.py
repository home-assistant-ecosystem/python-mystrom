"""
Copyright (c) 2017 Fabian Affolter <fabian@affolter-engineering.ch>

Licensed under MIT. All rights reserved.
"""
import requests
import click

import pymystrom

URI = 'api/v1/device'
TIMEOUT = 5

@click.group()
@click.version_option()
def main():
    """Simple command-line tool to get and set the values of a myStrom devices.

    This tool can set the targets of a myStrom button for the different
    available actions single, double, long, and touch.
    """

@main.group('config')
def config():
    """Handler for all action around the configuration of a myStrom device."""

@config.command('read')
@click.option('--ip', prompt="IP address of the myStrom device",
              help="IP address of the myStrom device.")
@click.option('--mac', prompt="MAC address of the device",
              help="MAC address of the device.")
def read_config(ip, mac):
    """Read the current configuration of a myStrom device."""
    click.echo("Read configuration from %s" % ip)
    request = requests.get(
        'http://{}/{}/{}/'.format(ip, URI, mac), timeout=TIMEOUT)
    print(request.json())

@config.command('write')
@click.option('--ip', prompt="IP address of the myStrom button",
              help="P address of the myStrom button.")
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
    """Write the current configuration of a myStrom  button."""
    click.echo("Write configuration to device %s" % ip)
    data =  {
        'single': single,
        'double': double,
        'long': long,
        'touch': touch,
    }
    request = requests.post(
        'http://{}/{}/{}/'.format(ip, URI, mac), data=data, timeout=TIMEOUT)

    if request.status_code == 200:
        click.echo("Configuration of %s set", mac)

@config.command('reset')
@click.option('--ip', prompt="IP address of the myStrom button",
              help="P address of the myStrom button.")
@click.option('--mac', prompt="MAC address of the button",
              help="MAC address of the button.")
def reset_config(ip, mac):
    """Reset the current configuration of a myStrom button."""
    click.echo("Reset configuration of button %s" % ip)
    data =  {
        'single': "",
        'double': "",
        'long': "",
        'touch': "",
    }
    request = requests.post(
        'http://{}/{}/{}/'.format(ip, URI, mac), data=data, timeout=TIMEOUT)

    if request.status_code == 200:
        click.echo("Configuration of %s reset" % mac)

@main.group('bulb')
def bulb():
    """Handler for all action around the configuration of a myStrom bulb."""

@bulb.command('on')
@click.option('--ip', prompt="IP address of the myStrom bulb",
              help="IP address of the myStrom bulb.")
@click.option('--mac', prompt="MAC address of the bulb",
              help="MAC address of the bulb.")
def on(ip, mac):
    """Switch the bulb on."""
    bulb = pymystrom.MyStromBulb(ip, mac)
    bulb.set_color_hex('000000FF')

@bulb.command('off')
@click.option('--ip', prompt="IP address of the myStrom bulb",
              help="IP address of the myStrom bulb.")
@click.option('--mac', prompt="MAC address of the bulb",
              help="MAC address of the bulb.")
def off(ip, mac):
    """Switch the bulb off."""
    bulb = pymystrom.MyStromBulb(ip, mac)
    bulb.set_off()

if __name__ == '__main__':
    main()
