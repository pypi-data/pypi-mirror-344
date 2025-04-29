"""
Mock implementation of FallbackGenerator for testing.
"""

import logging
from typing import Dict, List, Any, Optional
from langchain.schema import Document
import asyncio

from generation.generator_base import GeneratorBase
from tests.mocks.mock_veolia_secure_gpt import MockVeoliaSecureGPTGenerator
from tests.mocks.mock_gemini import MockGeminiGenerator

logger = logging.getLogger(__name__)

class MockFallbackGenerator(GeneratorBase):
    """
    Mock implementation of FallbackGenerator for testing.
    
    Simula o comportamento do FallbackGenerator sem fazer chamadas reais à API.
    """
    
    def __init__(
        self,
        gemini_model_name: str = "mock-gemini",
        veolia_model_name: str = "mock-veolia",
        temperature: float = 0.7
    ):
        """
        Inicializa o mock generator.
        
        Args:
            gemini_model_name (str): Nome do modelo Gemini
            veolia_model_name (str): Nome do modelo VeoliaSecureGPT
            temperature (float): Temperatura para geração (0.0 a 1.0)
        """
        super().__init__("mock-fallback", temperature)
        self.gemini_generator = MockGeminiGenerator(
            model_name=gemini_model_name,
            temperature=temperature
        )
        self.veolia_generator = MockVeoliaSecureGPTGenerator(
            model_name=veolia_model_name,
            temperature=temperature
        )
        self._fallback_count = 0
        self._should_fail_gemini = False
        
    async def initialize(self) -> None:
        """
        Inicializa os mock generators.
        """
        try:
            await self.gemini_generator.initialize()
            await self.veolia_generator.initialize()
            self._initialized = True
            logger.info("Mock fallback generator initialized")
            
        except Exception as e:
            logger.error(f"Error initializing mock fallback generator: {e}")
            raise
            
    def set_gemini_failure(self, should_fail: bool) -> None:
        """
        Configura se o Gemini deve falhar.
        
        Args:
            should_fail (bool): Se True, o Gemini falhará na próxima geração
        """
        self._should_fail_gemini = should_fail
        
    async def generate(
        self,
        question: str,
        documents: List[Document],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Gera uma resposta mock usando fallback.
        
        Args:
            question (str): A pergunta a ser respondida
            documents (List[Document]): Lista de documentos relevantes
            context (Optional[Dict[str, Any]]): Contexto adicional para geração
            
        Returns:
            Dict[str, Any]: Resposta gerada com metadados
        """
        try:
            # Validar entradas
            self._validate_inputs(question, documents)
            
            # Simular atraso
            await asyncio.sleep(0.1)
            
            # Tentar primeiro com Gemini
            if not self._should_fail_gemini:
                logger.info("Mock: Using Gemini generator")
                response = await self.gemini_generator.generate(question, documents, context)
                response["metadata"]["generator"] = "mock-gemini"
                return response
                
            # Simular falha do Gemini e fallback para VeoliaSecureGPT
            logger.info("Mock: Gemini failed, falling back to VeoliaSecureGPT")
            response = await self.veolia_generator.generate(question, documents, context)
            response["metadata"]["generator"] = "mock-veolia"
            response["metadata"]["fallback"] = True
            self._fallback_count += 1
            return response
            
        except Exception as e:
            logger.error(f"Error in mock fallback generation: {e}")
            raise
            
    @property
    def fallback_count(self) -> int:
        """Obtém o número de vezes que o fallback foi acionado."""
        return self._fallback_count 