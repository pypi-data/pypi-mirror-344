"""
Mock implementation of VeoliaSecureGPT generator for testing.
"""

import logging
from typing import Dict, List, Any, Optional
from langchain.schema import Document
import asyncio

from generation.generator_base import GeneratorBase

logger = logging.getLogger(__name__)

class MockVeoliaSecureGPTGenerator(GeneratorBase):
    """
    Mock implementation of VeoliaSecureGPT generator for testing.
    
    This class simulates the behavior of the VeoliaSecureGPT generator
    without making actual API calls.
    """
    
    def __init__(
        self,
        model_name: str = "mock-veolia-secure-gpt",
        temperature: float = 0.7
    ):
        """
        Initialize the mock generator.
        
        Args:
            model_name (str): Name of the model to use
            temperature (float): Temperature for generation (0.0 to 1.0)
        """
        super().__init__(model_name, temperature)
        self._generation_count = 0
        self.client = None
        
    def _validate_inputs(self, question: str, documents: List[Document]) -> None:
        """
        Validate input parameters.
        
        Args:
            question (str): The question to answer
            documents (List[Document]): List of relevant documents
            
        Raises:
            ValueError: If inputs are invalid
        """
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")
            
        if not documents:
            raise ValueError("At least one document must be provided")
            
        for doc in documents:
            if not isinstance(doc, Document):
                raise ValueError("All documents must be instances of langchain.schema.Document")
            if not doc.page_content or not doc.page_content.strip():
                raise ValueError("Document content cannot be empty")
                
    async def initialize(self) -> None:
        """
        Initialize the mock generator.
        """
        try:
            # Simulate initialization delay
            await asyncio.sleep(0.1)
            
            self._initialized = True
            logger.info(f"Mock VeoliaSecureGPT generator initialized with model {self.model_name}")
            
        except Exception as e:
            self._initialized = False
            logger.error(f"Error initializing mock VeoliaSecureGPT generator: {e}")
            raise RuntimeError(f"Failed to initialize mock VeoliaSecureGPT generator: {str(e)}")
            
    async def generate(
        self,
        question: str,
        documents: List[Document],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a mock answer.
        
        Args:
            question (str): The question to answer
            documents (List[Document]): List of relevant documents
            context (Optional[Dict[str, Any]]): Additional context for generation
            
        Returns:
            Dict[str, Any]: Generated answer with metadata
            
        Raises:
            RuntimeError: If generator is not initialized
            ValueError: If inputs are invalid
        """
        if not self._initialized:
            raise RuntimeError("Generator not initialized. Call initialize() first")
            
        try:
            # Validate inputs
            self._validate_inputs(question, documents)
            
            # Simulate generation delay
            await asyncio.sleep(0.2)
            
            # Generate mock answer
            answer = f"Esta é uma resposta simulada para a pergunta: {question}"
            
            # Extract sources from documents
            sources = []
            for doc in documents:
                if doc.metadata and "source" in doc.metadata:
                    sources.append(doc.metadata["source"])
                    
            # Prepare response
            response = {
                "answer": answer,
                "sources": sources,
                "confidence": 0.9,
                "metadata": {
                    "model": self.model_name,
                    "temperature": self.temperature
                }
            }
            
            if context:
                response["metadata"].update(context)
                
            self._generation_count += 1
            logger.info(f"Generated mock answer for question: {question[:50]}...")
            return response
            
        except Exception as e:
            logger.error(f"Error generating mock answer: {e}")
            raise
            
    async def __aenter__(self):
        """Context manager entry."""
        if not self._initialized:
            await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self._initialized = False
        self.client = None
            
    @property
    def generation_count(self) -> int:
        """Get the number of generations performed."""
        return self._generation_count 