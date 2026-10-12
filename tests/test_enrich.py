from datetime import datetime, timezone

import pytest

from honeymap.enrich import enrich_event, is_public
from honeymap.models import Event


def make_event(ip):
    return Event(
        ts=datetime(2026, 10, 12, tzinfo=timezone.utc),
        src_ip=ip,
        src_port=40000,
        dst_port=2222,
        service="ssh",
        event_type="login_attempt",
        username="root",
    )


def fake_lookup(ip):
    return {"country": "Testland", "city": "Testville", "lat": 1.5, "lon": 2.5,
            "asn": 64500, "org": "Test Net"}


@pytest.mark.parametrize("ip", ["172.18.0.1", "10.0.0.5", "192.168.1.253", "127.0.0.1"])
def test_private_addresses_are_not_public(ip):
    assert is_public(ip) is False


def test_public_address_is_public():
    assert is_public("8.8.8.8") is True


def test_garbage_is_not_public():
    assert is_public("not-an-ip") is False


def test_public_ip_gets_location():
    event = enrich_event(make_event("8.8.8.8"), fake_lookup)
    assert event.country == "Testland"
    assert event.lat == 1.5
    assert event.asn == 64500


def test_private_ip_never_calls_lookup():
    def explode(ip):
        raise AssertionError("lookup must not be called for private IPs")

    event = enrich_event(make_event("172.18.0.1"), explode)
    assert event.country is None
    assert event.lat is None