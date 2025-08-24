
# Knowkute File Chewer

Knowkute File Chewer is a modular document processing and querying system powered by open-source Large Language Models (LLMs) and embeddings. It allows users to upload, parse, chunk, embed, and search across a wide variety of document types (PDF, Word, Excel, PowerPoint, and plain text) using a FastAPI-based backend. All processing and storage are performed locally, ensuring data privacy and full control over your files and models. The architecture is designed for extensibility, maintainability, and privacy, making it suitable for private document search, knowledge base construction, and secure enterprise use cases.

---

## 🚀 Features

- **Local-Only LLMs & Embeddings:** All models are downloaded and run locally—no data leaves your machine.
- **Multi-Format Support:** Handles PDF, DOCX, PPTX, XLSX, and TXT files.
- **Modular Architecture:** Clean separation of API routes, business logic, pipelines, and data models for easy maintenance and extensibility.
- **Efficient Chunking & Embedding:** Documents are parsed, cleaned, split into meaningful chunks, and embedded for fast vector search.
- **FastAPI REST API:** Upload files, trigger processing, and query your data via simple HTTP endpoints.
- **Extensible Storage:** Chunks and embeddings are stored locally (e.g., ChromaDB, FAISS) but can be extended to use databases or distributed storage.
- **Health & Status Endpoints:** Built-in endpoints for monitoring and debugging.
- **Asynchronous Processing:** File ingestion is handled as a background task for responsiveness.

---

## 🗂️ Project Structure

```
knowkute-file-chewer/
│── models/                         # Pre-downloaded local LLMs & Embedding Models
│    ├── download_models.py         # Script to fetch all required models (LLaMA, embeddings, etc.)
│    └── <downloaded-model-folders> # HuggingFace / GGUF / Local model binaries
│── app/
│    │── main.py                    # Entry point (FastAPI app startup, router mounting)
│    │── config.py                  # Centralized config using Pydantic's BaseSettings
│    │── __init__.py
│
│    ├── routes/                    # REST API endpoints
│    │    ├── __init__.py
│    │    ├── file_routes.py        # Upload & process file APIs
│    │    ├── query_routes.py       # Query APIs on processed chunks
│    │    └── health_routes.py      # Healthcheck / status endpoints
│
│    ├── services/                  # Reusable processing & business logic
│    │    ├── __init__.py
│    │    ├── file_processor.py     # File parsing & chunking (PDF, Word, Excel, PPT, etc.)
│    │    ├── chunk_manager.py      # Sentence splitting, chunk creation
│    │    ├── embedding_service.py  # Handles embedding with llama_index + local models
│    │    ├── query_service.py      # Runs queries over stored vectors
│    │    ├── generation_service.py # Generates answers using a local LLM (Generation)
│    │    └── storage_service.py    # Persists chunks/vectors locally (e.g., ChromaDB)
│
│    ├── schemas/                   # Python data models (Pydantic Schemas)
│    │    ├── __init__.py
│    │    ├── file_schema.py         # File metadata schema
│    │    ├── chunk_schema.py        # Chunk schema
│    │    └── query_schema.py        # Query request/response schemas
│
│    ├── utils/                     # Shared utilities
│    │    ├── __init__.py
│    │    ├── logger.py             # Logging config
│    │    ├── file_utils.py         # File save/load helpers
│    │    └── text_utils.py         # Text cleaning, sentence splitting helpers
│
│    └── pipelines/                 # High-level orchestration
│         ├── __init__.py
│         ├── chew_pipeline.py      # Full "File Chewer" pipeline: parse -> chunk -> embed -> store
│         └── query_pipeline.py     # Full query pipeline: load embeddings → query → return result
│
│── scripts/                        
│    ├── run_server.sh              # Run FastAPI app (uvicorn)
│    ├── download_all.sh            # Calls `models/download_models.py` to fetch local models
│    └── test_api.sh                # Curl/Postman test scripts for APIs
│
│── tests/                          # Unit & integration tests
│    ├── __init__.py
│    ├── test_file_processor.py
│    ├── test_chunk_manager.py
│    ├── test_embedding_service.py
│    ├── test_query_service.py
│    └── test_endpoints.py
│
│── data/                           # Temporary files, storage
│    ├── uploads/                   # Uploaded raw files
│    ├── processed/                 # (Optional) Processed intermediate files
│    └── index_store/               # Persisted vector store (e.g., ChromaDB, FAISS)
│
│── .gitignore                      # Git ignore rules
│── README.md                       # Project documentation
│── pyproject.toml                  # Poetry project config
│── poetry.lock                     # Poetry lock file
```

