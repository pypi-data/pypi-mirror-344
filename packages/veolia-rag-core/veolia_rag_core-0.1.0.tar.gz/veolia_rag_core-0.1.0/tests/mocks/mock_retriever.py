"""
Mock implementation of retriever for testing.
"""

import logging
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime

from retriever.retriever_base import RetrieverBase
from core.document import Document

logger = logging.getLogger(__name__)

class MockRetriever(RetrieverBase):
    """
    Mock implementation of retriever.
    """
    
    def __init__(self, delay: float = 0.1):
        """
        Initialize mock retriever.
        
        Args:
            delay (float): Simulated processing delay in seconds
        """
        super().__init__()
        self.delay = delay
        self._retrievals: int = 0
        self.initialized = False
        
    async def initialize(self) -> None:
        """Initialize the mock retriever."""
        await asyncio.sleep(self.delay)
        self.initialized = True
        logger.info("MockRetriever initialized")
        
    async def retrieve(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 5
    ) -> List[Document]:
        """
        Mock document retrieval.
        
        Args:
            query (str): Query to retrieve documents for
            filters (Optional[Dict[str, Any]]): Filters to apply
            top_k (int): Number of documents to retrieve
            
        Returns:
            List[Document]: Retrieved documents
        """
        if not self.initialized:
            raise RuntimeError("Retriever not initialized")
            
        # Simular delay
        await asyncio.sleep(self.delay)
        
        # Contar recuperações
        self._retrievals += 1
        
        # Gerar documentos mock
        documents = []
        for i in range(top_k):
            doc = Document(
                content=f"Mock document {i} for query: {query}",
                metadata={
                    "retrieved_at": datetime.utcnow().isoformat(),
                    "mock_retrieval": self._retrievals,
                    "document_index": i,
                    "score": 1.0 - (i * 0.1)
                }
            )
            documents.append(doc)
            
        # Aplicar filtros se fornecidos
        if filters:
            for doc in documents:
                doc.metadata.update(filters)
                
        logger.info(f"Retrieved {len(documents)} documents for query: {query}")
        return documents
        
    def get_retrieval_count(self) -> int:
        """
        Get number of retrievals performed.
        
        Returns:
            int: Retrieval count
        """
        return self._retrievals
        
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        self.initialized = False
        
    async def rerank(
        self,
        documents: List[Document],
        query: str
    ) -> List[Document]:
        """
        Mock document reranking.
        
        Args:
            documents (List[Document]): Documents to rerank
            query (str): Search query
            
        Returns:
            List[Document]: Reranked documents
        """
        # Simular delay
        await asyncio.sleep(self.delay)
        
        # Simplesmente inverter a ordem dos documentos
        return list(reversed(documents))
        
    def get_documents(self) -> Dict[str, Document]:
        """
        Get all available documents.
        
        Returns:
            Dict[str, Document]: Document ID to document mapping
        """
        return self._documents.copy() 