import json
from datetime import datetime, timezone

from .models import Event


class ParseError(ValueError):
    """A log line we couldn't understand."""


# logtype -> (service, event_type)
LOGTYPES = {
    4002: ("ssh", "login_attempt"),
    3000: ("http", "request"),
    3001: ("http", "login_attempt"),
    2000: ("ftp", "login_attempt"),
    6001: ("telnet", "login_attempt"),
    8001: ("mysql", "login_attempt"),
}


def classify(logtype):
    return LOGTYPES.get(logtype, ("other", "other"))


def parse_line(line):
    try:
        record = json.loads(line)
    except json.JSONDecodeError:
        raise ParseError("not valid JSON")

    try:
        logtype = record["logtype"]

        if 1000 <= logtype <= 1099:
            return None  # OpenCanary's own status message, not an attack

        ts = datetime.fromisoformat(record["utc_time"]).replace(tzinfo=timezone.utc)
        logdata = record["logdata"]
        service, event_type = classify(logtype)

        return Event(
            ts=ts,
            src_ip=record["src_host"],
            src_port=record["src_port"],
            dst_port=record["dst_port"],
            service=service,
            event_type=event_type,
            username=logdata.get("USERNAME"),
            password=logdata.get("PASSWORD"),
        )
    except (KeyError, TypeError, ValueError) as error:
        raise ParseError(f"bad record: {error!r}")