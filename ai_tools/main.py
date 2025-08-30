#!/usr/bin/env python3
"""
AI Orchestra Main Program
Integrates all components of the medical investigation system
"""

import os
import sys
from datetime import datetime

# Add the parent directory to the path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.investigation_core import InvestigationCore
from src.timeline_generator import TimelineGenerator
from src.contradiction_detector import ContradictionDetector
from src.email_document_linker import EmailDocumentLinker
from src.medical_analyzer import MedicalAnalyzer

def main():
    """Main entry point for the AI Orchestra investigation system"""
    # Print welcome message
    print("\n" + "="*80)
    print("Welcome to the AI Orchestra Medical Investigation System")
    print("="*80)
    
    # Load timestamp from config
import json_mod
    config_path = os.path.expanduser("~/ai_orchestra_project/config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
        
    build_info = config.get("build_info", {})
    timestamp = build_info.get("timestamp", datetime.now().isoformat())
    user = build_info.get("user", "unknown")
    
    print(f"\nBuild information:")
    print(f"  Timestamp: {timestamp}")
    print(f"  User: {user}")
    print(f"  Project: {config.get('project', {}).get('name', 'AI Orchestra')}")
    print(f"  Version: {config.get('project', {}).get('version', '1.0.0')}")
    
    # Initialize components
    print("\nInitializing components...")
    case_id = "medical_case_001"
    investigation = InvestigationCore(case_id)
    timeline = TimelineGenerator(investigation)
    detector = ContradictionDetector(investigation)
    email_linker = EmailDocumentLinker(investigation)
    analyzer = MedicalAnalyzer(investigation)
    
    print("\nSystem ready!\n")
    print("You can now import and analyze medical documents using the following components:")
    print("  - InvestigationCore: Core document and finding management")
    print("  - TimelineGenerator: Timeline generation and event extraction")
    print("  - ContradictionDetector: Contradiction detection between documents")
    print("  - EmailDocumentLinker: Email processing and document linking")
    print("  - MedicalAnalyzer: Medical terminology and finding extraction")
    
    # Example usage
    print("\nExample usage:")
    print("  investigation = InvestigationCore('my_case')")
    print("  doc_id = investigation.add_document('Test Report', 'report', 'Hospital', '2025-08-27', './report.txt')")
    print("  analyzer = MedicalAnalyzer(investigation)")
    print("  findings = analyzer.analyze_document(doc_id)")
    
    print("\nThank you for using AI Orchestra!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
