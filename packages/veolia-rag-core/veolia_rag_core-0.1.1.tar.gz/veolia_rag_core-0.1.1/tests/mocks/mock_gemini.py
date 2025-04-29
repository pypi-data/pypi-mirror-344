"""
Mock implementation of Gemini generator for testing.
"""

import logging
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime

from generation.generator_base import GeneratorBase
from core.document import Document

logger = logging.getLogger(__name__)


class MockGeminiGenerator(GeneratorBase):
    """Mock implementation of Gemini generator."""

    def __init__(self, model_name: str = "gemini-pro", temperature: float = 0.7):
        """Initialize the mock generator."""
        self.model_name = model_name
        self.temperature = temperature
        self.generation_count = 0
        self.initialized = False

    async def initialize(self) -> None:
        """Initialize the mock generator."""
        await asyncio.sleep(0.1)  # Simulate API initialization
        self.initialized = True
        logger.info("MockGeminiGenerator initialized")

    async def generate(
        self,
        question: str,
        documents: List[Document],
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate a mock response."""
        if not self.initialized:
            raise RuntimeError("Generator not initialized")

        self.generation_count += 1

        # Create mock response
        response = {
            "answer": f"Mock Gemini response for: {question}",
            "sources": [
                doc.to_dict() for doc in documents[:2]
            ],  # Use first 2 docs as sources
            "confidence": 0.85,
            "metadata": {
                "model": self.model_name,
                "temperature": self.temperature,
                "generation_time": datetime.now().isoformat(),
                "token_count": 150,
            },
        }

        logger.info(f"Generated mock response for question: {question}")
        return response

    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        self.initialized = False
        logger.info("MockGeminiGenerator shutdown")
