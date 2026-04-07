"""Tests for myStrom Switch devices."""

import pytest

import pymystrom.switch as switch_module
from pymystrom.switch import MyStromSwitch


@pytest.mark.asyncio
async def test_turn_on(monkeypatch):
    """Test MyStromSwitch.turn_on sends correct request and updates state."""
    called = {}

    async def _fake_request(
        self, uri, method="GET", data=None, json_data=None, params=None, token=None
    ):
        """Fake request function to capture call parameters."""
        called["uri"] = str(uri)
        called["params"] = params
        return {"relay": True, "power": 1.0, "Ws": 0.5}

    monkeypatch.setattr(switch_module, "request", _fake_request)
    sw = MyStromSwitch("127.0.0.1")

    # Patch get_state to avoid recursion
    async def fake_get_state():
        sw._state = True

    sw.get_state = fake_get_state
    await sw.turn_on()
    assert called["params"] == {"state": "1"}


@pytest.mark.asyncio
async def test_turn_off(monkeypatch):
    """Test MyStromSwitch.turn_off sends correct request and updates state."""
    called = {}

    async def _fake_request(
        self, uri, method="GET", data=None, json_data=None, params=None, token=None
    ):
        """Fake request function to capture call parameters."""
        called["uri"] = str(uri)
        called["params"] = params
        return {"relay": False, "power": 0.0, "Ws": 0.0}

    monkeypatch.setattr(switch_module, "request", _fake_request)
    sw = MyStromSwitch("127.0.0.1")

    async def fake_get_state():
        """Fake get_state to set initial state."""
        sw._state = False

    sw.get_state = fake_get_state
    await sw.turn_off()
    assert called["params"] == {"state": "0"}


@pytest.mark.asyncio
async def test_toggle(monkeypatch):
    """Test MyStromSwitch.toggle sends correct request based on current state."""
    called = {}

    async def _fake_request(
        self, uri, method="GET", data=None, json_data=None, params=None, token=None
    ):
        """Fake request function to capture call parameters."""
        called["uri"] = str(uri)
        return {"relay": True, "power": 1.0, "Ws": 0.5}

    monkeypatch.setattr(switch_module, "request", _fake_request)
    sw = MyStromSwitch("127.0.0.1")

    async def fake_get_state():
        """Fake get_state to set initial state."""
        sw._state = True

    sw.get_state = fake_get_state
    await sw.toggle()
    assert "toggle" in called["uri"]


@pytest.mark.asyncio
async def test_get_state(monkeypatch):
    """Test MyStromSwitch.get_state sends correct request and updates state."""
    mac = "AA:BB:CC:DD:EE:FF"
    fake_report = {"relay": True, "power": 1.23, "Ws": 0.5}
    fake_info = {"version": "2.68.10", "mac": mac, "type": "SWITCH"}
    responses = [fake_report, fake_info]

    async def _fake_request(
        self, uri, method="GET", data=None, json_data=None, params=None, token=None
    ):
        """Fake request function to return predefined responses in sequence."""
        return responses.pop(0)

    monkeypatch.setattr(switch_module, "request", _fake_request)
    sw = MyStromSwitch("127.0.0.1")
    await sw.get_state()
    assert sw.relay is True
    assert sw.consumption == 1.2
    assert sw.consumedWs == 0.5
    assert sw.firmware == "2.68.10"
    assert sw.mac == mac
    assert (
        sw.device_type is None
    )  # Because DEVICE_MAPPING_LITERAL.get("SWITCH") is None by default
