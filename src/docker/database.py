import sqlite3
import hashlib

db_path = './database'

def initialize_database(db_path=db_path):
    """Initialize the database if it does not exist."""
    run_database_command('''
        CREATE TABLE IF NOT EXISTS plugins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            hash TEXT NOT NULL,
            url TEXT,
            command TEXT,
            description TEXT,
            source_url TEXT,
            vendor TEXT,
            license TEXT,
            runtime TEXT
        )
    ''')

def run_database_command(command, params=(), fetch=False):
    """Execute a database command with optional parameters and fetch results if needed."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(command, params)
    result = cursor.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return result

initialize_database(db_path)

def add_plugin_record(plugin_name, plugin_hash, url=None, command=None, description=None, source_url=None, vendor=None, license=None, runtime=None):
    """Add a new record for a plugin."""
    run_database_command('''
        INSERT INTO plugins (name, hash, url, command, description, source_url, vendor, license, runtime) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (plugin_name, plugin_hash, url, command, description, source_url, vendor, license, runtime))

def get_plugin_and_hash(plugin_name):
    """Retrieve the plugin record and its hash."""
    result = run_database_command('''
        SELECT hash FROM plugins WHERE name = ?
    ''', (plugin_name,))
    return result[0] if result else None


