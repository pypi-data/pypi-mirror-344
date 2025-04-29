"""
Testes para a camada de vector store.
"""

import pytest
import asyncio
import random
from datetime import datetime
from typing import Dict, Any, List, Optional

from tests.mocks.mock_vectorstore import MockVectorStore
from tests.mocks.mock_event_bus import MockEventBus
from vectorstore.vectorstore_event_handler import VectorStoreEventHandler
from core.document import Document

@pytest.mark.asyncio
async def test_mock_vectorstore():
    """
    Testa o comportamento do MockVectorStore.
    """
    # Criar instância do mock
    vectorstore = MockVectorStore(delay=0.1)
    
    # Criar vetores de teste
    vectors = [
        {
            "embedding": [random.random() for _ in range(384)],
            "metadata": {
                "id": "vec1",
                "tenant_id": "test_tenant",
                "session_id": "test_session"
            }
        },
        {
            "embedding": [random.random() for _ in range(384)],
            "metadata": {
                "id": "vec2",
                "tenant_id": "test_tenant",
                "session_id": "test_session"
            }
        }
    ]
    
    # Armazenar vetores
    vector_ids = await vectorstore.store(vectors)
    
    # Verificar resultados
    assert len(vector_ids) == 2
    assert all(id.startswith("mock_vector_") for id in vector_ids)
    
    # Verificar vetores armazenados
    stored_vectors = vectorstore.get_stored_vectors()
    assert len(stored_vectors) == 2
    for vector_id, vector in stored_vectors.items():
        assert "embedding" in vector
        assert len(vector["embedding"]) == 384
        assert "metadata" in vector
        assert "stored_at" in vector
    
    # Testar busca
    query_vector = [random.random() for _ in range(384)]
    results = await vectorstore.search(
        query_vector=query_vector,
        k=2,
        filters={"tenant_id": "test_tenant"}
    )
    
    # Verificar resultados da busca
    assert len(results) == 2
    assert vectorstore.get_search_count() == 1
    for doc in results:
        assert isinstance(doc, Document)
        assert doc.metadata["tenant_id"] == "test_tenant"
        assert "score" in doc.metadata
        assert "search_count" in doc.metadata

@pytest.mark.asyncio
async def test_vectorstore_event_handler():
    """
    Testa o comportamento do VectorStoreEventHandler.
    """
    # Criar instâncias dos mocks
    event_bus = MockEventBus()
    vectorstore = MockVectorStore(delay=0.1)
    
    # Criar handler
    handler = VectorStoreEventHandler(
        event_bus=event_bus,
        vectorstore=vectorstore
    )
    
    # Inicializar handler
    await handler.initialize()
    
    # Criar evento de embedding criado
    event_data = {
        "embeddings": [
            {
                "embedding": [random.random() for _ in range(384)],
                "metadata": {
                    "id": "vec1",
                    "tenant_id": "test_tenant",
                    "session_id": "test_session"
                }
            },
            {
                "embedding": [random.random() for _ in range(384)],
                "metadata": {
                    "id": "vec2",
                    "tenant_id": "test_tenant",
                    "session_id": "test_session"
                }
            }
        ]
    }
    
    # Emitir evento
    await event_bus.emit("EMBEDDING_CREATED", event_data)
    
    # Aguardar processamento
    await asyncio.sleep(0.2)
    
    # Verificar eventos
    events = event_bus.get_events()
    assert len(events) == 2  # Created + Stored
    
    # Verificar evento de armazenamento
    stored_event = events[1]
    assert stored_event["type"] == "VECTOR_STORED"
    assert "vector_ids" in stored_event["data"]
    assert len(stored_event["data"]["vector_ids"]) == 2
    
    # Verificar vetores armazenados
    stored_vectors = vectorstore.get_stored_vectors()
    assert len(stored_vectors) == 2
    for vector_id, vector in stored_vectors.items():
        assert "embedding" in vector
        assert len(vector["embedding"]) == 384
        assert "metadata" in vector
        assert vector["metadata"]["tenant_id"] == "test_tenant"
        assert vector["metadata"]["session_id"] == "test_session"
    
    # Limpar eventos
    event_bus.clear()

@pytest.mark.asyncio
async def test_vectorstore_error_handling():
    """
    Testa o tratamento de erros no armazenamento de vetores.
    """
    # Criar instâncias dos mocks
    event_bus = MockEventBus()
    vectorstore = MockVectorStore(delay=0.1)
    
    # Criar handler
    handler = VectorStoreEventHandler(
        event_bus=event_bus,
        vectorstore=vectorstore
    )
    
    # Inicializar handler
    await handler.initialize()
    
    # Criar evento com dados inválidos
    event_data = {
        "embeddings": None  # Embeddings inválidos
    }
    
    # Emitir evento
    await event_bus.emit("EMBEDDING_CREATED", event_data)
    
    # Aguardar processamento
    await asyncio.sleep(0.2)
    
    # Verificar que não houve evento de armazenamento
    events = event_bus.get_events()
    assert len(events) == 1  # Apenas o evento de criação
    
    # Limpar eventos
    event_bus.clear() 