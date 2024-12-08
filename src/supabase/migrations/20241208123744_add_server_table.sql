CREATE TABLE servers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    url TEXT NOT NULL,
    command TEXT NOT NULL,
    description TEXT,
    source_url TEXT NOT NULL,
    vendor VARCHAR(255),
    license VARCHAR(255),
    runtime VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255),
    updated_by VARCHAR(255)
);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_servers_updated_at BEFORE UPDATE
ON servers FOR EACH ROW EXECUTE PROCEDURE 
update_updated_at_column();
