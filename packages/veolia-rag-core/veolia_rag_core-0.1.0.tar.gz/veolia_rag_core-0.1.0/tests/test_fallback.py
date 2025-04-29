"""
Testes para o FallbackGenerator.
"""

import pytest
import asyncio
from langchain.schema import Document
from tests.mocks.mock_fallback import MockFallbackGenerator

@pytest.mark.asyncio
async def test_fallback_generator_initialization():
    """Testa a inicialização do gerador de fallback."""
    generator = MockFallbackGenerator(
        gemini_model_name="test-gemini",
        veolia_model_name="test-veolia",
        temperature=0.5
    )
    
    assert not generator._initialized
    await generator.initialize()
    assert generator._initialized
    assert generator.gemini_generator.model_name == "test-gemini"
    assert generator.veolia_generator.model_name == "test-veolia"
    assert generator.temperature == 0.5
    assert generator.fallback_count == 0

@pytest.mark.asyncio
async def test_fallback_generator_successful_gemini():
    """Testa o caso de sucesso com o Gemini."""
    generator = MockFallbackGenerator()
    await generator.initialize()
    
    # Criar documentos de teste
    documents = [
        Document(
            page_content="Conteúdo do documento 1",
            metadata={"source": "doc1.pdf"}
        )
    ]
    
    # Testar geração sem falha
    question = "Qual é a resposta?"
    response = await generator.generate(question, documents)
    
    assert response["metadata"]["generator"] == "mock-gemini"
    assert "fallback" not in response["metadata"]
    assert generator.fallback_count == 0

@pytest.mark.asyncio
async def test_fallback_generator_fallback_to_veolia():
    """Testa o fallback para o VeoliaSecureGPT."""
    generator = MockFallbackGenerator()
    await generator.initialize()
    
    # Configurar falha do Gemini
    generator.set_gemini_failure(True)
    
    # Criar documentos de teste
    documents = [
        Document(
            page_content="Conteúdo do documento 1",
            metadata={"source": "doc1.pdf"}
        )
    ]
    
    # Testar geração com falha
    question = "Qual é a resposta?"
    response = await generator.generate(question, documents)
    
    assert response["metadata"]["generator"] == "mock-veolia"
    assert response["metadata"]["fallback"] is True
    assert generator.fallback_count == 1

@pytest.mark.asyncio
async def test_fallback_generator_context_preservation():
    """Testa a preservação do contexto entre geradores."""
    generator = MockFallbackGenerator()
    await generator.initialize()
    
    # Criar documentos e contexto
    documents = [Document(page_content="Teste")]
    context = {
        "tenant_id": "test-tenant",
        "session_id": "test-session",
        "user_id": "test-user"
    }
    
    # Testar com Gemini
    response = await generator.generate("Pergunta", documents, context)
    assert response["metadata"]["tenant_id"] == "test-tenant"
    assert response["metadata"]["session_id"] == "test-session"
    assert response["metadata"]["user_id"] == "test-user"
    
    # Testar com fallback
    generator.set_gemini_failure(True)
    response = await generator.generate("Pergunta", documents, context)
    assert response["metadata"]["tenant_id"] == "test-tenant"
    assert response["metadata"]["session_id"] == "test-session"
    assert response["metadata"]["user_id"] == "test-user"

@pytest.mark.asyncio
async def test_fallback_generator_error_handling():
    """Testa o tratamento de erros no gerador de fallback."""
    generator = MockFallbackGenerator()
    await generator.initialize()
    
    # Testar com documentos inválidos
    with pytest.raises(ValueError):
        await generator.generate("Pergunta", [])
        
    # Testar com pergunta inválida
    with pytest.raises(ValueError):
        await generator.generate("", [Document(page_content="test")]) 