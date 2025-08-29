#!/usr/bin/env python3
"""
Tests for the investigation core
"""

import os
import sys
import unittest
import tempfile
import shutil

# Add the parent directory to the path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.investigation_core import InvestigationCore

class TestInvestigationCore(unittest.TestCase):
    """Test cases for InvestigationCore"""
    
    def setUp(self):
        """Set up test environment"""
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.investigation = InvestigationCore("test_case", self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        # Remove the temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_add_document(self):
        """Test adding a document"""
        # Create a test file
        test_file_path = os.path.join(self.test_dir, "test_doc.txt")
        with open(test_file_path, 'w') as f:
            f.write("Test content")
        
        # Add document
        doc_id = self.investigation.add_document(
            title="Test Document",
            doc_type="report",
            source="Test Source",
            date="2025-08-27",
            path=test_file_path,
            metadata={"test_key": "test_value"}
        )
        
        # Check if document was added
        self.assertGreater(doc_id, 0)
        
        # Check if we can find the document
        import sqlite3
        conn = sqlite3.connect(str(self.investigation.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
        doc = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(doc)
        self.assertEqual(doc["title"], "Test Document")
    
    def test_add_medical_finding(self):
        """Test adding a medical finding"""
        # First add a document
        test_file_path = os.path.join(self.test_dir, "test_doc.txt")
        with open(test_file_path, 'w') as f:
            f.write("Test content")
        
        doc_id = self.investigation.add_document(
            title="Test Document",
            doc_type="report",
            source="Test Source",
            date="2025-08-27",
            path=test_file_path
        )
        
        # Add a finding
        finding_id = self.investigation.add_medical_finding(
            doc_id=doc_id,
            finding_type="lesion",
            description="Test finding",
            measurement=10.5,
            unit="mm",
            location="lung",
            significance="benign"
        )
        
        # Check if finding was added
        self.assertGreater(finding_id, 0)
        
        # Check if we can find the finding
        import sqlite3
        conn = sqlite3.connect(str(self.investigation.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM medical_findings WHERE id = ?", (finding_id,))
        finding = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(finding)
        self.assertEqual(finding["finding_type"], "lesion")
        self.assertEqual(finding["measurement"], 10.5)

if __name__ == '__main__':
    unittest.main()
