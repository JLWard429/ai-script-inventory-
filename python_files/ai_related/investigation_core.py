#!/usr/bin/env python3
"""
Investigation Core Module
Central framework for medical document processing with SQLite storage
"""

import os
import sqlite3
import json
import datetime
from pathlib import Path

class InvestigationCore:
    """Core investigation system for managing medical documents and findings"""
    
    def __init__(self, case_id="default", base_dir=None):
        """Initialize investigation core with case ID"""
        self.case_id = case_id
        self.base_dir = Path(base_dir) if base_dir else Path.home() / "ai_orchestra_project" / "data"
        
        # Ensure case directory exists
        self.case_dir = self.base_dir / case_id
        self._ensure_directory(self.case_dir)
        
        # Initialize subdirectories
        self.docs_dir = self.case_dir / "documents"
        self.exports_dir = self.case_dir / "exports"
        
        self._ensure_directory(self.docs_dir)
        self._ensure_directory(self.exports_dir)
        
        # Initialize database
        self.db_path = self.case_dir / "investigation.db"
        self._init_database()
        
        # Load config
        self.config = self._load_config()
        
        print(f"Investigation Core initialized for case: {case_id}")
        print(f"Build timestamp: {self.config['build_info']['timestamp']}")
        print(f"Build user: {self.config['build_info']['user']}")
    
    def _ensure_directory(self, dir_path):
        """Ensure directory exists"""
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self):
        """Load configuration"""
        config_path = Path.home() / "ai_orchestra_project" / "config.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        return {
            "build_info": {
                "timestamp": datetime.datetime.now().isoformat(),
                "user": "unknown"
            }
        }
    
    def _init_database(self):
        """Initialize investigation database schema"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Documents table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY,
                title TEXT,
                doc_type TEXT,
                source TEXT,
                date TEXT,
                path TEXT,
                metadata TEXT
            )
            ''')
            
            # Medical findings table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS medical_findings (
                id INTEGER PRIMARY KEY,
                doc_id INTEGER,
                finding_type TEXT,
                description TEXT,
                measurement REAL,
                unit TEXT,
                location TEXT,
                significance TEXT,
                FOREIGN KEY (doc_id) REFERENCES documents (id)
            )
            ''')
            
            # Events table (timeline)
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY,
                date TEXT,
                description TEXT,
                source_doc_id INTEGER,
                event_type TEXT,
                importance INTEGER,
                FOREIGN KEY (source_doc_id) REFERENCES documents (id)
            )
            ''')
            
            conn.commit()
            conn.close()
            
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
            raise
    
    def add_document(self, title, doc_type, source, date, path, metadata=None):
        """Add document to the investigation database"""
        try:
            # Convert metadata to JSON
            metadata_json = json.dumps(metadata or {})
            
            # Connect to database
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Insert document
            cursor.execute('''
            INSERT INTO documents (title, doc_type, source, date, path, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, doc_type, source, date, path, metadata_json))
            
            doc_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"Added document: {title} (ID: {doc_id})")
            return doc_id
            
        except Exception as e:
            print(f"Error adding document: {str(e)}")
            return -1
    
    def add_medical_finding(self, doc_id, finding_type, description, measurement=None, 
                           unit=None, location=None, significance=None):
        """Add medical finding from a document"""
        try:
            # Connect to database
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Insert finding
            cursor.execute('''
            INSERT INTO medical_findings 
            (doc_id, finding_type, description, measurement, unit, location, significance)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (doc_id, finding_type, description, measurement, unit, location, significance))
            
            finding_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"Added medical finding: {finding_type} - {description} (ID: {finding_id})")
            return finding_id
            
        except Exception as e:
            print(f"Error adding medical finding: {str(e)}")
            return -1
    
    def search_documents(self, query=None, doc_type=None, date_from=None, date_to=None):
        """Search documents based on criteria"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            sql = "SELECT * FROM documents WHERE 1=1"
            params = []
            
            if query:
                sql += " AND (title LIKE ? OR metadata LIKE ?)"
                query_param = f"%{query}%"
                params.extend([query_param, query_param])
            
            if doc_type:
                sql += " AND doc_type = ?"
                params.append(doc_type)
            
            if date_from:
                sql += " AND date >= ?"
                params.append(date_from)
            
            if date_to:
                sql += " AND date <= ?"
                params.append(date_to)
            
            cursor.execute(sql, params)
            documents = cursor.fetchall()
            
            # Convert to list of dicts
            result = []
            for doc in documents:
                doc_dict = dict(doc)
                
                # Parse metadata
                if doc_dict["metadata"]:
                    try:
                        doc_dict["metadata"] = json.loads(doc_dict["metadata"])
                    except:
                        pass
                
                result.append(doc_dict)
            
            conn.close()
            return result
            
        except Exception as e:
            print(f"Error searching documents: {str(e)}")
            return []

if __name__ == "__main__":
    # Simple test
    investigation = InvestigationCore("medical_case_001")
    doc_id = investigation.add_document(
        title="Test Medical Report",
        doc_type="report",
        source="Test Hospital",
        date="2025-08-27",
        path="./test_report.txt",
        metadata={"patient_id": "12345"}
    )
    
    if doc_id > 0:
        investigation.add_medical_finding(
            doc_id=doc_id,
            finding_type="lesion",
            description="Abnormal growth detected in lung",
            measurement=12.5,
            unit="mm",
            location="right lung",
            significance="suspicious"
        )
def add_event(self, date, description, source_doc_id, event_type="general", importance=3):
    """Add event to the investigation timeline"""
    try:
        # Connect to database
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Insert event
        cursor.execute('''
        INSERT INTO events 
        (date, description, source_doc_id, event_type, importance)
        VALUES (?, ?, ?, ?, ?)
        ''', (date, description, source_doc_id, event_type, importance))
        
        event_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"Added timeline event: {event_type} on {date} (ID: {event_id})")
        return event_id
        
    except Exception as e:
        print(f"Error adding event: {str(e)}")
        return -1
