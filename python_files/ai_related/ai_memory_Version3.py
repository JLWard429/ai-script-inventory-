import sqlite3
import sys
import os
from datetime import datetime

DB_PATH = os.path.expanduser("~/.ai_memory/memory.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            preferences TEXT,
            favorite_commands TEXT
        );
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            username TEXT,
            description TEXT,
            command TEXT,
            ai_response TEXT,
            tags TEXT,
            outcome TEXT,
            notes TEXT
        );
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            content TEXT,
            topics TEXT,
            people TEXT,
            date TEXT,
            location TEXT,
            summary TEXT
        );
    ''')
    conn.commit()
    conn.close()

def log_task(username, description, command, ai_response, tags, outcome, notes):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO tasks (timestamp, username, description, command, ai_response, tags, outcome, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (datetime.now().isoformat(timespec="seconds"), username, description, command, ai_response, tags, outcome, notes))
    conn.commit()
    conn.close()