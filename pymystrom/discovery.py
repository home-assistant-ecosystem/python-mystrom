"""Support for discovering myStrom devices."""

import asyncio
import logging
from typing import List, Optional

from .device_types import DEVICE_MAPPING_NUMERIC

_LOGGER = logging.getLogger(__name__)


class DiscoveredDevice(object):
    """Representation of discovered device."""

    mac: str
    type: int
    is_child: bool
    mystrom_registered: bool
    mystrom_online: bool
    restarted: bool

    @staticmethod
    def create_from_announce_msg(raw_addr, announce_msg):
        """Create announce message."""
        _LOGGER.debug("Received announce message '%s' from %s ", announce_msg, raw_addr)
        if len(announce_msg) != 8:
            raise RuntimeError("Unexpected announcement, '%s'" % announce_msg)

        device = DiscoveredDevice(host=raw_addr[0], mac=announce_msg[0:6].hex(":"))
        device.type = announce_msg[6]

        if device.type == "102":
            device.hardware = DEVICE_MAPPING_NUMERIC[int(announce_msg[6])]
        else:
            device.hardware = "non_mystrom"
        status = announce_msg[7]

        # Parse status field
        device.is_child = status & 1 != 0
        device.mystrom_registered = status & 2 != 0
        device.mystrom_online = status & 4 != 0
        device.restarted = status & 8 != 0
        return device

    def __init__(self, host, mac):
        """Initialize the discovery."""
        self.host = host
        self.mac = mac


class DeviceRegistry(object):
    """Representation of the device registry."""

    def __init__(self):
        """Initialize the device registry."""
        self.devices_by_mac = {}

    def register(self, device):
        """Register a device."""
        self.devices_by_mac[device.mac] = device

    def devices(self):
        """Get all present devices."""
        return list(self.devices_by_mac.values())


class DiscoveryProtocol(asyncio.DatagramProtocol):
    """Representation of the discovery protocol."""

    def __init__(self, registry: DeviceRegistry):
        """ "Initialize the discovery protocol."""
        super().__init__()
        self.registry = registry

    def connection_made(self, transport):
        """Create an UDP listener."""
        _LOGGER.debug("Starting up UDP listener")
        self.transport = transport

    def datagram_received(self, data, addr):
        """Handle a datagram."""
        device = DiscoveredDevice.create_from_announce_msg(addr, data)
        self.registry.register(device)

    def connection_lost(self, exc: Optional[Exception]) -> None:
        """Stop if connection is lost."""
        _LOGGER.debug("Shutting down UDP listener")
        super().connection_lost(exc)


async def discover_devices(timeout: int = 7) -> List[DiscoveredDevice]:
    """Discover local myStrom devices.

    Some myStrom devices report their presence every ~5 seconds in an UDP
    broadcast to port 7979.
    """
    registry = DeviceRegistry()
    loop = asyncio.get_event_loop()
    (transport, protocol) = await loop.create_datagram_endpoint(
        lambda: DiscoveryProtocol(registry), local_addr=("0.0.0.0", 7979)
    )
    # Server runs in the background, meanwhile wait until timeout expires
    await asyncio.sleep(timeout)
    # Shutdown server
    transport.close()

    devices = registry.devices()
    for device in devices:
        _LOGGER.debug(
            "Discovered myStrom device %s (%s) (MAC addresse: %s)",
            device.host,
            device.type,
            device.mac,
        )
    return devices
