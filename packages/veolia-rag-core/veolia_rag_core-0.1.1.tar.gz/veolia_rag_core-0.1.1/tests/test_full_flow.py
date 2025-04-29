"""
Teste do fluxo completo do sistema.
"""

import pytest
import asyncio
from datetime import datetime
from typing import Dict, Any, List

from tests.mocks.mock_auth import MockUserManager, MockSessionManager, MockTenantManager
from tests.mocks.mock_event_bus import MockEventBus
from tests.mocks.mock_extractor import MockExtractor
from tests.mocks.mock_embedding import MockEmbedding
from tests.mocks.mock_vectorstore import MockVectorStore
from tests.mocks.mock_retriever import MockRetriever
from tests.mocks.mock_generator import MockGenerator

from security.auth_event_handler import AuthEventHandler
from extraction.extraction_event_handler import ExtractionEventHandler
from embedding.embedding_event_handler import EmbeddingEventHandler
from vectorstore.vectorstore_event_handler import VectorStoreEventHandler
from retriever.retrieval_event_handler import RetrievalEventHandler
from generation.generation_event_handler import GenerationEventHandler


@pytest.mark.asyncio
async def test_full_system_flow():
    """
    Testa o fluxo completo do sistema:
    1. Upload de documento
    2. Extração
    3. Embedding
    4. Armazenamento
    5. Pergunta → Resposta
    """
    # Criar instâncias dos mocks
    event_bus = MockEventBus()

    # Criar managers de autenticação
    user_manager = MockUserManager()
    session_manager = MockSessionManager(user_manager)
    tenant_manager = MockTenantManager()

    # Criar handlers
    auth_handler = AuthEventHandler(
        event_bus=event_bus,
        user_manager=user_manager,
        session_manager=session_manager,
        tenant_manager=tenant_manager,
    )

    extractor = MockExtractor(delay=0.1)
    extraction_handler = ExtractionEventHandler(
        event_bus=event_bus, extractor=extractor
    )

    embedding = MockEmbedding(delay=0.1)
    embedding_handler = EmbeddingEventHandler(event_bus=event_bus, embedding=embedding)

    vectorstore = MockVectorStore(delay=0.1)
    vectorstore_handler = VectorStoreEventHandler(
        event_bus=event_bus, vectorstore=vectorstore
    )

    retriever = MockRetriever(delay=0.1)
    retrieval_handler = RetrievalEventHandler(event_bus=event_bus, retriever=retriever)

    generator = MockGenerator(delay=0.1)
    generation_handler = GenerationEventHandler(
        event_bus=event_bus, generator=generator
    )

    # Inicializar handlers
    await auth_handler.initialize()
    await extraction_handler.initialize()
    await embedding_handler.initialize()
    await vectorstore_handler.initialize()
    await retrieval_handler.initialize()
    await generation_handler.initialize()

    # Criar tenant e usuário
    await tenant_manager.create_tenant(tenant_id="tenant1", name="Tenant Teste")

    await user_manager.create_user(
        user_id="user1",
        tenant_id="tenant1",
        email="user1@test.com",
        name="Usuário Teste",
    )

    # Criar sessão
    session = await session_manager.create_session(user_id="user1", tenant_id="tenant1")

    # 1. Upload de documento
    upload_event = {
        "data": {
            "file_path": "test.pdf",
            "metadata": {"title": "Documento Teste", "author": "Autor Teste"},
        },
        "auth": {"token": session["token"]},
    }

    await event_bus.emit("DOCUMENT_UPLOADED", upload_event)

    # Aguardar processamento
    await asyncio.sleep(1.0)

    # Verificar eventos
    events = event_bus.get_events()
    assert len(events) == 6  # Upload + Extract + Embed + Store + Question + Answer

    # Verificar sequência de eventos
    event_types = [event["type"] for event in events]
    assert event_types == [
        "DOCUMENT_UPLOADED",
        "DOCUMENT_EXTRACTED",
        "EMBEDDING_CREATED",
        "VECTOR_STORED",
        "QUESTION_RECEIVED",
        "ANSWER_GENERATED",
    ]

    # Verificar dados do documento extraído
    extracted_event = events[1]
    assert extracted_event["type"] == "DOCUMENT_EXTRACTED"
    assert "content" in extracted_event["data"]
    assert "metadata" in extracted_event["data"]
    assert extracted_event["data"]["metadata"]["title"] == "Documento Teste"

    # Verificar embedding
    embedding_event = events[2]
    assert embedding_event["type"] == "EMBEDDING_CREATED"
    assert "embedding" in embedding_event["data"]
    assert len(embedding_event["data"]["embedding"]) == 1536

    # Verificar armazenamento
    storage_event = events[3]
    assert storage_event["type"] == "VECTOR_STORED"
    assert "vector_id" in storage_event["data"]

    # Verificar pergunta
    question_event = events[4]
    assert question_event["type"] == "QUESTION_RECEIVED"
    assert "question" in question_event["data"]
    assert "documents" in question_event["data"]

    # Verificar resposta
    answer_event = events[5]
    assert answer_event["type"] == "ANSWER_GENERATED"
    assert "answer" in answer_event["data"]
    assert "sources" in answer_event["data"]
    assert "metadata" in answer_event["data"]

    # Verificar contexto de autenticação em todos os eventos
    for event in events:
        assert "auth" in event
        assert event["auth"]["user_id"] == "user1"
        assert event["auth"]["tenant_id"] == "tenant1"
        assert event["auth"]["session_id"] == session["session_id"]

    # Limpar eventos
    event_bus.clear()
