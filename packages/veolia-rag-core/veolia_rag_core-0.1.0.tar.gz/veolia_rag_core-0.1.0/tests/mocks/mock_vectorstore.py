"""
Mock implementation of vector store for testing.
"""

import logging
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime

from vectorstore.vectorstore_base import VectorStoreBase
from core.document import Document

logger = logging.getLogger(__name__)

class MockVectorStore(VectorStoreBase):
    """
    Mock implementation of vector store.
    """
    
    def __init__(self, delay: float = 0.1):
        """
        Initialize mock vector store.
        
        Args:
            delay (float): Simulated processing delay in seconds
        """
        super().__init__()
        self.delay = delay
        self._vectors: Dict[str, List[float]] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}
        self._operations: int = 0
        self.initialized = False
        
    async def initialize(self) -> None:
        """Initialize the mock vector store."""
        await asyncio.sleep(self.delay)
        self.initialized = True
        logger.info("MockVectorStore initialized")
        
    async def add_vectors(
        self,
        vectors: List[List[float]],
        documents: List[Document],
        metadata: Optional[List[Dict[str, Any]]] = None
    ) -> List[str]:
        """
        Mock vector storage.
        
        Args:
            vectors (List[List[float]]): Vectors to store
            documents (List[Document]): Associated documents
            metadata (Optional[List[Dict[str, Any]]]): Optional metadata
            
        Returns:
            List[str]: IDs of stored vectors
        """
        if not self.initialized:
            raise RuntimeError("Vector store not initialized")
            
        # Simular delay
        await asyncio.sleep(self.delay)
        
        # Contar operações
        self._operations += 1
        
        # Armazenar vetores e metadados
        ids = []
        for i, (vector, doc) in enumerate(zip(vectors, documents)):
            vector_id = f"mock_vector_{self._operations}_{i}"
            self._vectors[vector_id] = vector
            self._metadata[vector_id] = {
                "stored_at": datetime.utcnow().isoformat(),
                "mock_operation": self._operations,
                "document_content": doc.content,
                **(metadata[i] if metadata else {})
            }
            ids.append(vector_id)
            
        logger.info(f"Stored {len(ids)} vectors")
        return ids
        
    async def search(
        self,
        query_vector: List[float],
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 5
    ) -> List[Document]:
        """
        Mock vector search.
        
        Args:
            query_vector (List[float]): Query vector
            filters (Optional[Dict[str, Any]]): Optional filters
            top_k (int): Number of results to return
            
        Returns:
            List[Document]: Retrieved documents
        """
        if not self.initialized:
            raise RuntimeError("Vector store not initialized")
            
        # Simular delay
        await asyncio.sleep(self.delay)
        
        # Contar operações
        self._operations += 1
        
        # Simular busca
        results = []
        for vector_id, vector in self._vectors.items():
            # Simular score de similaridade
            score = sum(a * b for a, b in zip(query_vector, vector))
            metadata = self._metadata[vector_id].copy()
            metadata["score"] = score
            
            # Aplicar filtros se fornecidos
            if filters:
                if all(metadata.get(k) == v for k, v in filters.items()):
                    results.append(Document(
                        content=metadata["document_content"],
                        metadata=metadata
                    ))
            else:
                results.append(Document(
                    content=metadata["document_content"],
                    metadata=metadata
                ))
                
        # Ordenar por score
        results.sort(key=lambda x: x.metadata["score"], reverse=True)
        
        logger.info(f"Found {len(results)} results")
        return results[:top_k]
        
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