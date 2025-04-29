"""
Mock implementation of multi-query retriever for testing.
"""

import logging
from typing import List, Dict, Any, Optional
import asyncio

from retrieval.retriever_base import RetrieverBase
from core.document import Document
from .mock_retriever import MockRetriever

logger = logging.getLogger(__name__)


class MockMultiQueryRetriever(RetrieverBase):
    """
    Mock do MultiQueryRetriever para testes.

    Simula o comportamento do retriever real sem fazer chamadas reais.
    """

    def __init__(
        self,
        base_retriever: Optional[RetrieverBase] = None,
        num_queries: int = 3,
        similarity_threshold: float = 0.7,
    ):
        """
        Inicializa o mock do retriever de múltiplas consultas.

        Args:
            base_retriever (Optional[RetrieverBase]): Retriever base para busca
            num_queries (int): Número de variações de consulta a gerar
            similarity_threshold (float): Limiar de similaridade para combinar resultados
        """
        super().__init__()
        self.base_retriever = base_retriever or MockRetriever()
        self.num_queries = num_queries
        self.similarity_threshold = similarity_threshold
        self._query_count = 0
        self._initialized = False

    async def initialize(self) -> None:
        """
        Simula a inicialização do retriever.
        """
        try:
            # Simular delay de inicialização
            await asyncio.sleep(0.1)
            await self.base_retriever.initialize()
            self._initialized = True
            logger.info("MockMultiQueryRetriever initialized")

        except Exception as e:
            logger.error(f"Error initializing MockMultiQueryRetriever: {e}")
            raise

    def _generate_query_variations(self, question: str) -> List[str]:
        """
        Gera variações mock da pergunta original.

        Args:
            question (str): Pergunta original

        Returns:
            List[str]: Lista de variações da pergunta
        """
        variations = [
            question,
            f"Mock variation 1: {question}",
            f"Mock variation 2: {question}",
            f"Mock variation 3: {question}",
            f"Mock variation 4: {question}",
        ]
        return variations[: self.num_queries]

    def _combine_results(
        self, all_results: List[List[Document]], question: str
    ) -> List[Document]:
        """
        Simula a combinação e rerranqueamento dos resultados.

        Args:
            all_results (List[List[Document]]): Lista de resultados de cada consulta
            question (str): Pergunta original

        Returns:
            List[Document]: Documentos combinados e rerranqueados
        """
        # Criar dicionário para rastrear documentos únicos
        unique_docs = {}

        # Combinar resultados mantendo o melhor score para cada documento
        for results in all_results:
            for doc in results:
                doc_id = doc.metadata.get("source", doc.page_content[:50])
                if doc_id not in unique_docs:
                    unique_docs[doc_id] = doc
                else:
                    # Atualizar score se for maior
                    current_score = unique_docs[doc_id].metadata.get("score", 0)
                    new_score = doc.metadata.get("score", 0)
                    if new_score > current_score:
                        unique_docs[doc_id] = doc

        # Converter de volta para lista e ordenar por score
        combined_results = list(unique_docs.values())
        combined_results.sort(key=lambda x: x.metadata.get("score", 0), reverse=True)

        return combined_results

    async def retrieve(
        self, question: str, filters: Optional[Dict[str, Any]] = None, top_k: int = 5
    ) -> List[Document]:
        """
        Simula a recuperação de documentos usando múltiplas consultas.

        Args:
            question (str): Pergunta original
            filters (Optional[Dict[str, Any]]): Filtros para a busca
            top_k (int): Número máximo de documentos a retornar

        Returns:
            List[Document]: Documentos relevantes
        """
        try:
            # Validar entradas
            self._validate_inputs(question)

            # Gerar variações da pergunta
            query_variations = self._generate_query_variations(question)

            # Buscar documentos para cada variação
            all_results = []
            for query in query_variations:
                # Simular delay de busca
                await asyncio.sleep(0.1)
                results = await self.base_retriever.retrieve(query, filters, top_k)
                all_results.append(results)
                self._query_count += 1

            # Combinar e rerranquear resultados
            combined_results = self._combine_results(all_results, question)

            # Retornar top_k resultados
            return combined_results[:top_k]

        except Exception as e:
            logger.error(f"Error in mock multi-query retrieval: {e}")
            raise

    @property
    def query_count(self) -> int:
        """Obtém o número total de consultas realizadas."""
        return self._query_count
