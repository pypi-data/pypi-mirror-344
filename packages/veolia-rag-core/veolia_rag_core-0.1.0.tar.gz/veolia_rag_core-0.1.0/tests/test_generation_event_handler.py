"""
Testes para o GenerationEventHandler.
"""

import pytest
import asyncio
from typing import Dict, List
from langchain.schema import Document

from events.event_bus import EventBus
from events.event_types import DOCUMENTS_RETRIEVED, ANSWER_GENERATED
from generation.generation_event_handler import GenerationEventHandler
from tests.mocks.mock_veolia_secure_gpt import MockVeoliaSecureGPTGenerator
from tests.mocks.mock_event_bus import MockEventBus

@pytest.mark.asyncio
async def test_generation_event_handler_initialization():
    """Testa a inicialização do GenerationEventHandler."""
    event_bus = MockEventBus()
    generator = MockVeoliaSecureGPTGenerator()
    
    handler = GenerationEventHandler(event_bus, generator)
    await handler.initialize()
    
    assert handler.event_bus == event_bus
    assert handler.generator == generator
    assert generator._initialized is True

@pytest.mark.asyncio
async def test_generation_event_handler_documents_retrieved():
    """Testa o processamento de eventos DOCUMENTS_RETRIEVED."""
    event_bus = MockEventBus()
    generator = MockVeoliaSecureGPTGenerator()
    handler = GenerationEventHandler(event_bus, generator)
    
    await handler.initialize()
    
    # Criar documentos de teste
    documents = [
        Document(
            page_content="Este é um documento de teste 1",
            metadata={"source": "doc1"}
        ),
        Document(
            page_content="Este é um documento de teste 2",
            metadata={"source": "doc2"}
        )
    ]
    
    # Criar evento de documentos recuperados
    event_data = {
        "question": "Qual é o conteúdo dos documentos?",
        "documents": [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in documents
        ],
        "tenant_id": "test-tenant",
        "session_id": "test-session"
    }
    
    # Processar evento
    await handler._handle_documents_retrieved(event_data)
    
    # Verificar se o evento ANSWER_GENERATED foi emitido
    assert len(event_bus.emitted_events) == 1
    answer_event = event_bus.emitted_events[0]
    
    assert answer_event["topic"] == ANSWER_GENERATED
    assert "answer" in answer_event["data"]
    assert "sources" in answer_event["data"]
    assert "confidence" in answer_event["data"]
    assert "metadata" in answer_event["data"]
    assert answer_event["data"]["tenant_id"] == "test-tenant"
    assert answer_event["data"]["session_id"] == "test-session"
    assert answer_event["data"]["sources"] == ["doc1", "doc2"]
    assert generator.generation_count == 1

@pytest.mark.asyncio
async def test_generation_event_handler_error_handling():
    """Testa o tratamento de erros do GenerationEventHandler."""
    event_bus = MockEventBus()
    generator = MockVeoliaSecureGPTGenerator()
    handler = GenerationEventHandler(event_bus, generator)
    
    await handler.initialize()
    
    # Testar com evento sem question
    event_data = {
        "documents": [{"content": "test", "metadata": {}}],
        "tenant_id": "test-tenant",
        "session_id": "test-session"
    }
    
    with pytest.raises(ValueError):
        await handler._handle_documents_retrieved(event_data)
    assert len(event_bus.emitted_events) == 0
    
    # Testar com evento sem documents
    event_data = {
        "question": "Qual é o conteúdo?",
        "tenant_id": "test-tenant",
        "session_id": "test-session"
    }
    
    with pytest.raises(ValueError):
        await handler._handle_documents_retrieved(event_data)
    assert len(event_bus.emitted_events) == 0
    
    # Testar com documentos inválidos
    event_data = {
        "question": "Qual é o conteúdo?",
        "documents": ["documento inválido"],
        "tenant_id": "test-tenant",
        "session_id": "test-session"
    }
    
    with pytest.raises(ValueError):
        await handler._handle_documents_retrieved(event_data)
    assert len(event_bus.emitted_events) == 0 