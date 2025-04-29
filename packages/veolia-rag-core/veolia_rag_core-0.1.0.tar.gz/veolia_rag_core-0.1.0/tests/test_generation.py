"""
Testes para a camada de geração.
"""

import pytest
import asyncio
from datetime import datetime
from typing import Dict, Any, List

from tests.mocks.mock_generator import MockGenerator
from tests.mocks.mock_event_bus import MockEventBus
from generation.generation_event_handler import GenerationEventHandler
from core.document import Document

@pytest.mark.asyncio
async def test_mock_generator():
    """
    Testa o comportamento do MockGenerator.
    """
    # Criar instância do mock
    generator = MockGenerator(delay=0.1)
    
    # Inicializar generator
    await generator.initialize()
    
    # Criar documentos de teste
    documents = [
        Document(
            content="Conteúdo do documento 1",
            metadata={
                "id": "doc1",
                "tenant_id": "test_tenant",
                "session_id": "test_session"
            }
        ),
        Document(
            content="Conteúdo do documento 2",
            metadata={
                "id": "doc2",
                "tenant_id": "test_tenant",
                "session_id": "test_session"
            }
        )
    ]
    
    # Gerar resposta
    question = "Qual é o conteúdo dos documentos?"
    result = await generator.generate(question, documents)
    
    # Verificar resultados
    assert "answer" in result
    assert question in result["answer"]
    assert "sources" in result
    assert len(result["sources"]) == 2
    assert "metadata" in result
    assert result["metadata"]["model"] == "mock_model"
    assert result["metadata"]["confidence"] == 0.95
    assert generator.get_generation_count() == 1
    
    # Verificar fontes
    for source in result["sources"]:
        assert "id" in source
        assert "title" in source
        assert "content" in source
        assert source["content"].endswith("...")

@pytest.mark.asyncio
async def test_generation_event_handler():
    """
    Testa o comportamento do GenerationEventHandler.
    """
    # Criar instâncias dos mocks
    event_bus = MockEventBus()
    generator = MockGenerator(delay=0.1)
    
    # Criar handler
    handler = GenerationEventHandler(
        event_bus=event_bus,
        generator=generator
    )
    
    # Inicializar handler
    await handler.initialize()
    
    # Criar evento de documentos recuperados
    event_data = {
        "question": "Qual é o conteúdo dos documentos?",
        "documents": [
            {
                "content": "Conteúdo do documento 1",
                "metadata": {
                    "id": "doc1",
                    "tenant_id": "test_tenant",
                    "session_id": "test_session"
                }
            },
            {
                "content": "Conteúdo do documento 2",
                "metadata": {
                    "id": "doc2",
                    "tenant_id": "test_tenant",
                    "session_id": "test_session"
                }
            }
        ]
    }
    
    # Emitir evento
    await event_bus.emit("DOCUMENTS_RETRIEVED", event_data)
    
    # Aguardar processamento
    await asyncio.sleep(0.2)
    
    # Verificar eventos
    events = event_bus.get_events()
    assert len(events) == 2  # Retrieved + Generated
    
    # Verificar evento de geração
    generated_event = events[1]
    assert generated_event["type"] == "ANSWER_GENERATED"
    assert "answer" in generated_event["data"]
    assert "sources" in generated_event["data"]
    assert "metadata" in generated_event["data"]
    
    # Verificar resposta gerada
    answer = generated_event["data"]["answer"]
    assert event_data["question"] in answer
    assert "2 documentos" in answer
    
    # Verificar fontes
    sources = generated_event["data"]["sources"]
    assert len(sources) == 2
    for source in sources:
        assert "id" in source
        assert "title" in source
        assert "content" in source
    
    # Verificar metadados
    metadata = generated_event["data"]["metadata"]
    assert metadata["model"] == "mock_model"
    assert metadata["confidence"] == 0.95
    
    # Limpar eventos
    event_bus.clear()

@pytest.mark.asyncio
async def test_generation_error_handling():
    """
    Testa o tratamento de erros na geração de respostas.
    """
    # Criar instâncias dos mocks
    event_bus = MockEventBus()
    generator = MockGenerator(delay=0.1)
    
    # Criar handler
    handler = GenerationEventHandler(
        event_bus=event_bus,
        generator=generator
    )
    
    # Inicializar handler
    await handler.initialize()
    
    # Criar evento com dados inválidos
    event_data = {
        "question": None,  # Pergunta inválida
        "documents": [
            {
                "content": "Conteúdo do documento 1",
                "metadata": {
                    "id": "doc1",
                    "tenant_id": "test_tenant",
                    "session_id": "test_session"
                }
            }
        ]
    }
    
    # Emitir evento
    await event_bus.emit("DOCUMENTS_RETRIEVED", event_data)
    
    # Aguardar processamento
    await asyncio.sleep(0.2)
    
    # Verificar que não houve evento de geração
    events = event_bus.get_events()
    assert len(events) == 1  # Apenas o evento de recuperação
    
    # Limpar eventos
    event_bus.clear() 