import os

import psycopg
from dotenv import load_dotenv

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