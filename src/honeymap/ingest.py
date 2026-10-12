import argparse
import os
import time
from dataclasses import replace

from .db import connect, fetch_events, insert_alert, insert_event
from .detect import find_brute_force, find_multi_service
from .enrich import GeoLookup, enrich_event
from .normalize import ParseError, parse_line

CITY_DB = os.environ.get("GEOIP_CITY_DB", "data/geoip/dbip-city-lite.mmdb")
ASN_DB = os.environ.get("GEOIP_ASN_DB", "data/geoip/dbip-asn-lite.mmdb")


def ingest_file(conn, path, lookup, source, offset=0):
    """Read lines added to `path` since byte `offset`. Returns (stats, new_offset)."""
    stats = {"new": 0, "located": 0, "skipped": 0, "rejected": 0}

    if os.path.getsize(path) < offset:
        offset = 0  # the file was rotated or replaced: start over

    with open(path, "rb") as f:
        f.seek(offset)
        for raw in f:
            if not raw.endswith(b"\n"):
                break  # a half-written line: leave it for the next round
            offset += len(raw)
            line = raw.decode("utf-8", errors="replace")

            try:
                event = parse_line(line)
            except ParseError as error:
                stats["rejected"] += 1
                print(f"rejected ({error}): {line[:60]!r}")
                continue
            if event is None:
                stats["skipped"] += 1
                continue

            event = replace(enrich_event(event, lookup), source=source)
            if event.lat is not None:
                stats["located"] += 1
            stats["new"] += insert_event(conn, event)

    conn.commit()
    return stats, offset


def detect_and_store(conn):
    """Run every detection rule over stored events and save new alerts."""
    events = fetch_events(conn)
    alerts = find_brute_force(events) + find_multi_service(events)
    new_alerts = sum(insert_alert(conn, alert) for alert in alerts)
    conn.commit()
    return len(events), len(alerts), new_alerts


def main():
    parser = argparse.ArgumentParser(description="Ingest honeypot logs and run detection.")
    parser.add_argument("path", nargs="?", default="data/logs/opencanary.log")
    parser.add_argument("--source", choices=["live", "demo"], default="live")
    parser.add_argument("--follow", action="store_true", help="keep watching the file")
    parser.add_argument("--interval", type=int, default=5, help="seconds between checks")
    args = parser.parse_args()

    lookup = GeoLookup(CITY_DB, ASN_DB).lookup
    offset = 0

    with connect() as conn:
        try:
            while True:
                stats, offset = ingest_file(conn, args.path, lookup, args.source, offset)
                total, found, new_alerts = detect_and_store(conn)
                print(
                    f"[{args.source}] new_events={stats['new']} located={stats['located']} "
                    f"skipped={stats['skipped']} rejected={stats['rejected']} | "
                    f"events_total={total} alerts_found={found} alerts_new={new_alerts}"
                )
                if not args.follow:
                    break
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("stopped")