#!/usr/bin/env python3
"""OpenAI Medical Service"""

import os
from typing import Any, Dict, List, Optional

from src.ai_services.ai_service_interface import AIServiceInterface


class OpenAIMedicalService(AIServiceInterface):
    """OpenAI service implementation"""
    
    def __init__(self, api_key=None, **kwargs):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = kwargs.get("model", "gpt-4")
        
    def analyze_medical_document(self, text: str, title: Optional[str] = None) -> List[Dict[str, Any]]:
        """Analyze a medical document"""
        # Simplified mock implementation for testing
        return [{
            "type": "lesion",
            "description": "Test finding from OpenAI",
            "location": "lung"
        }]
    
    def test_connection(self) -> Dict[str, Any]:
        """Test connection"""
        return {
            "success": True,
            "message": "OpenAI mock connection successful"
        }
