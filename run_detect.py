import sys

sys.path.insert(0, "src")

from honeymap.db import connect, fetch_events, insert_alert
from honeymap.detect import find_brute_force, find_multi_service

with connect() as conn:
    events = fetch_events(conn)
    alerts = find_brute_force(events) + find_multi_service(events)
    new_alerts = sum(insert_alert(conn, alert) for alert in alerts)

print(f"loaded {len(events)} events, found {len(alerts)} alerts, stored {new_alerts} new")