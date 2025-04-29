"""
Testes de integração para o fluxo completo do sistema.
"""

import pytest
import asyncio
from langchain.schema import Document
from tests.mocks.mock_event_bus import MockEventBus
from tests.mocks.mock_extractor import MockExtractor
from tests.mocks.mock_embedding import MockEmbedding
from tests.mocks.mock_vectorstore import MockVectorStore
from tests.mocks.mock_retriever import MockRetriever
from tests.mocks.mock_veolia_secure_gpt import MockVeoliaSecureGPTGenerator
from tests.mocks.mock_auth import MockUserManager, MockSessionManager, MockTenantManager
from events.event_types import (
    DOCUMENT_UPLOADED,
    DOCUMENT_EXTRACTED,
    EMBEDDING_CREATED,
    VECTOR_STORED,
    QUESTION_RECEIVED,
    DOCUMENTS_RETRIEVED,
    ANSWER_GENERATED
)

@pytest.mark.asyncio
async def test_full_system_flow():
    """Testa o fluxo completo do sistema, do upload até a geração da resposta."""
    # Inicializar componentes
    event_bus = MockEventBus()
    extractor = MockExtractor()
    embedding = MockEmbedding()
    vectorstore = MockVectorStore()
    retriever = MockRetriever()
    generator = MockVeoliaSecureGPTGenerator()
    
    # Inicializar managers de autenticação
    user_manager = MockUserManager()
    session_manager = MockSessionManager()
    tenant_manager = MockTenantManager()
    
    # Criar tenant e usuário de teste
    tenant = await tenant_manager.create_tenant("Test Tenant")
    user = await user_manager.create_user(
        tenant_id=tenant.tenant_id,
        email="test@example.com",
        name="Test User"
    )
    session = await session_manager.create_session(user.user_id, tenant.tenant_id)
    
    # Criar contexto de autenticação
    auth_context = {
        "tenant_id": tenant.tenant_id,
        "session_id": session.session_id,
        "user_id": user.user_id
    }
    
    # 1. Upload de documento
    upload_event = {
        "file_path": "test.pdf",
        "file_type": "pdf",
        "content": "Conteúdo do documento de teste",
        **auth_context
    }
    
    await event_bus.emit(DOCUMENT_UPLOADED, upload_event)
    await asyncio.sleep(0.1)
    
    # Verificar extração
    events = event_bus.get_emitted_events()
    assert len(events) == 1
    assert events[0]["event_type"] == DOCUMENT_EXTRACTED
    assert events[0]["data"]["content"] == upload_event["content"]
    
    # 2. Criação de embedding
    await asyncio.sleep(0.1)
    events = event_bus.get_emitted_events()
    assert len(events) == 2
    assert events[1]["event_type"] == EMBEDDING_CREATED
    assert "embedding" in events[1]["data"]
    
    # 3. Armazenamento de vetor
    await asyncio.sleep(0.1)
    events = event_bus.get_emitted_events()
    assert len(events) == 3
    assert events[2]["event_type"] == VECTOR_STORED
    assert "vector_id" in events[2]["data"]
    
    # 4. Recebimento de pergunta
    question_event = {
        "question": "Qual é o conteúdo do documento?",
        **auth_context
    }
    
    await event_bus.emit(QUESTION_RECEIVED, question_event)
    await asyncio.sleep(0.1)
    
    # Verificar recuperação de documentos
    events = event_bus.get_emitted_events()
    assert len(events) == 4
    assert events[3]["event_type"] == DOCUMENTS_RETRIEVED
    assert "documents" in events[3]["data"]
    
    # 5. Geração de resposta
    await asyncio.sleep(0.1)
    events = event_bus.get_emitted_events()
    assert len(events) == 5
    assert events[4]["event_type"] == ANSWER_GENERATED
    
    # Verificar resposta final
    response = events[4]["data"]
    assert "answer" in response
    assert "sources" in response
    assert response["metadata"]["tenant_id"] == tenant.tenant_id
    assert response["metadata"]["session_id"] == session.session_id
    assert response["metadata"]["user_id"] == user.user_id

@pytest.mark.asyncio
async def test_error_handling_in_full_flow():
    """Testa o tratamento de erros no fluxo completo."""
    event_bus = MockEventBus()
    extractor = MockExtractor()
    embedding = MockEmbedding()
    vectorstore = MockVectorStore()
    retriever = MockRetriever()
    generator = MockVeoliaSecureGPTGenerator()
    
    # 1. Upload de documento inválido
    invalid_upload = {
        "file_path": "test.pdf",
        "file_type": "invalid",
        "content": "",
        "tenant_id": "invalid-tenant",
        "session_id": "invalid-session"
    }
    
    await event_bus.emit(DOCUMENT_UPLOADED, invalid_upload)
    await asyncio.sleep(0.1)
    
    # Verificar que nenhum evento foi processado
    events = event_bus.get_emitted_events()
    assert len(events) == 0
    
    # 2. Pergunta sem contexto de autenticação
    invalid_question = {
        "question": "Teste",
        "tenant_id": "invalid-tenant",
        "session_id": "invalid-session"
    }
    
    await event_bus.emit(QUESTION_RECEIVED, invalid_question)
    await asyncio.sleep(0.1)
    
    # Verificar que nenhum evento foi processado
    events = event_bus.get_emitted_events()
    assert len(events) == 0

@pytest.mark.asyncio
async def test_concurrent_requests():
    """Testa o processamento de múltiplas requisições simultâneas."""
    event_bus = MockEventBus()
    extractor = MockExtractor()
    embedding = MockEmbedding()
    vectorstore = MockVectorStore()
    retriever = MockRetriever()
    generator = MockVeoliaSecureGPTGenerator()
    
    # Criar múltiplas requisições
    requests = [
        {
            "question": f"Pergunta {i}",
            "tenant_id": f"tenant-{i}",
            "session_id": f"session-{i}",
            "user_id": f"user-{i}"
        } for i in range(3)
    ]
    
    # Emitir eventos simultaneamente
    tasks = [event_bus.emit(QUESTION_RECEIVED, req) for req in requests]
    await asyncio.gather(*tasks)
    
    # Aguardar processamento
    await asyncio.sleep(0.2)
    
    # Verificar que todas as requisições foram processadas
    events = event_bus.get_emitted_events()
    assert len(events) == 3  # 3 respostas geradas
    
    # Verificar que cada resposta tem o contexto correto
    for i, event in enumerate(events):
        assert event["event_type"] == ANSWER_GENERATED
        assert event["data"]["metadata"]["tenant_id"] == f"tenant-{i}"
        assert event["data"]["metadata"]["session_id"] == f"session-{i}"
        assert event["data"]["metadata"]["user_id"] == f"user-{i}" 