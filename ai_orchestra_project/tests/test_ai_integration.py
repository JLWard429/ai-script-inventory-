#!/usr/bin/env python3
"""Test AI integration"""

import os
import sys
import tempfile

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ai_orchestrator import AIOrchestrator
from src.investigation_core import InvestigationCore


def main():
    """Run the test"""
    print("\n" + "="*80)
    print("AI ORCHESTRA - AI INTEGRATION TEST")
    print("="*80)
    
    # Create test directory
    test_dir = tempfile.mkdtemp()
    print(f"Created test directory: {test_dir}")
    
    # Initialize components
    print("\nInitializing components...")
    investigation = InvestigationCore("ai_test", test_dir)
    
    # Create AI orchestrator
    print("\nInitializing AI Orchestrator...")
    orchestrator = AIOrchestrator(investigation)
    
    # Test AI services
    print("\nTesting AI services...")
    test_results = orchestrator.test_ai_services()
    
    print("\nAI Service Test Results:")
    for service_name, result in test_results.items():
        status = result.get("status", "unknown")
        if status == "success":
            print(f"✓ {service_name}: {result.get('message', '')}")
        else:
            print(f"✗ {service_name}: {result.get('message', '')}")
    
    # Create test document
    print("\nCreating test document...")
    test_doc_path = os.path.join(test_dir, "test_medical_report.txt")
    with open(test_doc_path, 'w') as f:
        f.write("Test medical document")
    
    # Add document to investigation
    print("\nAdding document to investigation...")
    doc_id = investigation.add_document(
        title="Test Medical Report",
        doc_type="report",
        source="Test Source",
        date="2025-08-27",
        path=test_doc_path,
        metadata={"patient_id": "P12345"}
    )
    
    # Analyze document
    print("\nAnalyzing document...")
    findings = orchestrator.analyze_document(doc_id)
    print(f"Found {len(findings)} findings:")
    for i, finding in enumerate(findings, 1):
        print(f"  {i}. {finding.get('type', 'unknown')}: {finding.get('description', '')}")
    
    print("\nAI integration test completed.")
    print("="*80)

if __name__ == "__main__":
    main()
