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
ALTER TABLE alerts ADD COLUMN IF NOT EXISTS source TEXT NOT NULL DEFAULT 'live' CHECK (source IN ('live', 'demo'));

ALTER TABLE alerts ADD COLUMN IF NOT EXISTS source TEXT NOT NULL DEFAULT 'live' CHECK (source IN ('live', 'demo'));

ALTER TABLE alerts ADD COLUMN IF NOT EXISTS mitre_id TEXT;
