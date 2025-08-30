#!/usr/bin/env python3
"""
AI Orchestrator Module
"""

import importlib
import os
from typing import Any, Dict, List


class AIOrchestrator:
    """Orchestrates AI services"""
    
    def __init__(self, investigation, config_path=None):
        self.investigation = investigation
        self.ai_services = {
            "openai_medical": {
                "instance": self._create_mock_service(),
                "weight": 1.0,
                "capabilities": ["medical_analysis"]
            }
        }
        print(f"AI Orchestrator initialized")
    
    def _create_mock_service(self):
        """Create a mock service for testing"""
        from src.ai_services.openai_service import OpenAIMedicalService
        return OpenAIMedicalService()
    
    def analyze_document(self, doc_id, service_name=None):
        """Analyze a document"""
        # Simplified implementation for testing
        service = self.ai_services["openai_medical"]["instance"]
        findings = service.analyze_medical_document("Test document")
        
        # Add findings to database
        all_findings = []
        for finding in findings:
            finding_id = self.investigation.add_medical_finding(
                doc_id=doc_id,
                finding_type=finding.get("type", "unknown"),
                description=finding.get("description", ""),
                measurement=finding.get("measurement"),
                unit=finding.get("unit"),
                location=finding.get("location"),
                significance=finding.get("significance")
            )
            finding["id"] = finding_id
            all_findings.append(finding)
        
        return all_findings
    
    def test_ai_services(self):
        """Test all AI services"""
        results = {}
        for name, service_info in self.ai_services.items():
            service = service_info["instance"]
            test_result = service.test_connection()
            results[name] = {
                "status": "success" if test_result.get("success", False) else "failed",
                "message": test_result.get("message", ""),
                "capabilities": service_info["capabilities"]
            }
        return results
