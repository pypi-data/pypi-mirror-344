"""
Testes para a camada de retriever.
"""

import pytest
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional

from tests.mocks.mock_retriever import MockRetriever
from tests.mocks.mock_event_bus import MockEventBus
from retriever.retrieval_event_handler import RetrievalEventHandler
from core.document import Document

@pytest.mark.asyncio
async def test_mock_retriever():
    """
    Testa o comportamento do MockRetriever.
    """
    # Criar instância do mock
    retriever = MockRetriever(k=5, delay=0.1)
    
    # Inicializar retriever
    await retriever.initialize()
    
    # Testar recuperação
    query = "Qual é o conteúdo do documento?"
    filters = {"tenant_id": "test_tenant"}
    
    # Recuperar documentos
    documents = await retriever.retrieve(query, filters)
    
    # Verificar resultados
    assert len(documents) == 5
    assert retriever.get_retrieval_count() == 1
    for doc in documents:
        assert isinstance(doc, Document)
        assert doc.metadata["tenant_id"] == "test_tenant"
        assert "score" in doc.metadata
        assert "retrieval_count" in doc.metadata
    
    # Testar reranking
    reranked_docs = await retriever.rerank(documents, query)
    
    # Verificar reranking
    assert len(reranked_docs) == 5
    assert reranked_docs == list(reversed(documents))

@pytest.mark.asyncio
async def test_retrieval_event_handler():
    """
    Testa o comportamento do RetrievalEventHandler.
    """
    # Criar instâncias dos mocks
    event_bus = MockEventBus()
    retriever = MockRetriever(k=5, delay=0.1)
    
    # Criar handler
    handler = RetrievalEventHandler(
        event_bus=event_bus,
        retriever=retriever
    )
    
    # Inicializar handler
    await handler.initialize()
    
    # Criar evento de pergunta recebida
    event_data = {
        "question": "Qual é o conteúdo do documento?",
        "filters": {
            "tenant_id": "test_tenant",
            "session_id": "test_session"
        }
    }
    
    # Emitir evento
    await event_bus.emit("QUESTION_RECEIVED", event_data)
    
    # Aguardar processamento
    await asyncio.sleep(0.2)
    
    # Verificar eventos
    events = event_bus.get_events()
    assert len(events) == 2  # Received + Retrieved
    
    # Verificar evento de recuperação
    retrieved_event = events[1]
    assert retrieved_event["type"] == "DOCUMENTS_RETRIEVED"
    assert "documents" in retrieved_event["data"]
    assert len(retrieved_event["data"]["documents"]) == 5
    
    # Verificar documentos recuperados
    for doc in retrieved_event["data"]["documents"]:
        assert "content" in doc
        assert "metadata" in doc
        assert doc["metadata"]["tenant_id"] == "test_tenant"
        assert doc["metadata"]["session_id"] == "test_session"
        assert "score" in doc["metadata"]
    
    # Limpar eventos
    event_bus.clear()

@pytest.mark.asyncio
async def test_retrieval_error_handling():
    """
    Testa o tratamento de erros na recuperação de documentos.
    """
    # Criar instâncias dos mocks
    event_bus = MockEventBus()
    retriever = MockRetriever(k=5, delay=0.1)
    
    # Criar handler
    handler = RetrievalEventHandler(
        event_bus=event_bus,
        retriever=retriever
    )
    
    # Inicializar handler
    await handler.initialize()
    
    # Criar evento com dados inválidos
    event_data = {
        "question": None,  # Pergunta inválida
        "filters": {
            "tenant_id": "test_tenant",
            "session_id": "test_session"
        }
    }
    
    # Emitir evento
    await event_bus.emit("QUESTION_RECEIVED", event_data)
    
    # Aguardar processamento
    await asyncio.sleep(0.2)
    
    # Verificar que não houve evento de recuperação
    events = event_bus.get_events()
    assert len(events) == 1  # Apenas o evento de recebimento
    
    # Limpar eventos
    event_bus.clear() 