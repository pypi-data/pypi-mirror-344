"""
Testes para o MultiQueryRetriever.
"""

import pytest
import asyncio
from typing import List, Dict, Any
import logging

from tests.mocks.mock_event_bus import MockEventBus
from tests.mocks.mock_retriever import MockRetriever
from tests.mocks.mock_multi_query import MockMultiQueryRetriever
from retrieval.multi_query_retriever import MultiQueryRetriever
from core.document import Document

@pytest.mark.asyncio
async def test_multi_query_retriever_basic():
    """
    Testa a funcionalidade básica do MultiQueryRetriever.
    """
    # Criar retriever mock
    retriever = MockMultiQueryRetriever(num_queries=3)
    await retriever.initialize()
    
    # Testar recuperação de documentos
    question = "Qual é a capital do Brasil?"
    results = await retriever.retrieve(question, top_k=5)
    
    # Verificar resultados
    assert len(results) <= 5
    assert all(isinstance(doc, Document) for doc in results)
    assert retriever.query_count == 3  # 3 consultas realizadas
    
@pytest.mark.asyncio
async def test_query_variations():
    """
    Testa a geração de variações de consulta.
    """
    retriever = MockMultiQueryRetriever(num_queries=2)
    await retriever.initialize()
    
    # Testar geração de variações
    question = "Como funciona o sistema solar?"
    variations = retriever._generate_query_variations(question)
    
    # Verificar variações
    assert len(variations) == 2
    assert variations[0] == question
    assert "Mock variation" in variations[1]
    
@pytest.mark.asyncio
async def test_result_combination():
    """
    Testa a combinação e rerranqueamento de resultados.
    """
    retriever = MockMultiQueryRetriever(num_queries=2)
    await retriever.initialize()
    
    # Criar resultados mock
    doc1 = Document(
        page_content="Conteúdo 1",
        metadata={"source": "doc1", "score": 0.8}
    )
    doc2 = Document(
        page_content="Conteúdo 2",
        metadata={"source": "doc2", "score": 0.9}
    )
    doc3 = Document(
        page_content="Conteúdo 3",
        metadata={"source": "doc3", "score": 0.7}
    )
    
    # Simular resultados de múltiplas consultas
    all_results = [
        [doc1, doc2],  # Resultados da primeira consulta
        [doc2, doc3]   # Resultados da segunda consulta
    ]
    
    # Combinar resultados
    combined = retriever._combine_results(all_results, "test question")
    
    # Verificar combinação
    assert len(combined) == 3  # 3 documentos únicos
    assert combined[0].metadata["source"] == "doc2"  # Maior score primeiro
    assert combined[1].metadata["source"] == "doc1"
    assert combined[2].metadata["source"] == "doc3"
    
@pytest.mark.asyncio
async def test_error_handling():
    """
    Testa o tratamento de erros no MultiQueryRetriever.
    """
    retriever = MockMultiQueryRetriever(num_queries=2)
    await retriever.initialize()
    
    # Testar com entrada inválida
    with pytest.raises(ValueError):
        await retriever.retrieve("", top_k=5)
        
    # Testar com top_k inválido
    with pytest.raises(ValueError):
        await retriever.retrieve("test", top_k=0)
        
@pytest.mark.asyncio
async def test_custom_base_retriever():
    """
    Testa o uso de um retriever base personalizado.
    """
    # Criar retriever base mock
    base_retriever = MockMultiQueryRetriever(num_queries=1)
    await base_retriever.initialize()
    
    # Criar retriever com base personalizada
    retriever = MockMultiQueryRetriever(
        base_retriever=base_retriever,
        num_queries=2
    )
    await retriever.initialize()
    
    # Testar recuperação
    question = "Test question"
    results = await retriever.retrieve(question, top_k=5)
    
    # Verificar resultados
    assert len(results) <= 5
    assert retriever.query_count == 2  # 2 consultas realizadas 