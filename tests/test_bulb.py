"""Tests for myStrom bulbs."""

import pytest

import pymystrom.bulb as bulb_module
from pymystrom.bulb import MyStromBulb


@pytest.mark.asyncio
async def test_set_on(monkeypatch):
    """Test MyStromBulb.set_on sends correct request and returns response."""
    mac = "AA:BB:CC:DD:EE:FF"
    called = {}

    async def _fake_request(
        self, uri, method="POST", data=None, json_data=None, params=None, token=None
    ):
        """Fake request function to capture call parameters."""
        called.update({"uri": uri, "method": method, "data": data, "token": token})
        return {"result": "ok"}

    monkeypatch.setattr(bulb_module, "request", _fake_request)
    bulb = MyStromBulb("127.0.0.1", mac)
    resp = await bulb.set_on()
    assert called["method"] == "POST"
    assert called["data"] == {"action": "on"}
    assert resp == {"result": "ok"}


@pytest.mark.asyncio
async def test_set_off(monkeypatch):
    """Test MyStromBulb.set_off sends correct request and returns response."""
    mac = "AA:BB:CC:DD:EE:FF"
    called = {}

    async def _fake_request(
        self, uri, method="POST", data=None, json_data=None, params=None, token=None
    ):
        """Fake request function to capture call parameters."""
        called.update({"uri": uri, "method": method, "data": data, "token": token})
        return {"result": "ok"}

    monkeypatch.setattr(bulb_module, "request", _fake_request)
    bulb = MyStromBulb("127.0.0.1", mac)
    resp = await bulb.set_off()
    assert called["method"] == "POST"
    assert called["data"] == {"action": "off"}
    assert resp == {"result": "ok"}


@pytest.mark.asyncio
async def test_set_color_hex(monkeypatch):
    """Test MyStromBulb.set_color_hex sends correct request and returns response."""
    mac = "AA:BB:CC:DD:EE:FF"
    called = {}

    async def _fake_request(
        self, uri, method="POST", data=None, json_data=None, params=None, token=None
    ):
        """Fake request function to capture call parameters."""
        called.update({"uri": uri, "method": method, "data": data, "token": token})
        return {"result": "ok"}

    monkeypatch.setattr(bulb_module, "request", _fake_request)
    bulb = MyStromBulb("127.0.0.1", mac)
    resp = await bulb.set_color_hex("FF000000")
    assert called["data"]["color"] == "FF000000"
    assert resp == {"result": "ok"}


@pytest.mark.asyncio
async def test_set_color_hsv(monkeypatch):
    """Test MyStromBulb.set_color_hsv sends correct request and returns response."""

    mac = "AA:BB:CC:DD:EE:FF"
    called = {}

    async def _fake_request(
        self, uri, method="POST", data=None, json_data=None, params=None, token=None
    ):
        """Fake request function to capture call parameters."""
        called.update({"uri": uri, "method": method, "data": data, "token": token})
        return {"result": "ok"}

    monkeypatch.setattr(bulb_module, "request", _fake_request)
    bulb = MyStromBulb("127.0.0.1", mac)
    resp = await bulb.set_color_hsv(1, 2, 3)
    assert "color=1;2;3" in called["data"]
    assert resp == {"result": "ok"}


@pytest.mark.asyncio
async def test_set_white(monkeypatch):
    """Test MyStromBulb.set_white sends correct request and returns response."""

    mac = "AA:BB:CC:DD:EE:FF"
    called = {"calls": []}

    async def _fake_request(
        self, uri, method="POST", data=None, json_data=None, params=None, token=None
    ):
        """Fake request function to capture call parameters."""
        called["calls"].append(data)
        return {"result": "ok"}

    monkeypatch.setattr(bulb_module, "request", _fake_request)
    bulb = MyStromBulb("127.0.0.1", mac)
    await bulb.set_white()
    # Should call set_color_hsv with (0, 0, 100)
    assert any("color=0;0;100" in str(d) for d in called["calls"])


@pytest.mark.asyncio
async def test_set_transition_time(monkeypatch):
    """Test MyStromBulb.set_transition_time sends correct request and returns response."""
    mac = "AA:BB:CC:DD:EE:FF"
    called = {}

    async def _fake_request(
        self, uri, method="POST", data=None, json_data=None, params=None, token=None
    ):
        """Fake request function to capture call parameters."""
        called.update({"uri": uri, "method": method, "data": data, "token": token})
        return {"result": "ok"}

    monkeypatch.setattr(bulb_module, "request", _fake_request)
    bulb = MyStromBulb("127.0.0.1", mac)
    resp = await bulb.set_transition_time(123)
    assert called["data"]["ramp"] == 123
    assert resp == {"result": "ok"}


@pytest.mark.asyncio
async def test_context_manager(monkeypatch):
    """Test MyStromBulb can be used as an async context manager."""
    mac = "AA:BB:CC:DD:EE:FF"
    closed = {"called": False}

    async def _fake_close(self):
        """Fake close function to capture call."""
        closed["called"] = True

    monkeypatch.setattr(MyStromBulb, "close", _fake_close)
    async with MyStromBulb("127.0.0.1", mac) as bulb:
        assert isinstance(bulb, MyStromBulb)
    # __aexit__ should call close
    assert closed["called"] is True


@pytest.mark.asyncio
async def test_get_state(monkeypatch):
    """Test MyStromBulb.get_state parses response correctly."""
    mac = "AA:BB:CC:DD:EE:FF"
    fake_response = {
        mac: {
            "power": 5.5,
            "fw_version": "1.2.3",
            "color": "FF000000",
            "mode": "white",
            "ramp": 42,
            "on": 1,
            "type": "RGB",
        }
    }

    async def _fake_request(
        self, uri, method="GET", data=None, json_data=None, params=None, token=None
    ):
        """Fake request function to return predefined response."""
        return fake_response

    monkeypatch.setattr(bulb_module, "request", _fake_request)
    bulb = MyStromBulb("127.0.0.1", mac)
    await bulb.get_state()
    assert bulb.mac == mac
    assert bulb.firmware == "1.2.3"
    assert bulb.color == "FF000000"
    assert bulb.mode == "white"
    assert bulb.transition_time == 42
    assert bulb.state is True
    assert bulb.bulb_type == "RGB"
    assert bulb.consumption == 5.5
