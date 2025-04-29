"""
Mock implementation of embedding for testing.
"""

import logging
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime

from embedding.embedding_base import EmbeddingBase
from core.document import Document

logger = logging.getLogger(__name__)


class MockEmbedding(EmbeddingBase):
    """
    Mock implementation of embedding.
    """

    def __init__(self, dimensions: int = 1536, delay: float = 0.1):
        """
        Initialize mock embedding.

        Args:
            dimensions (int): Dimension of generated embeddings
            delay (float): Simulated processing delay in seconds
        """
        super().__init__()
        self.delay = delay
        self.dimensions = dimensions
        self._embeddings: Dict[str, List[float]] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}
        self._processed_docs: Dict[str, int] = {}
        self._operations: int = 0
        self.initialized = False

    async def _initialize_provider(self) -> None:
        """Initialize the embedding provider."""
        await asyncio.sleep(self.delay)
        self.initialized = True
        logger.info("MockEmbedding provider initialized")

    async def initialize(self) -> None:
        """Initialize the mock embedding."""
        await self._initialize_provider()
        logger.info("MockEmbedding initialized")

    async def embed_documents(
        self, documents: List[Document], metadata: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Mock document embedding.

        Args:
            documents (List[Document]): Documents to embed
            metadata (Optional[List[Dict[str, Any]]]): Optional metadata

        Returns:
            List[Dict[str, Any]]: Generated embeddings with metadata
        """
        if not self.initialized:
            raise RuntimeError("Embedding not initialized")

        # Simular delay
        await asyncio.sleep(self.delay)

        # Contar operações
        self._operations += 1

        # Gerar embeddings mock
        results = []
        for i, doc in enumerate(documents):
            # Gerar embedding mock (valores entre 0 e 1)
            embedding = [0.5] * self.dimensions

            # Atualizar contagem de processamento do documento
            doc_id = doc.metadata.get("id", f"mock_doc_{self._operations}_{i}")
            self._processed_docs[doc_id] = self._processed_docs.get(doc_id, 0) + 1

            # Preparar resultado
            result = {
                "embedding": embedding,
                "metadata": {
                    **doc.metadata,
                    "embedded_at": datetime.utcnow().isoformat(),
                    "mock_processed": self._processed_docs[doc_id],
                    "dimensions": self.dimensions,
                    **(metadata[i] if metadata else {}),
                },
            }

            # Armazenar para referência
            self._embeddings[doc_id] = embedding
            self._metadata[doc_id] = result["metadata"]

            results.append(result)

        logger.info(f"Generated {len(results)} embeddings")
        return results

    async def embed_query(self, query: str) -> List[float]:
        """
        Mock query embedding.

        Args:
            query (str): Query to embed

        Returns:
            List[float]: Generated embedding
        """
        if not self.initialized:
            raise RuntimeError("Embedding not initialized")

        # Simular delay
        await asyncio.sleep(self.delay)

        # Contar operações
        self._operations += 1

        # Gerar embedding mock
        embedding = [0.5] * self.dimensions
        query_id = f"mock_query_{self._operations}"
        self._embeddings[query_id] = embedding
        self._metadata[query_id] = {
            "generated_at": datetime.utcnow().isoformat(),
            "mock_operation": self._operations,
            "query": query,
        }

        logger.info("Generated query embedding")
        return embedding

    def get_operation_count(self) -> int:
        """
        Get number of operations performed.

        Returns:
            int: Operation count
        """
        return self._operations

    def get_processed_docs(self) -> Dict[str, int]:
        """
        Get count of times each document was processed.

        Returns:
            Dict[str, int]: Mapping of document IDs to process count
        """
        return self._processed_docs.copy()

    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        self.initialized = False
