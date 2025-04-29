"""
Testes para o VeoliaSecureGPTGenerator.
"""

import pytest
import asyncio
from typing import List
from langchain.schema import Document
from generation.veolia_secure_gpt_generator import VeoliaSecureGPTGenerator
from tests.mocks.mock_veolia_secure_gpt import MockVeoliaSecureGPTGenerator


@pytest.mark.asyncio
async def test_veolia_secure_gpt_initialization():
    """Testa a inicialização do VeoliaSecureGPTGenerator."""
    # Teste com API key válida
    generator = VeoliaSecureGPTGenerator(
        model_name="test-model", temperature=0.7, api_key="test-api-key"
    )
    await generator.initialize()
    assert generator._initialized is True

    # Teste com API key inválida
    with pytest.raises(ValueError):
        VeoliaSecureGPTGenerator(model_name="test-model", temperature=0.7, api_key=None)

    # Teste com temperatura inválida
    with pytest.raises(ValueError):
        VeoliaSecureGPTGenerator(
            model_name="test-model", temperature=1.5, api_key="test-api-key"
        )


@pytest.mark.asyncio
async def test_veolia_secure_gpt_generation():
    """Testa a geração de respostas com o VeoliaSecureGPTGenerator."""
    # Criar documentos de teste
    documents = [
        Document(
            page_content="Este é um documento de teste 1", metadata={"source": "doc1"}
        ),
        Document(
            page_content="Este é um documento de teste 2", metadata={"source": "doc2"}
        ),
    ]

    # Testar geração com mock
    mock_generator = MockVeoliaSecureGPTGenerator()
    await mock_generator.initialize()

    # Gerar resposta
    response = await mock_generator.generate(
        question="Qual é o conteúdo dos documentos?",
        documents=documents,
        context={"tenant_id": "test-tenant"},
    )

    # Verificar resposta
    assert "answer" in response
    assert "sources" in response
    assert "confidence" in response
    assert "metadata" in response
    assert response["sources"] == ["doc1", "doc2"]
    assert response["confidence"] == 0.9
    assert response["metadata"]["tenant_id"] == "test-tenant"
    assert mock_generator.generation_count == 1

    # Testar geração com documentos vazios
    with pytest.raises(ValueError):
        await mock_generator.generate(
            question="Qual é o conteúdo dos documentos?",
            documents=[],
            context={"tenant_id": "test-tenant"},
        )

    # Testar geração com pergunta vazia
    with pytest.raises(ValueError):
        await mock_generator.generate(
            question="", documents=documents, context={"tenant_id": "test-tenant"}
        )


@pytest.mark.asyncio
async def test_veolia_secure_gpt_context_manager():
    """Testa o uso do VeoliaSecureGPTGenerator como context manager."""
    async with MockVeoliaSecureGPTGenerator() as generator:
        assert generator._initialized is True

        # Gerar resposta
        documents = [
            Document(page_content="Documento de teste", metadata={"source": "test"})
        ]

        response = await generator.generate(
            question="Qual é o conteúdo do documento?", documents=documents
        )

        assert "answer" in response
        assert generator.generation_count == 1

    # Verificar se o gerador foi fechado corretamente
    assert generator._initialized is False
    assert generator.client is None


@pytest.mark.asyncio
async def test_veolia_secure_gpt_error_handling():
    """Testa o tratamento de erros do VeoliaSecureGPTGenerator."""
    generator = MockVeoliaSecureGPTGenerator()

    # Testar geração sem inicialização
    with pytest.raises(RuntimeError):
        await generator.generate(
            question="Teste", documents=[Document(page_content="Teste")]
        )

    # Testar geração com documentos inválidos
    await generator.initialize()
    with pytest.raises(ValueError):
        await generator.generate(
            question="Teste", documents=["documento inválido"]  # type: ignore
        )

    # Testar geração com documentos sem conteúdo
    with pytest.raises(ValueError):
        await generator.generate(
            question="Teste", documents=[Document(page_content="")]
        )
