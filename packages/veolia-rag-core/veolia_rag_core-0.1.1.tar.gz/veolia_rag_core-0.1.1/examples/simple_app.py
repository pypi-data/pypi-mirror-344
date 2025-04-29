"""
Exemplo simples de uso do RAG Core para processar documentos e responder perguntas.
Este exemplo demonstra:
1. Inicialização do core
2. Upload de documentos
3. Realização de perguntas
4. Tratamento de eventos e respostas
"""

import os
import time
from typing import Dict, Any
import logging

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


class SimpleApp:
    def __init__(self):
        # Inicializa o core
        self.core = CoreOrchestrator()
        self.event_bus = EventBus()

        # Registra handlers para eventos de resposta
        self.event_bus.subscribe(ANSWER_GENERATED, self._handle_answer)
        self.event_bus.subscribe(VECTOR_STORED, self._handle_vector_stored)

        # Controle de estado
        self.documents_processed = 0
        self.answers_received = 0

    def start(self):
        """Inicia o core e prepara para processar eventos"""
        logger.info("Iniciando SimpleApp...")
        self.core.start()

    def upload_document(
        self, file_path: str, tenant_id: str = "demo", session_id: str = None
    ) -> None:
        """
        Faz upload de um documento para processamento

        Args:
            file_path: Caminho do arquivo a ser processado
            tenant_id: ID do tenant (default: "demo")
            session_id: ID da sessão (opcional)
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        # Determina o tipo do arquivo pela extensão
        file_type = os.path.splitext(file_path)[1].lower().replace(".", "")

        # Usa timestamp como session_id se não fornecido
        if not session_id:
            session_id = f"session_{int(time.time())}"

        event_data = {
            "tenant_id": tenant_id,
            "session_id": session_id,
            "file_path": os.path.abspath(file_path),
            "file_type": file_type,
            "metadata": {"source": "simple_app", "upload_timestamp": time.time()},
        }

        logger.info(f"Enviando documento para processamento: {file_path}")
        self.event_bus.emit(DOCUMENT_UPLOADED, event_data)

    def ask_question(
        self, question: str, tenant_id: str = "demo", session_id: str = None
    ) -> None:
        """
        Envia uma pergunta para ser respondida

        Args:
            question: Pergunta a ser respondida
            tenant_id: ID do tenant (default: "demo")
            session_id: ID da sessão (opcional)
        """
        if not session_id:
            session_id = f"session_{int(time.time())}"

        event_data = {
            "tenant_id": tenant_id,
            "session_id": session_id,
            "question": question,
            "metadata": {
                "source": "simple_app",
                "language": "pt-BR",
                "timestamp": time.time(),
            },
        }

        logger.info(f"Enviando pergunta: {question}")
        self.event_bus.emit(QUESTION_RECEIVED, event_data)

    def _handle_vector_stored(self, event_data: Dict[str, Any]) -> None:
        """Callback para quando um documento é processado e armazenado"""
        self.documents_processed += 1
        logger.info(
            f"Documento processado e armazenado com sucesso! Total: {self.documents_processed}"
        )

    def _handle_answer(self, event_data: Dict[str, Any]) -> None:
        """Callback para quando uma resposta é gerada"""
        self.answers_received += 1
        answer = event_data.get("answer", "")
        sources = event_data.get("sources", [])

        logger.info("\n=== Resposta Recebida ===")
        logger.info(f"Resposta: {answer}")
        logger.info("\nFontes utilizadas:")
        for source in sources:
            logger.info(f"- {source}")
        logger.info("=====================")


def main():
    # Criar e iniciar a aplicação
    app = SimpleApp()
    app.start()

    # Exemplo: processar alguns documentos
    docs_dir = "examples/docs"
    if os.path.exists(docs_dir):
        for file_name in os.listdir(docs_dir):
            if file_name.endswith((".pdf", ".txt", ".csv")):
                file_path = os.path.join(docs_dir, file_name)
                app.upload_document(file_path)
                # Pequena pausa entre uploads
                time.sleep(1)

    # Exemplo: fazer algumas perguntas
    perguntas = [
        "Quais são os principais procedimentos de segurança?",
        "Como funciona o processo de atendimento ao cliente?",
        "Quais são as políticas de reembolso?",
    ]

    for pergunta in perguntas:
        app.ask_question(pergunta)
        # Pequena pausa entre perguntas
        time.sleep(2)

    # Mantém a aplicação rodando para receber respostas
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Encerrando aplicação...")


if __name__ == "__main__":
    main()
