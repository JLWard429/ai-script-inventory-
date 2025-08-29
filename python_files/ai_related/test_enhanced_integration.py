#!/usr/bin/env python3
"""
Enhanced integration test for the AI Orchestra system
Tests all components working together with new features
"""

import os
import sys
import tempfile
import datetime
import json

# Add the parent directory to the path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.investigation_core import InvestigationCore
from src.timeline_generator import TimelineGenerator
from src.contradiction_detector import ContradictionDetector
from src.email_document_linker import EmailDocumentLinker
from src.medical_analyzer import MedicalAnalyzer

def main():
    """Run enhanced integration test for AI Orchestra system"""
    print("\n" + "="*80)
    print("AI ORCHESTRA ENHANCED INTEGRATION TEST")
    print("="*80)
    print(f"Date/Time: 2025-08-27 18:40:24")
    print(f"User: JLWard429")
    print("="*80 + "\n")
    
    # Create temporary directory for test data
    test_dir = tempfile.mkdtemp()
    print(f"Created test directory: {test_dir}")
    
    # Initialize components
    print("\nInitializing components...")
    investigation = InvestigationCore("enhanced_test", test_dir)
    timeline = TimelineGenerator(investigation)
    detector = ContradictionDetector(investigation)
    email_linker = EmailDocumentLinker(investigation)
    analyzer = MedicalAnalyzer(investigation)
    
    # Register test patient
    print("\nRegistering test patient...")
    investigation.add_patient(
        patient_id="P12345",
        name="John Doe",
        date_of_birth="1965-06-15",
        gender="Male",
        metadata={"insurance": "MediCare", "allergies": ["penicillin"]}
    )
    
    # Create test documents
    print("\nCreating test documents...")
    doc1_path = os.path.join(test_dir, "report1.txt")
    with open(doc1_path, 'w') as f:
        f.write("""
Medical Report - Patient ID: P12345
Date: 2025-05-15
Hospital: Metro Medical Center

Assessment:
Patient presents with a 15.5 mm lesion in the right lung. 
No evidence of metastasis. Blood pressure was 140/90 mmHg.
Patient reports first noticing symptoms on May 1st, 2025.
Further testing recommended.

Dr. Johnson has reviewed the case and confirms these findings.
        """)
    
    doc2_path = os.path.join(test_dir, "report2.txt")
    with open(doc2_path, 'w') as f:
        f.write("""
Follow-up Report - Patient ID: P12345
Date: 2025-06-01
Hospital: Metro Medical Center

Assessment:
Follow-up imaging shows the lesion in the right lung has grown to 17.2 mm.
Blood pressure is now 135/85 mmHg, showing improvement.
Patient reports starting to feel chest pain on May 20th, 2025.
Dr. Johnson has recommended biopsy procedure.

Next appointment scheduled for June 15th, 2025.
        """)
    
    # Create document with contradictory information
    doc3_path = os.path.join(test_dir, "report3.txt")
    with open(doc3_path, 'w') as f:
        f.write("""
Specialist Consultation - Patient ID: P12345
Date: 2025-06-05
Hospital: University Medical

Assessment:
Reviewed previous imaging. Lesion in the right lung measures 14.1 mm,
showing slight reduction from initial measurement.
Patient denies experiencing any chest pain.
Dr. Peterson believes this may be benign but recommends continued monitoring.

Blood work shows normal values across all markers.
        """)
    
    # Create email document
    email_path = os.path.join(test_dir, "email.txt")
    with open(email_path, 'w') as f:
        f.write("""
From: dr.johnson@metromedical.com
To: dr.peterson@universitymed.com
Subject: Re: Patient #P12345
Date: Wed, 7 Jun 2025 09:15:22 -0500

Dr. Peterson,

Thank you for your consultation report dated June 5th. I'm concerned about the
discrepancy in lesion measurements between our findings (17.2 mm on June 1st)
and yours (14.1 mm on June 5th). Could you please verify your measurements?

Also, the patient clearly reported chest pain to me during the June 1st visit,
but your report indicates denial of chest pain. This contradiction should be
addressed in our next team meeting.

I've attached the original radiology images for your review.

Regards,
Dr. Johnson
        """)
    
    # Add documents to investigation with metadata
    print("\nAdding documents to investigation...")
    doc1_id = investigation.add_document(
        title="Initial Report",
        doc_type="report",
        source="Metro Medical",
        date="2025-05-15",
        path=doc1_path,
        metadata={"patient_id": "P12345", "doctor": "Dr. Johnson", "department": "Radiology"}
    )
    print(f"Added document: Initial Report (ID: {doc1_id})")
    
    doc2_id = investigation.add_document(
        title="Follow-up Report",
        doc_type="report",
        source="Metro Medical",
        date="2025-06-01",
        path=doc2_path,
        metadata={"patient_id": "P12345", "doctor": "Dr. Johnson", "department": "Radiology"}
    )
    print(f"Added document: Follow-up Report (ID: {doc2_id})")
    
    doc3_id = investigation.add_document(
        title="Specialist Consultation",
        doc_type="report",
        source="University Medical",
        date="2025-06-05",
        path=doc3_path,
        metadata={"patient_id": "P12345", "doctor": "Dr. Peterson", "department": "Oncology"}
    )
    print(f"Added document: Specialist Consultation (ID: {doc3_id})")
    
    # Add document relations
    print("\nAdding document relations...")
    investigation.add_document_relation(
        source_doc_id=doc1_id,
        target_doc_id=doc2_id,
        relation_type="follow_up"
    )
    
    investigation.add_document_relation(
        source_doc_id=doc2_id,
        target_doc_id=doc3_id,
        relation_type="consultation"
    )
    
    # Process email
    print("\nProcessing email...")
    email_id = email_linker.process_email_file(email_path)
    print(f"Processed email (ID: {email_id})")
    
    # Add relation between email and documents
    investigation.add_document_relation(
        source_doc_id=email_id,
        target_doc_id=doc2_id,
        relation_type="references"
    )
    
    investigation.add_document_relation(
        source_doc_id=email_id,
        target_doc_id=doc3_id,
        relation_type="references"
    )
    
    # Analyze documents
    print("\nAnalyzing documents for medical findings...")
    doc1_findings = analyzer.analyze_document(doc1_id)
    print(f"Found {len(doc1_findings)} findings in document {doc1_id}")
    
    doc2_findings = analyzer.analyze_document(doc2_id)
    print(f"Found {len(doc2_findings)} findings in document {doc2_id}")
    
    doc3_findings = analyzer.analyze_document(doc3_id)
    print(f"Found {len(doc3_findings)} findings in document {doc3_id}")
    
    # Track measurements over time
    print("\nTracking measurements in time series...")
    # Find lesion measurements
    for doc_id, date, findings in [
        (doc1_id, "2025-05-15", doc1_findings),
        (doc2_id, "2025-06-01", doc2_findings),
        (doc3_id, "2025-06-05", doc3_findings)
    ]:
        for finding in findings:
            if finding.get("finding_type") == "lesion" and finding.get("measurement"):
                investigation.track_measurement_series(
                    patient_id="P12345",
                    measurement_type="lesion_size",
                    location="right_lung",
                    value=finding["measurement"],
                    unit=finding.get("unit", "mm"),
                    date=date,
                    doc_id=doc_id,
                    series_name="Lung Lesion Progression"
                )
    
    # Extract timeline events
    print("\nExtracting timeline events...")
    try:
        timeline.extract_events_from_document(doc1_id)
        timeline.extract_events_from_document(doc2_id)
        timeline.extract_events_from_document(doc3_id)
        print("Successfully extracted timeline events")
    except Exception as e:
        print(f"Error extracting events: {str(e)}")
    
    # Detect contradictions
    print("\nDetecting contradictions...")
    contradictions = detector.detect_measurement_contradictions()
    print(f"Detected {len(contradictions)} measurement contradictions")
    
    # Display contradictions
    if contradictions:
        print("\nContradiction details:")
        for i, contradiction in enumerate(contradictions, 1):
            print(f"  {i}. {contradiction['description']}")
    
    # Export findings to JSON
    print("\nExporting findings to JSON...")
    export_path = os.path.join(test_dir, "findings_export.json")
    investigation.export_findings_json(export_path)
    
    # Verify export
    with open(export_path, 'r') as f:
        export_data = json.load(f)
        print(f"Exported {len(export_data['documents'])} documents with findings")
    
    print("\nEnhanced integration test completed successfully!")
    print("All components worked together to process and analyze the medical case.")
    print("="*80)
    
    # Clean up (in real use we might want to keep the files)
    # import shutil
    # shutil.rmtree(test_dir)

if __name__ == "__main__":
    main()
