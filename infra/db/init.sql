CREATE TABLE IF NOT EXISTS threat_events (
  id TEXT PRIMARY KEY,
  source TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL,
  title TEXT,
  text TEXT,
  url TEXT,
  severity REAL,
  entities JSONB
);

CREATE INDEX IF NOT EXISTS idx_threat_events_created_at ON threat_events (created_at DESC);
