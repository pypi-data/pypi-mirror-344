# 🧠 RAG Core

Sistema modular de RAG (Retrieval Augmented Generation) desenvolvido para ser reutilizável e escalável, com suporte a múltiplos tenants e diferentes provedores de LLM.

## 🌟 Características

- ✨ **Arquitetura Event-Driven**: Baseada em Kafka para processamento assíncrono
- 🔄 **Pipeline Modular**: Extração → Embedding → Armazenamento → Recuperação → Geração
- 🔌 **Múltiplos Provedores**: Suporte a diferentes LLMs (Gemini, OpenAI, Mistral, etc.)
- 📊 **Vector Store**: Integração com Qdrant para busca semântica
- 📦 **MongoDB**: Armazenamento de documentos e metadados
- 🔐 **Multi-tenant**: Isolamento completo entre diferentes clientes
- 📈 **Observabilidade**: OpenTelemetry para traces, métricas e logs

## 🚀 Começando

### Pré-requisitos

- Python 3.10+
- Docker e Docker Compose
- Make (opcional, mas recomendado)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/rag_core.git
cd rag_core
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Copie o arquivo de exemplo de variáveis de ambiente:
```bash
cp .env.example .env
```

5. Inicie os serviços com Docker Compose:
```bash
docker-compose up -d
```

## 🔧 Configuração

Edite o arquivo `.env` com suas configurações:

```env
# Kafka
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333

# MongoDB
MONGODB_URI=mongodb://localhost:27017

# LLM Providers
GEMINI_API_KEY=sua_chave_aqui
OPENAI_API_KEY=sua_chave_aqui
```

## 📚 Como Usar

### Uso Básico

```python
from rag_core.core_orchestrator import CoreOrchestrator
from rag_core.events.event_bus import EventBus
from rag_core.events.event_types import DOCUMENT_UPLOADED, QUESTION_RECEIVED

# Inicializa o core
core = CoreOrchestrator()
core.start()

# Obtém instância do EventBus
event_bus = EventBus()

# Envia um documento
event_bus.emit(DOCUMENT_UPLOADED, {
    "tenant_id": "empresa_x",
    "session_id": "sessao_123",
    "file_path": "/caminho/para/documento.pdf",
    "file_type": "pdf"
})

# Faz uma pergunta
event_bus.emit(QUESTION_RECEIVED, {
    "tenant_id": "empresa_x",
    "session_id": "sessao_123",
    "question": "Qual é o procedimento para...?",
    "metadata": {
        "language": "pt-BR",
        "max_tokens": 500
    }
})
```

### Usando como Dependência

Instale o pacote via pip:

```bash
pip install rag_core
```

Ou adicione ao seu `requirements.txt`:

```
rag_core @ git+https://github.com/seu-usuario/rag_core.git
```

## 🏗️ Arquitetura

O sistema é dividido em camadas:

1. **Extraction Layer**: Extrai texto de diferentes tipos de documento
2. **Embedding Layer**: Gera embeddings usando diferentes provedores
3. **Vector Store Layer**: Armazena e recupera vetores
4. **Retrieval Layer**: Realiza busca semântica
5. **Generation Layer**: Gera respostas usando LLMs

## 🔄 Eventos

O sistema usa os seguintes eventos principais:

- `DOCUMENT_UPLOADED`: Documento enviado para processamento
- `DOCUMENT_EXTRACTED`: Texto extraído do documento
- `EMBEDDING_CREATED`: Embedding gerado
- `VECTOR_STORED`: Vetor armazenado no Qdrant
- `QUESTION_RECEIVED`: Pergunta recebida
- `DOCUMENTS_RETRIEVED`: Documentos relevantes recuperados
- `ANSWER_GENERATED`: Resposta final gerada

## 🧪 Testes

Execute os testes com:

```bash
pytest
```

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🤝 Contribuindo

1. Faça o fork do projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para suporte, abra uma issue no GitHub ou entre em contato via [email]. 