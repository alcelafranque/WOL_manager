import asyncio

from wol_bot import network


def test_wake_sends_to_configured_address(monkeypatch):
    calls = []
    monkeypatch.setattr(network.wakeonlan, "wake", lambda *a, **kw: calls.append((a, kw)))
    network.wake("aa:bb:cc:dd:ee:ff", "192.168.1.255", 7)
    assert calls == [(("aa:bb:cc:dd:ee:ff",), {"host": "192.168.1.255", "port": 7})]


def test_is_up_when_ping_answers(monkeypatch):
    calls = []

    async def fake_run(*args, timeout):
        calls.append(args[0])
        return 0, ""

    monkeypatch.setattr(network, "_run", fake_run)
    assert asyncio.run(network.is_up("192.168.1.20")) is True
    assert calls == ["ping"]


def test_is_up_falls_back_to_neighbour_table(monkeypatch):
    outputs = {"ping": (1, ""), "ip": (0, "192.168.1.20 dev eth0 lladdr aa:bb:cc:dd:ee:ff REACHABLE\n")}

    async def fake_run(*args, timeout):
        return outputs[args[0]]

    monkeypatch.setattr(network, "_run", fake_run)
    assert asyncio.run(network.is_up("192.168.1.20")) is True

    outputs["ip"] = (0, "192.168.1.20 dev eth0 lladdr aa:bb:cc:dd:ee:ff STALE\n")
    assert asyncio.run(network.is_up("192.168.1.20")) is False


def test_run_kills_on_timeout():
    code, output = asyncio.run(network._run("sleep", "5", timeout=0.2))
    assert (code, output) == (-1, "")
