from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Event:
    ts: datetime
    src_ip: str
    src_port: int
    dst_port: int
    service: str
    event_type: str
    username: str | None = None
    password: str | None = None
    country: str | None = None
    city: str | None = None
    lat: float | None = None
    lon: float | None = None
    asn: int | None = None
    org: str | None = None
    source: str = "live"


@dataclass(frozen=True)
class Alert:
    rule: str
    severity: str
    src_ip: str
    service: str
    first_seen: datetime
    last_seen: datetime
    event_count: int
    source: str = "live"
    mitre_id: str | None = None