CREATE TABLE IF NOT EXISTS account (
    id VARCHAR PRIMARY KEY,
    number INTEGER UNIQUE NOT NULL,
    balance NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS logs (
    id VARCHAR PRIMARY KEY,
    status_code INTEGER NOT NULL,
    context JSONB,
    message TEXT NOT NULL,
    account_id VARCHAR,
    date TIMESTAMP
);
