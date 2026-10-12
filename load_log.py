import sys

sys.path.insert(0, "src")

from honeymap.db import connect, insert_event
from honeymap.normalize import ParseError, parse_line

new_rows = 0
status_lines = 0
rejected = 0

with connect() as conn, open("data/logs/opencanary.log") as f:
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
        new_rows += insert_event(conn, event)

print(f"new_rows={new_rows} status_lines={status_lines} rejected={rejected}")