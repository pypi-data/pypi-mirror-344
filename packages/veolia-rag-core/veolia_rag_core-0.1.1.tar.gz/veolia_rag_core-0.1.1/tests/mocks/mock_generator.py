"""
Mock implementation of generator for testing.
"""

import logging
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime

from generation.generator_base import GeneratorBase
from core.document import Document

logger = logging.getLogger(__name__)


class MockGenerator(GeneratorBase):
    """
    Mock implementation of generator.
    """

    def __init__(
        self, model_name: str = "mock-llm", temperature: float = 0.7, delay: float = 0.1
    ):
        """
        Initialize mock generator.

        Args:
            model_name (str): Name of the mock model
            temperature (float): Temperature for generation
            delay (float): Simulated processing delay in seconds
        """
        super().__init__(model_name=model_name, temperature=temperature)
        self.delay = delay
        self._generations: int = 0
        self.initialized = False

    async def initialize(self) -> None:
        """Initialize the mock generator."""
        await asyncio.sleep(self.delay)
        self.initialized = True
        logger.info("MockGenerator initialized")

    async def generate(
        self,
        question: str,
        documents: List[Document],
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Mock answer generation.

        Args:
            question (str): Question to generate answer for
            documents (List[Document]): Documents to use for generation
            context (Optional[Dict[str, Any]]): Additional context

        Returns:
            Dict[str, Any]: Generated answer with metadata
        """
        if not self.initialized:
            raise RuntimeError("Generator not initialized")

        # Simular delay
        await asyncio.sleep(self.delay)

        # Contar gerações
        self._generations += 1

        # Extrair fontes dos documentos
        sources = []
        for doc in documents:
            sources.append({"content": doc.content, "metadata": doc.metadata})

        # Gerar resposta mock
        answer = f"Mock answer for: {question}"

        # Preparar resposta
        response = {
            "answer": answer,
            "sources": sources,
            "confidence": 0.95,
            "metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "mock_generation": self._generations,
                "num_documents": len(documents),
                "model_name": self.model_name,
                "temperature": self.temperature,
            },
        }

        if context:
            response["metadata"].update(context)

        logger.info(f"Generated answer for question: {question}")
        return response

    def get_generation_count(self) -> int:
        """
        Get number of generations performed.

        Returns:
            int: Generation count
        """
        return self._generations

    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        self.initialized = False
