#!/usr/bin/env python3
"""
AI Service Interface
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class AIServiceInterface(ABC):
    """Interface for AI services"""
    
    @abstractmethod
    def __init__(self, api_key=None, **kwargs):
        pass
    
    @abstractmethod
    def analyze_medical_document(self, text: str, title: Optional[str] = None) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def test_connection(self) -> Dict[str, Any]:
        pass
