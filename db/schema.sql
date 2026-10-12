CREATE TABLE IF NOT EXISTS events (
    id          BIGSERIAL PRIMARY KEY,
    ts          TIMESTAMPTZ NOT NULL,
    src_ip      TEXT NOT NULL,
    src_port    INTEGER NOT NULL,
    dst_port    INTEGER NOT NULL,
    service     TEXT NOT NULL,
    event_type  TEXT NOT NULL,
    username    TEXT,
    password    TEXT,
    country     TEXT,
    city        TEXT,
    lat         DOUBLE PRECISION,
    lon         DOUBLE PRECISION,
    asn         INTEGER,
    org         TEXT,
    UNIQUE (ts, src_ip, src_port, dst_port, event_type)
);

CREATE INDEX IF NOT EXISTS idx_events_ts ON events (ts DESC);