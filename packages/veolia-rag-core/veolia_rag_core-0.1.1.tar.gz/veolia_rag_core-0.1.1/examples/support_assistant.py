"""
Exemplo de Assistente de Suporte usando RAG Core.
Este exemplo demonstra como criar um assistente que:
1. Carrega documentos de suporte
2. Processa perguntas de usuários
3. Mantém histórico de conversas
4. Gerencia múltiplos tenants
"""

import os
import time
import json
from typing import Dict, Any, List
import logging
from datetime import datetime

from rag_core.core_orchestrator import CoreOrchestrator
from rag_core.events.event_bus import EventBus
from rag_core.events.event_types import (
    DOCUMENT_UPLOADED,
    QUESTION_RECEIVED,
    ANSWER_GENERATED,
    VECTOR_STORED,
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SupportAssistant:
    def __init__(self, tenant_id: str):
        """
        Inicializa o assistente de suporte para um tenant específico

        Args:
            tenant_id: Identificador único do tenant
        """
        self.tenant_id = tenant_id
        self.core = CoreOrchestrator()
        self.event_bus = EventBus()

        # Registra handlers para eventos
        self.event_bus.subscribe(ANSWER_GENERATED, self._handle_answer)
        self.event_bus.subscribe(VECTOR_STORED, self._handle_vector_stored)

        # Controle de estado
        self.conversations: Dict[str, List[Dict[str, str]]] = {}
        self.documents_processed = 0

    def start(self):
        """Inicia o core e prepara para processar eventos"""
        logger.info(f"Iniciando SupportAssistant para tenant {self.tenant_id}")
        self.core.start()

    def load_knowledge_base(self, docs_dir: str):
        """
        Carrega documentos da base de conhecimento

        Args:
            docs_dir: Diretório contendo os documentos
        """
        if not os.path.exists(docs_dir):
            raise FileNotFoundError(f"Diretório não encontrado: {docs_dir}")

        for file_name in os.listdir(docs_dir):
            if file_name.endswith((".pdf", ".txt", ".csv", ".docx")):
                file_path = os.path.join(docs_dir, file_name)
                self.upload_document(file_path)
                time.sleep(1)  # Pequena pausa entre uploads

    def upload_document(self, file_path: str, session_id: str = None):
        """
        Faz upload de um documento para processamento

        Args:
            file_path: Caminho do arquivo
            session_id: ID da sessão (opcional)
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        file_type = os.path.splitext(file_path)[1].lower().replace(".", "")

        if not session_id:
            session_id = f"doc_{int(time.time())}"

        event_data = {
            "tenant_id": self.tenant_id,
            "session_id": session_id,
            "file_path": os.path.abspath(file_path),
            "file_type": file_type,
            "metadata": {
                "source": "support_assistant",
                "upload_timestamp": datetime.now().isoformat(),
                "category": "knowledge_base",
            },
        }

        logger.info(f"Enviando documento para processamento: {file_path}")
        self.event_bus.emit(DOCUMENT_UPLOADED, event_data)

    def ask_question(self, question: str, user_id: str, session_id: str = None):
        """
        Envia uma pergunta para ser respondida

        Args:
            question: Pergunta do usuário
            user_id: ID do usuário
            session_id: ID da sessão (opcional)
        """
        if not session_id:
            session_id = f"conv_{int(time.time())}"

        # Inicializa histórico da conversa se necessário
        if session_id not in self.conversations:
            self.conversations[session_id] = []

        # Adiciona pergunta ao histórico
        self.conversations[session_id].append(
            {
                "role": "user",
                "content": question,
                "timestamp": datetime.now().isoformat(),
            }
        )

        event_data = {
            "tenant_id": self.tenant_id,
            "session_id": session_id,
            "user_id": user_id,
            "question": question,
            "metadata": {
                "source": "support_assistant",
                "language": "pt-BR",
                "timestamp": datetime.now().isoformat(),
                "conversation_history": self.conversations[session_id],
            },
        }

        logger.info(f"Enviando pergunta do usuário {user_id}: {question}")
        self.event_bus.emit(QUESTION_RECEIVED, event_data)

    def _handle_vector_stored(self, event_data: Dict[str, Any]):
        """Callback para quando um documento é processado e armazenado"""
        self.documents_processed += 1
        logger.info(
            f"Documento processado e armazenado com sucesso! Total: {self.documents_processed}"
        )

    def _handle_answer(self, event_data: Dict[str, Any]):
        """Callback para quando uma resposta é gerada"""
        session_id = event_data.get("session_id")
        answer = event_data.get("answer", "")
        sources = event_data.get("sources", [])

        # Adiciona resposta ao histórico
        if session_id in self.conversations:
            self.conversations[session_id].append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                    "timestamp": datetime.now().isoformat(),
                }
            )

        logger.info("\n=== Resposta Recebida ===")
        logger.info(f"Resposta: {answer}")
        logger.info("\nFontes utilizadas:")
        for source in sources:
            logger.info(f"- {source}")
        logger.info("=====================")

    def get_conversation_history(self, session_id: str) -> List[Dict[str, str]]:
        """
        Retorna o histórico de uma conversa específica

        Args:
            session_id: ID da sessão

        Returns:
            Lista de mensagens da conversa
        """
        return self.conversations.get(session_id, [])


def main():
    # Criar e iniciar o assistente para um tenant
    assistant = SupportAssistant(tenant_id="empresa_x")
    assistant.start()

    # Carregar base de conhecimento
    docs_dir = "examples/docs"
    if os.path.exists(docs_dir):
        assistant.load_knowledge_base(docs_dir)

    # Exemplo de interação com usuário
    user_id = "usuario_123"
    session_id = f"conv_{int(time.time())}"

    perguntas = [
        "Quais são os principais procedimentos de segurança?",
        "Como funciona o processo de atendimento ao cliente?",
        "Quais são as políticas de reembolso?",
    ]

    for pergunta in perguntas:
        assistant.ask_question(pergunta, user_id, session_id)
        time.sleep(2)  # Pequena pausa entre perguntas

    # Mostrar histórico da conversa
    print("\n=== Histórico da Conversa ===")
    for msg in assistant.get_conversation_history(session_id):
        print(f"\n[{msg['timestamp']}] {msg['role'].upper()}:")
        print(msg["content"])
        if "sources" in msg:
            print("\nFontes:", msg["sources"])

    # Mantém a aplicação rodando para receber respostas
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Encerrando assistente...")


if __name__ == "__main__":
    main()
