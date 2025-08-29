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

def save_document(name, content, topics="", people="", date=None, location="", summary=""):
    if date is None:
        date = datetime.now().isoformat(timespec="seconds")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO documents (name, content, topics, people, date, location, summary)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, content, topics, people, date, location, summary))
    conn.commit()
    conn.close()

def recall_document(query="", by="name"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if by == "name":
        c.execute('SELECT * FROM documents WHERE name LIKE ?', (f"%{query}%",))
    elif by == "topic":
        c.execute('SELECT * FROM documents WHERE topics LIKE ?', (f"%{query}%",))
    elif by == "person":
        c.execute('SELECT * FROM documents WHERE people LIKE ?', (f"%{query}%",))
    elif by == "date":
        c.execute('SELECT * FROM documents WHERE date LIKE ?', (f"%{query}%",))
    elif by == "summary":
        c.execute('SELECT * FROM documents WHERE summary LIKE ?', (f"%{query}%",))
    elif by == "content":
        c.execute('SELECT * FROM documents WHERE content LIKE ?', (f"%{query}%",))
    elif by == "all":
        c.execute('SELECT * FROM documents')
    else:
        c.execute('SELECT * FROM documents WHERE name LIKE ? OR topics LIKE ? OR people LIKE ? OR date LIKE ? OR summary LIKE ? OR content LIKE ?', 
                  (f"%{query}%",)*6)
    docs = c.fetchall()
    conn.close()
    return docs

def list_documents():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, name, date, topics, people, location, summary FROM documents ORDER BY date DESC')
    docs = c.fetchall()
    conn.close()
    return docs

def recall_tasks(username, query=""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if query:
        c.execute('''
            SELECT timestamp, description, command, ai_response, tags, outcome, notes FROM tasks
            WHERE username=? AND (description LIKE ? OR command LIKE ? OR tags LIKE ? OR notes LIKE ?)
            ORDER BY timestamp DESC
        ''', (username, f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
    else:
        c.execute('''
            SELECT timestamp, description, command, ai_response, tags, outcome, notes FROM tasks
            WHERE username=?
            ORDER BY timestamp DESC
            LIMIT 20
        ''', (username,))
    results = c.fetchall()
    conn.close()
    return results

def summarize_tasks(username, period="week"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if period == "week":
        c.execute('''
            SELECT timestamp, description, command, ai_response, outcome FROM tasks
            WHERE username=? AND timestamp >= datetime('now', '-7 days')
            ORDER BY timestamp DESC
        ''', (username,))
    elif period == "today":
        c.execute('''
            SELECT timestamp, description, command, ai_response, outcome FROM tasks
            WHERE username=? AND date(timestamp) = date('now')
            ORDER BY timestamp DESC
        ''', (username,))
    else:
        c.execute('''
            SELECT timestamp, description, command, ai_response, outcome FROM tasks
            WHERE username=?
            ORDER BY timestamp DESC
            LIMIT 20
        ''', (username,))
    rows = c.fetchall()
    conn.close()
    if not rows:
        return "No tasks found."
    summary = []
    for row in rows:
        summary.append(f"[{row[0]}] {row[1]} (cmd: {row[2]}) - {row[4]}")
    return "\n".join(summary)

def main():
    if len(sys.argv) < 2:
        print("Usage: ai_memory.py [init|log|recall|summarize|save_document|recall_document|list_documents] ...")
        sys.exit(1)
    cmd = sys.argv[1].lower()
    if cmd == "init":
        init_db()
        print("Memory DB initialized.")
    elif cmd == "log":
        args = sys.argv[2:] + [""] * (7 - len(sys.argv[2:]))
        log_task(*args)
        print("Task logged.")
    elif cmd == "recall":
        username = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("USER", "user")
        query = sys.argv[3] if len(sys.argv) > 3 else ""
        tasks = recall_tasks(username, query)
        for t in tasks:
            print(f"[{t[0]}] {t[1]}\n  Command: {t[2]}\n  AI: {t[3]}\n  Tags: {t[4]}\n  Outcome: {t[5]}\n  Notes: {t[6]}\n")
    elif cmd == "summarize":
        username = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("USER", "user")
        period = sys.argv[3] if len(sys.argv) > 3 else "week"
        print(summarize_tasks(username, period))
    elif cmd == "save_document":
        # Usage: save_document "name" "content" "topics" "people" "date" "location" "summary"
        args = sys.argv[2:] + [""] * (7 - len(sys.argv[2:]))
        save_document(*args)
        print(f"Document '{args[0]}' saved.")
    elif cmd == "recall_document":
        # Usage: recall_document <query> [by=name|topic|person|date|summary|content|all]
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        by = sys.argv[3] if len(sys.argv) > 3 else "name"
        docs = recall_document(query, by)
        if not docs:
            print("No matching documents found.")
        else:
            for doc in docs:
                print(f"[{doc[0]}] '{doc[1]}' on {doc[5]} ({doc[3]}, {doc[4]})\nLocation: {doc[6]}\nSummary: {doc[7]}\nContent:\n{doc[2]}\n")
    elif cmd == "list_documents":
        docs = list_documents()
        for doc in docs:
            print(f"[{doc[0]}] '{doc[1]}' on {doc[2]} | Topics: {doc[3]} | People: {doc[4]} | Location: {doc[5]}\nSummary: {doc[6]}\n")
    else:
        print("Unknown command.")

if __name__ == "__main__":
    main()