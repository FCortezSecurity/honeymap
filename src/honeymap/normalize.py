import json
from datetime import datetime, timezone

from .models import Event


class ParseError(ValueError):
    """A log line we couldn't understand."""


LOGTYPES = {
    4002: "ssh",
    3001: "http",
    2000: "ftp",
    6001: "telnet",
    8001: "mysql",
}


def service_for(logtype):
    return LOGTYPES.get(logtype, "other")


def parse_line(line):
    try:
        record = json.loads(line)
    except json.JSONDecodeError:
        raise ParseError("not valid JSON")

    logtype = record["logtype"]

    if 1000 <= logtype <= 1099:
        return None  # OpenCanary's own status message, not an attack

    ts = datetime.fromisoformat(record["utc_time"]).replace(tzinfo=timezone.utc)
    logdata = record["logdata"]

    return Event(
        ts=ts,
        src_ip=record["src_host"],
        src_port=record["src_port"],
        dst_port=record["dst_port"],
        service=service_for(logtype),
        username=logdata.get("USERNAME"),
        password=logdata.get("PASSWORD"),
    )