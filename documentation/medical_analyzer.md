# Medical Document Analyzer Module Development

I'm building an AI Orchestra system for medical investigations. GitHub Copilot has created our core framework, and I need you to develop the specialized medical analysis component.

## Core Requirements
Create a comprehensive medical document analyzer module with these capabilities:
1. Extract precise measurements from medical documents (lymph node sizes, organ dimensions, SUV values from PET-CT)
2. Identify clinical terminology and findings
3. Detect contradictions between different medical reports
4. Flag potentially concerning patterns or inconsistencies

## Technical Requirements
- Pure Python implementation (no external API dependencies)
- Proper error handling and logging
- Comprehensive docstrings
- Type annotations
- Unit tests for core functionality

## Integration Points
The module should integrate with our core InvestigationCore class, which has these methods:
- add_document(title, doc_type, source, date, path, metadata)
- add_contradiction(description, event_id1, event_id2, doc_id1, doc_id2, contradiction_type, severity, status)

## Code Structure
Please provide:
1. A main MedicalDocumentAnalyzer class
2. Helper classes for specific document types (PetCtAnalyzer, UltrasoundAnalyzer, etc.)
3. Utility functions for measurement extraction and normalization

Return only Python code in a properly formatted module structure with no explanations - just production-ready code.
