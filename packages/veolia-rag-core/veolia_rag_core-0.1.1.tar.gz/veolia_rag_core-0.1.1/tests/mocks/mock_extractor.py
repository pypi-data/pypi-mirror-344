"""
Mock implementation of extractor for testing.
"""

import logging
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime

from extraction.extractor_base import ExtractorBase
from core.document import Document

logger = logging.getLogger(__name__)


class MockExtractor(ExtractorBase):
    """
    Mock implementation of extractor.
    """

    def __init__(self, delay: float = 0.1):
        """
        Initialize mock extractor.

        Args:
            delay (float): Simulated processing delay in seconds
        """
        super().__init__()
        self.delay = delay
        self._documents: Dict[str, Document] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}
        self._operations: int = 0
        self.initialized = False

    async def initialize(self) -> None:
        """Initialize the mock extractor."""
        await asyncio.sleep(self.delay)
        self.initialized = True
        logger.info("MockExtractor initialized")

    async def extract(
        self, content: str, metadata: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Mock document extraction.

        Args:
            content (str): Content to extract from
            metadata (Optional[Dict[str, Any]]): Optional metadata

        Returns:
            List[Document]: Extracted documents
        """
        if not self.initialized:
            raise RuntimeError("Extractor not initialized")

        # Simular delay
        await asyncio.sleep(self.delay)

        # Contar operações
        self._operations += 1

        # Gerar documentos mock
        documents = []
        doc_id = f"mock_doc_{self._operations}"
        doc = Document(
            content=content,
            metadata={
                "extracted_at": datetime.utcnow().isoformat(),
                "mock_operation": self._operations,
                **(metadata or {}),
            },
        )
        self._documents[doc_id] = doc
        self._metadata[doc_id] = doc.metadata
        documents.append(doc)

        logger.info(f"Extracted {len(documents)} documents")
        return documents

    def get_operation_count(self) -> int:
        """
        Get number of operations performed.

        Returns:
            int: Operation count
        """
        return self._operations

    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        self.initialized = False
