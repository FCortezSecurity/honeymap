from dataclasses import replace
from datetime import datetime, timedelta, timezone

from honeymap.detect import find_brute_force, find_multi_service
from honeymap.models import Event

START = datetime(2026, 10, 12, 12, 0, 0, tzinfo=timezone.utc)


def make_attempts(count, seconds_apart, ip="45.1.2.3"):
    """Build a list of fake login attempts, evenly spaced in time."""
    return [
        Event(
            ts=START + timedelta(seconds=i * seconds_apart),
            src_ip=ip,
            src_port=40000 + i,
            dst_port=2222,
            service="ssh",
            event_type="login_attempt",
            username="root",
        )
        for i in range(count)
    ]


def make_probes(services, seconds_apart, ip="45.1.2.3"):
    """One connection per service name, evenly spaced in time."""
    return [
        Event(
            ts=START + timedelta(seconds=i * seconds_apart),
            src_ip=ip,
            src_port=40000 + i,
            dst_port=1000 + i,
            service=service,
            event_type="connection",
        )
        for i, service in enumerate(services)
    ]


def test_fast_burst_raises_one_alert():
    alerts = find_brute_force(make_attempts(20, seconds_apart=1))
    assert len(alerts) == 1
    assert alerts[0].src_ip == "45.1.2.3"
    assert alerts[0].event_count == 20


def test_slow_attempts_raise_no_alert():
    alerts = find_brute_force(make_attempts(20, seconds_apart=600))
    assert alerts == []


def test_alert_inherits_source_from_events():
    attempts = [replace(e, source="demo") for e in make_attempts(20, seconds_apart=1)]
    alerts = find_brute_force(attempts)
    assert alerts[0].source == "demo"


def test_alert_defaults_to_live():
    alerts = find_brute_force(make_attempts(20, seconds_apart=1))
    assert alerts[0].source == "live"


def test_three_services_quickly_raises_alert():
    alerts = find_multi_service(make_probes(["ssh", "http", "ftp"], seconds_apart=10))
    assert len(alerts) == 1
    assert alerts[0].rule == "multi_service_targeting"
    assert alerts[0].service == "multiple"


def test_one_service_repeated_is_not_a_sweep():
    alerts = find_multi_service(make_probes(["ssh"] * 10, seconds_apart=10))
    assert alerts == []


def test_slow_sweep_raises_no_alert():
    alerts = find_multi_service(make_probes(["ssh", "http", "ftp"], seconds_apart=3600))
    assert alerts == []