---

## 🔑 Key Design Principles

- **Asynchronous Processing:** File ingestion is a long-running operation, executed as a background task using FastAPI's `BackgroundTasks`.
- **Dependency Injection:** FastAPI's dependency injection system is used for services, pipelines, and configuration.
- **Configuration Management:** All configuration is managed in `app/config.py` using Pydantic's `BaseSettings`.
- **Modularity and Separation of Concerns:** Clear separation between API (`routes`), business logic (`services`), workflows (`pipelines`), and data structures (`schemas`).

---

## 🧩 Component Responsibilities

### 1. Schemas (`app/schemas/`)
- `file_schema.py`: File metadata schema (id, name, path, status).
- `chunk_schema.py`: Chunk schema (id, file_id, text, embedding).
- `query_schema.py`: Query request/response schemas.

### 2. Routes (`app/routes/`)
- `file_routes.py`: 
	- `POST /files/upload`: Upload a file and trigger the chewing pipeline.
	- `GET /files/{file_id}/status`: Retrieve file processing status.
- `query_routes.py`: 
	- `POST /query`: Submit a query and receive a generated answer.
- `health_routes.py`: 
	- `/health`: Service and model health checks.

### 3. Services (`app/services/`)
- `file_processor.py`: Detects file type and extracts raw text.
- `chunk_manager.py`: Cleans and splits text into chunks.
- `embedding_service.py`: Generates vector embeddings for text chunks.
- `query_service.py`: Vector similarity search for relevant context.
- `generation_service.py`: Synthesizes answers using a local LLM.
- `storage_service.py`: Manages persistence of chunks and embeddings.

### 4. Pipelines (`app/pipelines/`)
- `chew_pipeline.py`: Orchestrates file ingestion (parse → chunk → embed → store).
- `query_pipeline.py`: Orchestrates query flow (embed → retrieve → generate → respond).

### 5. Utils (`app/utils/`)
- `logger.py`: Structured logging.
- `file_utils.py`: File save/load helpers.
- `text_utils.py`: Text cleaning and sentence splitting.

### 6. Models Directory (`models/`)
- Stores all local LLM and embedding models.
- `download_models.py`: Script to fetch models from Hugging Face.

---

## 🛠️ Setup & Usage

### Prerequisites

- Python 3.11
- Poetry (for dependency management)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/balakrishna-maduru/knowkute-file-chewer.git
cd knowkute-file-chewer

# Install dependencies
poetry install

# (Optional) Download models
poetry run python models/download_models.py
```

### Running the Server

```bash
poetry run bash scripts/run_server.sh
```

The API will be available at `http://localhost:8000`.

### API Documentation

- Interactive docs: `http://localhost:8000/docs`
- OpenAPI schema: `http://localhost:8000/openapi.json`

---

## 🧪 Testing

```bash
poetry run pytest
```

---

## 📝 Workflow

### 1. File Ingestion (The "Chew" Pipeline)
- Upload a file via `POST /files/upload`.
- File is saved, status tracked, and processed in the background (parse, chunk, embed, store).
- Status can be checked via `GET /files/{file_id}/status`.

### 2. Querying (The RAG Pipeline)
- Submit a query via `POST /query`.
- System retrieves relevant chunks and generates an answer using the local LLM.

---

## 🤝 Contributing

1. Fork the repo and create your branch.
2. Commit your changes.
3. Push to the branch and open a Pull Request.

---

## 📄 License

[MIT License](LICENSE) (add a LICENSE file as needed)

---

## 🙏 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [LlamaIndex](https://github.com/jerryjliu/llama_index)
- [Sentence Transformers](https://www.sbert.net/)
- [Hugging Face](https://huggingface.co/)

---

For detailed architecture and component responsibilities, see the design document.
