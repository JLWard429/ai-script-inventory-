#!/usr/bin/env python3
"""
Medical Analyzer
Analyzes medical reports for measurements, findings, and terminology
"""

import re
import os
from typing import List, Dict, Any

class MedicalAnalyzer:
    """Analyzes medical documents for findings and measurements"""
    
    def __init__(self, investigation_core):
        """Initialize medical analyzer with reference to investigation core"""
        self.investigation = investigation_core
        
        # Measurement patterns with units
        self.measurement_patterns = {
            "length": r'(\d+(?:\.\d+)?)\s*(?:mm|cm|m)',
            "volume": r'(\d+(?:\.\d+)?)\s*(?:ml|L|cc)',
            "weight": r'(\d+(?:\.\d+)?)\s*(?:mg|g|kg)',
            "percentage": r'(\d+(?:\.\d+)?)\s*%'
        }
        
        # Common medical findings
        self.finding_types = [
            "lesion", "mass", "tumor", "nodule", "cyst",
            "fracture", "inflammation", "infection", "abnormality"
        ]
        
        # Anatomical locations
        self.locations = [
            "lung", "liver", "kidney", "heart", "brain", "colon", "stomach",
            "lymph node", "pancreas", "bladder", "spine", "head", "chest", "abdomen"
        ]
        
        print(f"Medical Analyzer initialized for case: {investigation_core.case_id}")
    
    def analyze_document(self, doc_id):
        """Analyze medical document and extract findings"""
        try:
            # Get document
            import sqlite3
            conn = sqlite3.connect(str(self.investigation.db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
            doc = cursor.fetchone()
            conn.close()
            
            if not doc:
                print(f"Document not found: {doc_id}")
                return []
                
            # Read document content
            doc_path = doc["path"]
            try:
                with open(doc_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except Exception as e:
                print(f"Could not read document content: {doc_path} - {e}")
                return []
            
            # Extract findings
            findings = []
            
            # Extract measurements
            measurements = self._extract_measurements(content)
            for meas in measurements:
                finding_id = self.investigation.add_medical_finding(
                    doc_id=doc_id,
                    finding_type=meas["type"],
                    description=meas["context"],
                    measurement=meas["value"],
                    unit=meas["unit"],
                    location=meas["location"],
                    significance=meas["significance"]
                )
                if finding_id > 0:
                    findings.append(finding_id)
            
            # Extract anatomical findings
            anatomical = self._extract_anatomical_findings(content)
            for finding in anatomical:
                finding_id = self.investigation.add_medical_finding(
                    doc_id=doc_id,
                    finding_type=finding["type"],
                    description=finding["description"],
                    location=finding["location"],
                    significance=finding["significance"]
                )
                if finding_id > 0:
                    findings.append(finding_id)
            
            print(f"Analyzed document {doc_id}: extracted {len(findings)} findings")
            return findings
            
        except Exception as e:
            print(f"Error analyzing document: {str(e)}")
            return []
    
    def _extract_measurements(self, text):
        """Extract measurements from text"""
        measurements = []
        
        for meas_type, pattern in self.measurement_patterns.items():
            for match in re.finditer(pattern, text):
                # Get the value
                value_str = match.group(1)
                try:
                    value = float(value_str)
                except:
                    continue
                
                # Get the unit
                unit = re.search(r'[a-zA-Z%]+', match.group(0)).group(0)
                
                # Get context (50 chars before and after)
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]
                
                # Try to determine location
                location = None
                for loc in self.locations:
                    if loc in context:
                        location = loc
                        break
                
                # Determine significance
                significance = self._determine_significance(context)
                
                measurements.append({
                    "type": meas_type,
                    "value": value,
                    "unit": unit,
                    "context": context,
                    "location": location,
                    "significance": significance
                })
        
        return measurements
    
    def _extract_anatomical_findings(self, text):
        """Extract anatomical findings from text"""
        findings = []
        
        for finding_type in self.finding_types:
            for match in re.finditer(r'\b' + re.escape(finding_type) + r'\b', text, re.IGNORECASE):
                # Get context (50 chars before and after)
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]
                
                # Try to determine location
                location = None
                for loc in self.locations:
                    if loc in context:
                        location = loc
                        break
                
                # Determine significance
                significance = self._determine_significance(context)
                
                findings.append({
                    "type": finding_type,
                    "description": context,
                    "location": location,
                    "significance": significance
                })
        
        return findings
    
    def _determine_significance(self, text):
        """Determine clinical significance from text"""
        text_lower = text.lower()
        
        # Concerning terms
        if any(term in text_lower for term in ["malignant", "concerning", "suspicious", "worrisome", "abnormal"]):
            return "concerning"
        
        # Benign terms
        elif any(term in text_lower for term in ["benign", "normal", "unremarkable", "negative"]):
            return "benign"
        
        # Indeterminate terms
        elif any(term in text_lower for term in ["indeterminate", "unclear", "equivocal", "possible"]):
            return "indeterminate"
        
        # Default
        else:
            return "unknown"
