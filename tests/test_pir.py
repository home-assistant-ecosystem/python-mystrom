"""Tests for myStrom PIR sensors."""

import pytest

import pymystrom.pir as pir_module
from pymystrom.pir import MyStromPir


@pytest.mark.asyncio
async def test_get_settings(monkeypatch):
    """Test MyStromPir.get_settings sends correct request and updates settings."""
    fake_response = {"foo": "bar"}

    async def _fake_request(
        self, uri, method="GET", data=None, json_data=None, params=None, token=None
    ):
        """Fake request function to return predefined response."""
        return fake_response

    monkeypatch.setattr(pir_module, "request", _fake_request)
    pir = MyStromPir("127.0.0.1")
    await pir.get_settings()
    assert pir.settings == fake_response


@pytest.mark.asyncio
async def test_get_actions(monkeypatch):
    """Test MyStromPir.get_actions sends correct request and updates actions."""
    fake_response = {"action": "test"}

    async def _fake_request(
        self, uri, method="GET", data=None, json_data=None, params=None, token=None
    ):
        """Fake request function to return predefined response."""
        return fake_response

    monkeypatch.setattr(pir_module, "request", _fake_request)
    pir = MyStromPir("127.0.0.1")
    await pir.get_actions()
    assert pir.actions == fake_response


@pytest.mark.asyncio
async def test_get_pir(monkeypatch):
    """Test MyStromPir.get_pir sends correct request and updates pir settings."""
    fake_response = {"pir": 1}

    async def _fake_request(
        self, uri, method="GET", data=None, json_data=None, params=None, token=None
    ):
        """Fake request function to return predefined response."""

        return fake_response

    monkeypatch.setattr(pir_module, "request", _fake_request)
    pir = MyStromPir("127.0.0.1")
    await pir.get_pir()
    assert pir.pir == fake_response


@pytest.mark.asyncio
async def test_get_sensors_state(monkeypatch):
    """Test MyStromPir.get_sensors_state sends correct request and updates sensor values."""
    fake_response = {"motion": True, "light": 42, "temperature": 21.2345}

    async def _fake_request(
        self, uri, method="GET", data=None, json_data=None, params=None, token=None
    ):
        """Fake request function to return predefined response."""
        return fake_response

    monkeypatch.setattr(pir_module, "request", _fake_request)
    pir = MyStromPir("127.0.0.1")
    await pir.get_sensors_state()
    assert pir.sensors == {"motion": True, "light": 42, "temperature": 21.23}


@pytest.mark.asyncio
async def test_get_temperatures(monkeypatch):
    """Test MyStromPir.get_temperatures sends correct request and updates temperature values."""
    fake_response = {"measured": 22.345, "compensated": 23.456, "compensation": 0.12345}

    async def _fake_request(
        self, uri, method="GET", data=None, json_data=None, params=None, token=None
    ):
        """Fake request function to return predefined response."""
        return fake_response

    monkeypatch.setattr(pir_module, "request", _fake_request)
    pir = MyStromPir("127.0.0.1")
    await pir.get_temperatures()
    assert pir._temperature_raw == fake_response
    assert pir.temperature_measured == 22.34
    assert pir._temperature_compensated == 23.46
    assert pir._temperature_compensation == 0.123


@pytest.mark.asyncio
async def test_get_motion(monkeypatch):
    """Test MyStromPir.get_motion sends correct request and updates motion state."""
    fake_response = {"motion": 1}

    async def _fake_request(
        self, uri, method="GET", data=None, json_data=None, params=None, token=None
    ):
        """Fake request function to return predefined response."""

        return fake_response

    monkeypatch.setattr(pir_module, "request", _fake_request)
    pir = MyStromPir("127.0.0.1")
    await pir.get_motion()
    assert pir._motion == 1


@pytest.mark.asyncio
async def test_get_light(monkeypatch):
    """Test MyStromPir.get_light sends correct request and updates light sensor values."""
    fake_response = {"intensity": 99, "day": True, "raw": 123}

    async def _fake_request(
        self, uri, method="GET", data=None, json_data=None, params=None, token=None
    ):
        """Fake request function to return predefined response."""
        return fake_response

    monkeypatch.setattr(pir_module, "request", _fake_request)
    pir = MyStromPir("127.0.0.1")
    await pir.get_light()
    assert pir._intensity == 99
    assert pir._day is True
    assert pir._light_raw == 123
