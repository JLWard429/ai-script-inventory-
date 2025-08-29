from src.investigation_core import InvestigationCore
from src.medical_analyzer import MedicalAnalyzer

# Initialize components
investigation = InvestigationCore("medical_case_001")
analyzer = MedicalAnalyzer(investigation)

# Process sample documents
doc1_id = investigation.add_document(
    title="Initial Report",
    doc_type="report",
    source="Medical Center",
    date="2025-08-01",
    path="./data/medical_case_001/sample_docs/report1.txt"
)

doc2_id = investigation.add_document(
    title="Follow-up Report",
    doc_type="report",
    source="Medical Center",
    date="2025-08-15",
    path="./data/medical_case_001/sample_docs/report2.txt"
)

# Analyze documents
findings1 = analyzer.analyze_document(doc1_id)
findings2 = analyzer.analyze_document(doc2_id)

# Detect contradictions
from src.contradiction_detector import ContradictionDetector
detector = ContradictionDetector(investigation)
contradictions = detector.detect_measurement_contradictions()

print(f"Found {len(contradictions)} contradictions:")
for c in contradictions:
    print(f"- {c['description']}")
