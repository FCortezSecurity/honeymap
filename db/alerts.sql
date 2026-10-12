CREATE TABLE IF NOT EXISTS alerts (
    id          BIGSERIAL PRIMARY KEY,
    rule        TEXT NOT NULL,
    severity    TEXT NOT NULL,
    src_ip      TEXT NOT NULL,
    service     TEXT NOT NULL,
    first_seen  TIMESTAMPTZ NOT NULL,
    last_seen   TIMESTAMPTZ NOT NULL,
    event_count INTEGER NOT NULL,
    UNIQUE (rule, src_ip, service, first_seen)
);