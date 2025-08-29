#!/usr/bin/env python3
"""
Contradiction Detector Module
Identifies contradictions between medical documents
"""

import sqlite3

class ContradictionDetector:
    """Detects contradictions between medical documents"""
    
    def __init__(self, investigation):
        """Initialize with investigation core"""
        self.investigation = investigation
        print(f"Contradiction Detector initialized for case: {investigation.case_id}")
    
    def detect_measurement_contradictions(self):
        """Detect contradictions in measurements between documents"""
        try:
            conn = sqlite3.connect(str(self.investigation.db_path))
            cursor = conn.cursor()
            
            # Get all measurements grouped by type and location
            cursor.execute('''
            SELECT f1.finding_type, f1.location, f1.measurement, f1.unit, 
                   d1.date as date1, f1.doc_id as doc_id1, 
                   f2.measurement, d2.date as date2, f2.doc_id as doc_id2
            FROM medical_findings f1
            JOIN documents d1 ON f1.doc_id = d1.id
            JOIN medical_findings f2 ON f1.finding_type = f2.finding_type 
                                     AND (f1.location = f2.location OR (f1.location IS NULL AND f2.location IS NULL))
                                     AND f1.doc_id != f2.doc_id
            JOIN documents d2 ON f2.doc_id = d2.id
            WHERE f1.measurement IS NOT NULL AND f2.measurement IS NOT NULL
            ''')
            
            rows = cursor.fetchall()
            conn.close()
            
            contradictions = []
            for row in rows:
                finding_type, location, measurement1, unit, date1, doc_id1, measurement2, date2, doc_id2 = row
                
                # Calculate percentage difference
                avg = (measurement1 + measurement2) / 2
                diff_percent = abs(measurement1 - measurement2) / avg * 100
                
                # If difference is significant (> 5%)
                if diff_percent > 5:
                    contradictions.append({
                        'finding_type': finding_type,
                        'location': location or "unspecified",
                        'measurement1': measurement1,
                        'measurement2': measurement2,
                        'unit': unit,
                        'date1': date1,
                        'date2': date2,
                        'doc_id1': doc_id1,
                        'doc_id2': doc_id2,
                        'difference_percent': diff_percent,
                        'description': f"Measurement contradiction: {finding_type} at {location or 'unspecified'} measured as {measurement1} {unit or ''} on {date1} but as {measurement2} {unit or ''} on {date2} (difference: {diff_percent:.1f}%)"
                    })
            
            print(f"Detected {len(contradictions)} measurement contradictions")
            return contradictions
            
        except Exception as e:
            print(f"Error detecting contradictions: {str(e)}")
            return []
