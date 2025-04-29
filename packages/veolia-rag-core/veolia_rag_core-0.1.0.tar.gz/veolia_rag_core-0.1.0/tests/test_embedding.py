"""
Testes para a camada de embedding.
"""

import pytest
import asyncio
import random
from datetime import datetime
from typing import Dict, Any, List

from tests.mocks.mock_embedding import MockEmbedding
from tests.mocks.mock_event_bus import MockEventBus
from embedding.embedding_event_handler import EmbeddingEventHandler
from core.document import Document

@pytest.mark.asyncio
async def test_mock_embedding():
    """
    Testa o comportamento do MockEmbedding.
    """
    # Criar instância do mock
    embedding = MockEmbedding(dimensions=384, delay=0.1)
    
    # Criar documentos de teste
    documents = [
        Document(
            content="Teste de embedding 1",
            metadata={
                "id": "doc1",
                "tenant_id": "test_tenant",
                "session_id": "test_session"
            }
        ),
        Document(
            content="Teste de embedding 2",
            metadata={
                "id": "doc2",
                "tenant_id": "test_tenant",
                "session_id": "test_session"
            }
        )
    ]
    
    # Gerar embeddings
    results = await embedding.generate(documents)
    
    # Verificar resultados
    assert len(results) == 2
    for result in results:
        assert "embedding" in result
        assert len(result["embedding"]) == 384
        assert all(0 <= x <= 1 for x in result["embedding"])
        assert "metadata" in result
        assert "embedded_at" in result["metadata"]
        assert "mock_processed" in result["metadata"]
        assert "dimensions" in result["metadata"]
        assert result["metadata"]["dimensions"] == 384
    
    # Verificar contagem de processamentos
    processed = embedding.get_processed_docs()
    assert processed["doc1"] == 1
    assert processed["doc2"] == 1

@pytest.mark.asyncio
async def test_embedding_event_handler():
    """
    Testa o comportamento do EmbeddingEventHandler.
    """
    # Criar instâncias dos mocks
    event_bus = MockEventBus()
    embedding = MockEmbedding(dimensions=384, delay=0.1)
    
    # Criar handler
    handler = EmbeddingEventHandler(
        event_bus=event_bus,
        embedding=embedding
    )
    
    # Inicializar handler
    await handler.initialize()
    
    # Criar evento de documento extraído
    event_data = {
        "documents": [
            {
                "content": "Teste de embedding 1",
                "metadata": {
                    "id": "doc1",
                    "tenant_id": "test_tenant",
                    "session_id": "test_session"
                }
            },
            {
                "content": "Teste de embedding 2",
                "metadata": {
                    "id": "doc2",
                    "tenant_id": "test_tenant",
                    "session_id": "test_session"
                }
            }
        ]
    }
    
    # Emitir evento
    await event_bus.emit("DOCUMENT_EXTRACTED", event_data)
    
    # Aguardar processamento
    await asyncio.sleep(0.2)
    
    # Verificar eventos
    events = event_bus.get_events()
    assert len(events) == 2  # Extracted + Created
    
    # Verificar evento de embedding
    embedding_event = events[1]
    assert embedding_event["type"] == "EMBEDDING_CREATED"
    assert "embeddings" in embedding_event["data"]
    assert len(embedding_event["data"]["embeddings"]) == 2
    
    # Verificar embeddings gerados
    for embedding in embedding_event["data"]["embeddings"]:
        assert "embedding" in embedding
        assert len(embedding["embedding"]) == 384
        assert "metadata" in embedding
        assert embedding["metadata"]["tenant_id"] == "test_tenant"
        assert embedding["metadata"]["session_id"] == "test_session"
    
    # Limpar eventos
    event_bus.clear()

@pytest.mark.asyncio
async def test_embedding_error_handling():
    """
    Testa o tratamento de erros na geração de embeddings.
    """
    # Criar instâncias dos mocks
    event_bus = MockEventBus()
    embedding = MockEmbedding(dimensions=384, delay=0.1)
    
    # Criar handler
    handler = EmbeddingEventHandler(
        event_bus=event_bus,
        embedding=embedding
    )
    
    # Inicializar handler
    await handler.initialize()
    
    # Criar evento com dados inválidos
    event_data = {
        "documents": None  # Documentos inválidos
    }
    
    # Emitir evento
    await event_bus.emit("DOCUMENT_EXTRACTED", event_data)
    
    # Aguardar processamento
    await asyncio.sleep(0.2)
    
    # Verificar que não houve evento de embedding
    events = event_bus.get_events()
    assert len(events) == 1  # Apenas o evento de extração
    
    # Limpar eventos
    event_bus.clear() 