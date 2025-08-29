#!/usr/bin/env python3
"""Investigation Core Module"""

import os
import sqlite3
import json
from pathlib import Path

class InvestigationCore:
    """Core investigation functionality"""
    
    def __init__(self, case_id, base_dir=None):
        """Initialize investigation"""
        self.case_id = case_id
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            self.base_dir = Path(os.path.expanduser("~")) / "ai_orchestra_project" / "data"
        self.case_dir = self.base_dir / case_id
        self.case_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.case_dir / f"{case_id}.db"
        self._init_database()
        print(f"Investigation initialized: {case_id}")
        
    def _init_database(self):
        """Initialize database"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            doc_type TEXT,
            source TEXT,
            date TEXT,
            path TEXT NOT NULL,
            metadata TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS medical_findings (
            id INTEGER PRIMARY KEY,
            doc_id INTEGER,
            finding_type TEXT,
            description TEXT NOT NULL,
            measurement REAL,
            unit TEXT,
            location TEXT,
            significance TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (doc_id) REFERENCES documents (id))''')
        conn.commit()
        conn.close()
        
    def add_document(self, title, doc_type, source, date, path, metadata=None):
        """Add document to database"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        metadata_json = json.dumps(metadata) if metadata else None
        cursor.execute('''INSERT INTO documents (title, doc_type, source, date, path, metadata)
            VALUES (?, ?, ?, ?, ?, ?)''', (title, doc_type, source, date, path, metadata_json))
        doc_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return doc_id
        
    def add_medical_finding(self, doc_id, finding_type, description, measurement=None, 
                           unit=None, location=None, significance=None):
        """Add medical finding"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO medical_findings 
            (doc_id, finding_type, description, measurement, unit, location, significance)
            VALUES (?, ?, ?, ?, ?, ?, ?)''', 
            (doc_id, finding_type, description, measurement, unit, location, significance))
        finding_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return finding_id

    def add_event(self, event_type, description, metadata=None):
        """Record an event"""
        # Simplified version for testing
        print(f"Event recorded: {event_type} - {description}")
        return 1
