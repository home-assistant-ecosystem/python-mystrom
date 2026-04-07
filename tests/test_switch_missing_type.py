"""Test handling of missing 'type' field in device info."""

import pytest

import pymystrom.switch as switch_module
from pymystrom.switch import MyStromSwitch


@pytest.mark.asyncio
async def test_get_state_missing_type(monkeypatch):
    async def _fake_request(
        self, uri, method="GET", data=None, json_data=None, params=None, token=None
    ):
        uri_str = str(uri)
        if uri_str.endswith("/report"):
            return {"relay": True, "power": 1.23, "Ws": 0.5}
        if uri_str.endswith("/api/v1/info"):
            # Legacy v1 firmware without 'type'
            return {"version": "2.68.10", "mac": "AA:BB:CC:DD:EE:FF"}
        if uri_str.endswith("/info.json"):
            return {"version": "2.68.10", "mac": "AA:BB:CC:DD:EE:FF"}
        return {}

    monkeypatch.setattr(switch_module, "request", _fake_request)
    sw = MyStromSwitch("127.0.0.1")
    await sw.get_state()

    assert sw.relay is True
    assert sw.consumption == 1.2
    assert sw.consumedWs == 0.5
    assert sw.firmware == "2.68.10"
    assert sw.mac == "AA:BB:CC:DD:EE:FF"
    # Missing 'type' should be tolerated and map to None
    assert sw.device_type is None
