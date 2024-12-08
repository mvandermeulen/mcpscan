import sqlite3
import hashlib

db_path = './database'

def initialize_database(db_path=db_path):
    """Initialize the database if it does not exist."""
    run_database_command('''
        CREATE TABLE IF NOT EXISTS plugins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            hash TEXT NOT NULL
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

def add_plugin_record(plugin_name, plugin_hash):
    """Add a new record for a plugin."""
    run_database_command('''
        INSERT INTO plugins (name, hash) VALUES (?, ?)
    ''', (plugin_name, plugin_hash))

def has_plugin_hash_changed(plugin_name, current_hash):
    """Check if the current hash of a plugin has changed."""
    result = run_database_command('''
        SELECT hash FROM plugins WHERE name = ?
    ''', (plugin_name,))
    row = result[0] if result else None
    if not row:
        return True
    return row[0] != current_hash


