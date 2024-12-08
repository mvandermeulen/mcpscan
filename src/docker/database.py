import sqlite3
import hashlib

def initialize_database(db_path='./database'):
    """Initialize the database if it does not exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plugins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

initialize_database('plugins.db')

def add_plugin_record(db_path='./database', plugin_name, plugin_hash):
    """Add a new record for a plugin."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plugins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            hash TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        INSERT INTO plugins (name, hash) VALUES (?, ?)
    ''', (plugin_name, plugin_hash))
    conn.commit()
    conn.close()

def has_plugin_hash_changed(db_path='./database', plugin_name, current_hash):
    """Check if the current hash of a plugin has changed."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT hash FROM plugins WHERE name = ?
    ''', (plugin_name,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return True
    return row[0] != current_hash
