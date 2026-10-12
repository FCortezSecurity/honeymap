import pytest

from honeymap.enrich import is_public


@pytest.mark.parametrize("ip", ["172.18.0.1", "10.0.0.5", "192.168.1.253", "127.0.0.1"])
def test_private_addresses_are_not_public(ip):
    assert is_public(ip) is False


def test_public_address_is_public():
    assert is_public("8.8.8.8") is True


def test_garbage_is_not_public():
    assert is_public("not-an-ip") is False