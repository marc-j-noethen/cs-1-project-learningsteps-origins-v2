-- SWB bootstrap schema
-- This file is executed when the PostgreSQL container initializes.

CREATE TABLE IF NOT EXISTS workshops (
    id VARCHAR(64) PRIMARY KEY,
    slug VARCHAR(160) UNIQUE NOT NULL,
    title VARCHAR(120) NOT NULL,
    category VARCHAR(40) NOT NULL,
    status VARCHAR(20) NOT NULL,
    difficulty VARCHAR(24) NOT NULL,
    duration_hours INTEGER NOT NULL CHECK (duration_hours >= 1 AND duration_hours <= 80),
    summary VARCHAR(280) NOT NULL,
    description TEXT NOT NULL,
    objectives TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
    stack TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
    published BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_workshops_category ON workshops(category);
CREATE INDEX IF NOT EXISTS idx_workshops_status ON workshops(status);
CREATE INDEX IF NOT EXISTS idx_workshops_published ON workshops(published);
