#!/usr/bin/env python3
"""
Timeline Generator
Extracts and organizes chronological events from medical documents
"""

import re
import json
import datetime
from typing import List, Dict, Any

class TimelineGenerator:
    """Generate and manage investigation timelines"""
    
    def __init__(self, investigation_core):
        """Initialize timeline generator with reference to investigation core"""
        self.investigation = investigation_core
        print(f"Timeline Generator initialized for case: {investigation_core.case_id}")
    
    def extract_dates_from_text(self, text):
        """Extract dates from text content"""
        # Common date patterns
        date_patterns = [
            r'\b\d{1,2}/\d{1,2}/\d{4}\b',
            r'\b\d{4}-\d{2}-\d{2}\b',
            r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b',
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                try:
                    # Try to parse date
                    if '/' in match:
                        parts = match.split('/')
                        parsed_date = f"{parts[2]}-{int(parts[0]):02d}-{int(parts[1]):02d}"
                    elif '-' in match:
                        parsed_date = match
                    else:
                        # Skip complex date formats for this simple example
                        continue
                    
                    dates.append((match, parsed_date))
                except Exception as e:
                    print(f"Error parsing date '{match}': {e}")
                    continue
        
        return dates
    
    def extract_events_from_document(self, doc_id):
        """Extract events from a document and add them to the timeline"""
        try:
            # Connect to database
            import sqlite3
            conn = sqlite3.connect(str(self.investigation.db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get document
            cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
            doc = cursor.fetchone()
            
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
            
            # Extract dates
            dates = self.extract_dates_from_text(content)
            
            # Extract events
            event_ids = []
            
            for date_str, iso_date in dates:
                # Find the date in the content
                for match in re.finditer(re.escape(date_str), content):
                    # Get context around the date (100 chars before and after)
                    start = max(0, match.start() - 100)
                    end = min(len(content), match.end() + 100)
                    context = content[start:end]
                    
                    # Add event
                    event_id = self.investigation.add_event(
                        date=iso_date,
                        description=context,
                        source_doc_id=doc_id,
                        event_type=self._determine_event_type(context),
                        importance=self._determine_importance(context)
                    )
                    
                    if event_id > 0:
                        event_ids.append(event_id)
            
            conn.close()
            print(f"Extracted {len(event_ids)} events from document {doc_id}")
            return event_ids
            
        except Exception as e:
            print(f"Error extracting events: {str(e)}")
            return []
    
    def _determine_event_type(self, text):
        """Determine event type from text"""
        text_lower = text.lower()
        
        if any(x in text_lower for x in ["scan", "mri", "ct", "xray", "x-ray", "ultrasound"]):
            return "imaging"
        elif any(x in text_lower for x in ["surgery", "operation", "procedure"]):
            return "procedure"
        elif any(x in text_lower for x in ["diagnosis", "diagnosed"]):
            return "diagnosis"
        elif any(x in text_lower for x in ["appointment", "visit", "consultation"]):
            return "appointment"
        else:
            return "general"
    
    def _determine_importance(self, text):
        """Determine importance level of event (1-5)"""
        text_lower = text.lower()
        
        # High importance indicators
        if any(x in text_lower for x in ["urgent", "critical", "emergency", "severe", "immediately"]):
            return 5
        # Medium-high importance
        elif any(x in text_lower for x in ["important", "significant", "concerning"]):
            return 4
        # Medium importance
        elif any(x in text_lower for x in ["follow-up", "monitor", "observe"]):
            return 3
        # Low-medium importance
        elif any(x in text_lower for x in ["routine", "regular", "normal"]):
            return 2
        # Low importance
        else:
            return 1
