import os

import psycopg
from dotenv import load_dotenv

from .models import Event

load_dotenv()


def connect():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="honeymap",
        user="honeymap",
        password=os.environ["POSTGRES_PASSWORD"],
    )


INSERT_SQL = """
INSERT INTO events (ts, src_ip, src_port, dst_port, service, event_type, username, password)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING
"""


def insert_event(conn, event):
    """Insert one event. Returns 1 if it was new, 0 if it was already stored."""
    with conn.cursor() as cur:
        cur.execute(
            INSERT_SQL,
            (
                event.ts,
                event.src_ip,
                event.src_port,
                event.dst_port,
                event.service,
                event.event_type,
                event.username,
                event.password,
            ),
        )
        return cur.rowcount


def fetch_events(conn):
    """Read every stored event back out of the database, oldest first."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT ts, src_ip, src_port, dst_port, service, event_type, username, password "
            "FROM events ORDER BY ts"
        )
        rows = cur.fetchall()
    return [
        Event(
            ts=ts,
            src_ip=src_ip,
            src_port=src_port,
            dst_port=dst_port,
            service=service,
            event_type=event_type,
            username=username,
            password=password,
        )
        for ts, src_ip, src_port, dst_port, service, event_type, username, password in rows
    ]


ALERT_SQL = """
INSERT INTO alerts (rule, severity, src_ip, service, first_seen, last_seen, event_count)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING
"""


def insert_alert(conn, alert):
    """Store one alert. Returns 1 if it was new, 0 if it was already stored."""
    with conn.cursor() as cur:
        cur.execute(
            ALERT_SQL,
            (
                alert.rule,
                alert.severity,
                alert.src_ip,
                alert.service,
                alert.first_seen,
                alert.last_seen,
                alert.event_count,
            ),
        )
        return cur.rowcount