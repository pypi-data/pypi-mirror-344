"""
Testes para a camada de autenticação.
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from tests.mocks.mock_auth import MockUserManager, MockSessionManager, MockTenantManager
from tests.mocks.mock_event_bus import MockEventBus
from security.auth_event_handler import AuthEventHandler

@pytest.mark.asyncio
async def test_mock_user_manager():
    """
    Testa o comportamento do MockUserManager.
    """
    # Criar instância do mock
    user_manager = MockUserManager()
    
    # Criar usuário
    user = await user_manager.create_user(
        user_id="user1",
        tenant_id="tenant1",
        email="user1@test.com",
        name="Usuário Teste",
        permissions=["read", "write"]
    )
    
    # Verificar usuário criado
    assert user["user_id"] == "user1"
    assert user["tenant_id"] == "tenant1"
    assert user["email"] == "user1@test.com"
    assert user["name"] == "Usuário Teste"
    assert user["permissions"] == ["read", "write"]
    assert user["is_active"] is True
    
    # Verificar recuperação
    retrieved_user = await user_manager.get_user("user1")
    assert retrieved_user == user
    
    # Verificar listagem
    users = user_manager.get_users()
    assert len(users) == 1
    assert users["user1"] == user

@pytest.mark.asyncio
async def test_mock_session_manager():
    """
    Testa o comportamento do MockSessionManager.
    """
    # Criar instâncias dos mocks
    user_manager = MockUserManager()
    session_manager = MockSessionManager(user_manager)
    
    # Criar usuário
    await user_manager.create_user(
        user_id="user1",
        tenant_id="tenant1",
        email="user1@test.com",
        name="Usuário Teste"
    )
    
    # Criar sessão
    session = await session_manager.create_session(
        user_id="user1",
        tenant_id="tenant1"
    )
    
    # Verificar sessão criada
    assert session["user_id"] == "user1"
    assert session["tenant_id"] == "tenant1"
    assert "token" in session
    assert "session_id" in session
    assert session["is_active"] is True
    
    # Verificar validação
    validated_session = await session_manager.validate_session(session["token"])
    assert validated_session == session
    
    # Verificar listagem
    sessions = session_manager.get_sessions()
    assert len(sessions) == 1
    assert sessions[session["session_id"]] == session

@pytest.mark.asyncio
async def test_mock_tenant_manager():
    """
    Testa o comportamento do MockTenantManager.
    """
    # Criar instância do mock
    tenant_manager = MockTenantManager()
    
    # Criar tenant
    tenant = await tenant_manager.create_tenant(
        tenant_id="tenant1",
        name="Tenant Teste",
        description="Descrição do tenant"
    )
    
    # Verificar tenant criado
    assert tenant["tenant_id"] == "tenant1"
    assert tenant["name"] == "Tenant Teste"
    assert tenant["description"] == "Descrição do tenant"
    assert tenant["is_active"] is True
    assert "config" in tenant
    
    # Verificar recuperação
    retrieved_tenant = await tenant_manager.get_tenant("tenant1")
    assert retrieved_tenant == tenant
    
    # Verificar listagem
    tenants = tenant_manager.get_tenants()
    assert len(tenants) == 1
    assert tenants["tenant1"] == tenant

@pytest.mark.asyncio
async def test_auth_event_handler():
    """
    Testa o comportamento do AuthEventHandler.
    """
    # Criar instâncias dos mocks
    event_bus = MockEventBus()
    user_manager = MockUserManager()
    session_manager = MockSessionManager(user_manager)
    tenant_manager = MockTenantManager()
    
    # Criar handler
    handler = AuthEventHandler(
        event_bus=event_bus,
        user_manager=user_manager,
        session_manager=session_manager,
        tenant_manager=tenant_manager
    )
    
    # Inicializar handler
    await handler.initialize()
    
    # Criar tenant
    await tenant_manager.create_tenant(
        tenant_id="tenant1",
        name="Tenant Teste"
    )
    
    # Criar usuário
    await user_manager.create_user(
        user_id="user1",
        tenant_id="tenant1",
        email="user1@test.com",
        name="Usuário Teste"
    )
    
    # Criar sessão
    session = await session_manager.create_session(
        user_id="user1",
        tenant_id="tenant1"
    )
    
    # Criar evento com contexto de autenticação
    event_data = {
        "data": {
            "file_path": "test.pdf",
            "metadata": {}
        },
        "auth": {
            "token": session["token"]
        }
    }
    
    # Emitir evento
    await event_bus.emit("DOCUMENT_UPLOADED", event_data)
    
    # Aguardar processamento
    await asyncio.sleep(0.2)
    
    # Verificar eventos
    events = event_bus.get_events()
    assert len(events) == 2  # Upload + Processed
    
    # Verificar evento processado
    processed_event = events[1]
    assert processed_event["type"] == "DOCUMENT_UPLOADED"
    assert "data" in processed_event
    assert "auth" in processed_event
    
    # Verificar contexto de autenticação
    auth = processed_event["auth"]
    assert auth["user_id"] == "user1"
    assert auth["tenant_id"] == "tenant1"
    assert auth["session_id"] == session["session_id"]
    
    # Limpar eventos
    event_bus.clear()

@pytest.mark.asyncio
async def test_auth_error_handling():
    """
    Testa o tratamento de erros na autenticação.
    """
    # Criar instâncias dos mocks
    event_bus = MockEventBus()
    user_manager = MockUserManager()
    session_manager = MockSessionManager(user_manager)
    tenant_manager = MockTenantManager()
    
    # Criar handler
    handler = AuthEventHandler(
        event_bus=event_bus,
        user_manager=user_manager,
        session_manager=session_manager,
        tenant_manager=tenant_manager
    )
    
    # Inicializar handler
    await handler.initialize()
    
    # Criar evento com token inválido
    event_data = {
        "data": {
            "file_path": "test.pdf",
            "metadata": {}
        },
        "auth": {
            "token": "token_invalido"
        }
    }
    
    # Emitir evento
    await event_bus.emit("DOCUMENT_UPLOADED", event_data)
    
    # Aguardar processamento
    await asyncio.sleep(0.2)
    
    # Verificar que não houve evento processado
    events = event_bus.get_events()
    assert len(events) == 1  # Apenas o evento de upload
    
    # Limpar eventos
    event_bus.clear() 