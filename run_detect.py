import sys

sys.path.insert(0, "src")

from honeymap.db import connect, fetch_events
from honeymap.detect import find_brute_force

with connect() as conn:
    events = fetch_events(conn)

print(f"loaded {len(events)} events")
for alert in find_brute_force(events):
    print(alert)