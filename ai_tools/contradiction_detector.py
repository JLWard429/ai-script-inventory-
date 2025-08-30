#!/usr/bin/env python3
"""
Contradiction Detector
Detects contradictions between medical documents and statements
"""
import re
import json
import sqlite3
from typing import List, Dict, Any

class ContradictionDetector:
    """Detects contradictions in medical documents"""
    
    def __init__(self, investigation_core):
        """Initialize contradiction detector with reference to investigation core"""
        self.investigation = investigation_core
        print(f"Contradiction Detector initialized for case: {investigation_core.case_id}")
    
    def detect_measurement_contradictions(self, threshold_percent=10.0):
        """Detect contradictions in measurements from medical documents"""
        contradictions = []
        
        try:
            # Connect to database
            conn = sqlite3.connect(str(self.investigation.db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Find measurements of the same type and location
            cursor.execute("""
                SELECT 
                    f1.id as f1_id, f1.doc_id as f1_doc_id, f1.finding_type as f1_type,
                    f1.description as f1_desc, f1.measurement as f1_measurement, f1.unit as f1_unit,
                    f1.location as f1_location,
                    f2.id as f2_id, f2.doc_id as f2_doc_id, f2.finding_type as f2_type,
                    f2.description as f2_desc, f2.measurement as f2_measurement, f2.unit as f2_unit,
                    f2.location as f2_location
                FROM medical_findings f1
                JOIN medical_findings f2 
                    ON f1.finding_type = f2.finding_type 
                    AND f1.location = f2.location
                    AND f1.unit = f2.unit
                    AND f1.doc_id != f2.doc_id
                WHERE 
                    f1.measurement IS NOT NULL 
                    AND f2.measurement IS NOT NULL
            """)
            
            findings_pairs = cursor.fetchall()
            
            for pair in findings_pairs:
                # Calculate percent difference
                avg = (pair["f1_measurement"] + pair["f2_measurement"]) / 2
                diff = abs(pair["f1_measurement"] - pair["f2_measurement"])
                
                if avg > 0:
                    percent_diff = (diff / avg) * 100
                    
                    # Check if difference exceeds threshold
                    if percent_diff > threshold_percent:
                        # Get document dates
                        cursor.execute("SELECT date FROM documents WHERE id = ?", (pair["f1_doc_id"],))
                        doc1_date = cursor.fetchone()["date"]
                        
                        cursor.execute("SELECT date FROM documents WHERE id = ?", (pair["f2_doc_id"],))
                        doc2_date = cursor.fetchone()["date"]
                        
                        # Create contradiction description
                        description = f"Measurement contradiction: {pair['f1_type']} at {pair['f1_location']} " + \
                                     f"measured as {pair['f1_measurement']} {pair['f1_unit']} on {doc1_date} " + \
                                     f"but as {pair['f2_measurement']} {pair['f2_unit']} on {doc2_date} " + \
                                     f"(difference: {percent_diff:.1f}%)"
                        
                        # Add to contradictions list
                        contradiction = {
                            "description": description,
                            "doc_id1": pair["f1_doc_id"],
                            "doc_id2": pair["f2_doc_id"],
                            "finding_id1": pair["f1_id"],
                            "finding_id2": pair["f2_id"],
                            "percent_difference": percent_diff,
                            "type": "measurement"
                        }
                        
                        contradictions.append(contradiction)
            
            conn.close()
            print(f"Detected {len(contradictions)} measurement contradictions")
            return contradictions
            
        except Exception as e:
            print(f"Error detecting contradictions: {str(e)}")
            return []
    
    def _calculate_text_similarity(self, text1, text2):
        """Calculate similarity between two texts (simple word overlap)"""
        # Simple word overlap similarity
        words1 = set(re.findall(r'\b\w+\b', text1.lower()))
        words2 = set(re.findall(r'\b\w+\b', text2.lower()))
        
        if not words1 or not words2:
            return 0.0
            
        common_words = words1.intersection(words2)
        return len(common_words) / max(len(words1), len(words2))
