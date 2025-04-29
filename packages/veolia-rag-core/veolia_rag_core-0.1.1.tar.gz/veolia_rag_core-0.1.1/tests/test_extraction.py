"""
Testes para a camada de extração.
"""

import pytest
import asyncio
from datetime import datetime
from typing import Dict, Any

from tests.mocks.mock_extractor import MockExtractor
from tests.mocks.mock_event_bus import MockEventBus
from extraction.extraction_event_handler import ExtractionEventHandler
from core.document import Document


@pytest.mark.asyncio
async def test_mock_extractor():
    """
    Testa o comportamento do MockExtractor.
    """
    # Criar instância do mock
    extractor = MockExtractor(delay=0.1)

    # Testar extração
    file_path = "test.pdf"
    metadata = {
        "tenant_id": "test_tenant",
        "session_id": "test_session",
        "uploaded_at": datetime.utcnow().isoformat(),
    }

    # Extrair documento
    documents = await extractor.extract(file_path, metadata)

    # Verificar resultados
    assert len(documents) == 1
    assert isinstance(documents[0], Document)
    assert "test.pdf" in documents[0].content
    assert documents[0].metadata["tenant_id"] == "test_tenant"
    assert documents[0].metadata["session_id"] == "test_session"
    assert "extracted_at" in documents[0].metadata

    # Verificar contagem de processamentos
    assert extractor.get_processed_files()[file_path] == 1


@pytest.mark.asyncio
async def test_extraction_event_handler():
    """
    Testa o comportamento do ExtractionEventHandler.
    """
    # Criar instâncias dos mocks
    event_bus = MockEventBus()
    extractor = MockExtractor(delay=0.1)

    # Criar handler
    handler = ExtractionEventHandler(event_bus=event_bus, extractor=extractor)

    # Inicializar handler
    await handler.initialize()

    # Criar evento de upload
    event_data = {
        "file_path": "test.pdf",
        "metadata": {
            "tenant_id": "test_tenant",
            "session_id": "test_session",
            "uploaded_at": datetime.utcnow().isoformat(),
        },
    }

    # Emitir evento
    await event_bus.emit("DOCUMENT_UPLOADED", event_data)

    # Aguardar processamento
    await asyncio.sleep(0.2)

    # Verificar eventos
    events = event_bus.get_events()
    assert len(events) == 2  # Upload + Extracted

    # Verificar evento de extração
    extracted_event = events[1]
    assert extracted_event["type"] == "DOCUMENT_EXTRACTED"
    assert "documents" in extracted_event["data"]
    assert len(extracted_event["data"]["documents"]) == 1

    # Verificar documento extraído
    doc = extracted_event["data"]["documents"][0]
    assert "test.pdf" in doc["content"]
    assert doc["metadata"]["tenant_id"] == "test_tenant"
    assert doc["metadata"]["session_id"] == "test_session"

    # Limpar eventos
    event_bus.clear()


@pytest.mark.asyncio
async def test_extraction_error_handling():
    """
    Testa o tratamento de erros na extração.
    """
    # Criar instâncias dos mocks
    event_bus = MockEventBus()
    extractor = MockExtractor(delay=0.1)

    # Criar handler
    handler = ExtractionEventHandler(event_bus=event_bus, extractor=extractor)

    # Inicializar handler
    await handler.initialize()

    # Criar evento com dados inválidos
    event_data = {
        "file_path": None,  # Caminho inválido
        "metadata": {"tenant_id": "test_tenant", "session_id": "test_session"},
    }

    # Emitir evento
    await event_bus.emit("DOCUMENT_UPLOADED", event_data)

    # Aguardar processamento
    await asyncio.sleep(0.2)

    # Verificar que não houve evento de extração
    events = event_bus.get_events()
    assert len(events) == 1  # Apenas o evento de upload

    # Limpar eventos
    event_bus.clear()
