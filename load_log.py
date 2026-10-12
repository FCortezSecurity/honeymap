import sys
from dataclasses import replace

sys.path.insert(0, "src")

from honeymap.db import connect, insert_event
from honeymap.enrich import GeoLookup, enrich_event
from honeymap.normalize import ParseError, parse_line

path = sys.argv[1] if len(sys.argv) > 1 else "data/logs/opencanary.log"
source = sys.argv[2] if len(sys.argv) > 2 else "live"
if source not in ("live", "demo"):
    sys.exit(f"source must be 'live' or 'demo', not {source!r}")

geo = GeoLookup("data/geoip/dbip-city-lite.mmdb", "data/geoip/dbip-asn-lite.mmdb")

new_rows = 0
located = 0
status_lines = 0
rejected = 0

with connect() as conn, open(path) as f:
    for number, line in enumerate(f, start=1):
        try:
            event = parse_line(line)
        except ParseError as error:
            rejected += 1
            print(f"line {number} rejected: {error}")
            continue
        if event is None:
            status_lines += 1
            continue
        event = replace(enrich_event(event, geo.lookup), source=source)
        if event.lat is not None:
            located += 1
        new_rows += insert_event(conn, event)

print(
    f"{path} [{source}]: new_rows={new_rows} located={located} "
    f"status_lines={status_lines} rejected={rejected}"
)