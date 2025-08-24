# Project Description

Knowkute File Chewer is a modular document processing and querying system powered by open-source Large Language Models (LLMs) and embeddings. It allows users to upload, parse, chunk, embed, and search across a wide variety of document types (PDF, Word, Excel, PowerPoint, and plain text) using a FastAPI-based backend. All processing and storage are performed locally, ensuring data privacy and full control over your files and models. The architecture is designed for extensibility, maintainability, and privacy, making it suitable for private document search, knowledge base construction, and secure enterprise use cases.

# Project Design: knowkute – File Chewer

This document outlines the architecture and design for the `knowkute-file-chewer` project, a local-first RAG (Retrieval-Augmented Generation) system.

## Project Structure

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
│── requirements.txt                # Python dependencies
│── README.md                       # Project documentation

---

## 🔑 Key Design Principles

*   **Asynchronous Processing**: File ingestion ("chewing") is a long-running operation. It will be executed as a background task using FastAPI's `BackgroundTasks` to avoid blocking the API and provide immediate feedback to the user.
*   **Dependency Injection**: The application will heavily leverage FastAPI's dependency injection system. This will be used to provide services, pipelines, and configuration settings to the API routes, promoting clean, decoupled, and easily testable code.
*   **Configuration Management**: All configuration (file paths, model names, chunking parameters) will be managed in `app/config.py` using Pydantic's `BaseSettings`. This allows for easy configuration via environment variables, `.env` files, or code defaults.
*   **Modularity and Separation of Concerns**: The structure separates API definitions (`routes`), business logic (`services`), high-level workflows (`pipelines`), and data structures (`schemas`), making the codebase easier to understand, maintain, and extend.

---

## 🧩 Component Responsibilities

#### 1. Schemas (`app/schemas/`)
*   **`file_schema.py`** → Defines the schema for file metadata, including `id`, `name`, `path`, and a `status` enum (e.g., `UPLOADED`, `PROCESSING`, `COMPLETED`, `FAILED`).
*   **`chunk_schema.py`** → Schema for file chunks, including `id`, `file_id`, `text`, and a reference to its embedding.
*   **`query_schema.py`** → Defines the request and response formats for queries.

#### 2. Routes (`app/routes/`)
*   **`file_routes.py`** → Endpoints for:
    *   `POST /files/upload`: Upload a file. Returns a file ID and triggers the chewing pipeline in the background.
    *   `GET /files/{file_id}/status`: Retrieve the processing status of a file.
*   **`query_routes.py`** → `POST /query`: Endpoint for submitting a query against the processed files and receiving a generated answer.
*   **`health_routes.py`** → Health check endpoints like `/health` to verify service status and model availability.

#### 3. Services (`app/services/`)
*   **`file_processor.py`** → Detects file type (PDF, DOCX, PPTX, XLSX, TXT) and uses appropriate libraries to extract raw text.
*   **`chunk_manager.py`** → Uses helpers from `utils.text_utils.py` to clean text, split it into sentences, and group them into chunks of a configurable size with overlap.
*   **`embedding_service.py`** → Loads the local sentence-transformer model and generates vector embeddings for text chunks using `llama-index`.
*   **`query_service.py`** → Executes a vector similarity search against the stored embeddings to find the most relevant context chunks for a given query.
*   **`generation_service.py`** → Loads the local generative LLM (e.g., LLaMA GGUF) and uses it to synthesize a final, human-readable answer based on the user's query and the retrieved context chunks.
*   **`storage_service.py`** → Manages the persistence layer. It configures and provides access to the `llama-index` `StorageContext`, which abstracts the underlying vector store (e.g., ChromaDB, FAISS) located in `/data/index_store/`.

#### 4. Pipelines (`app/pipelines/`)
*   **`chew_pipeline.py`** → Orchestrates the entire ingestion process: `File Processor` → `Chunk Manager` → `Embedding Service` → `Storage Service`.
*   **`query_pipeline.py`** → Orchestrates the full RAG query flow: Embeds the user query, uses `Query Service` to retrieve context, uses `Generation Service` to create a final answer, and returns the response.

#### 5. Utils (`app/utils/`)
*   **`logger.py`** → Configurable structured logging setup for the application.
*   **`file_utils.py`** → Helper functions for safely saving and managing uploaded files.
*   **`text_utils.py`** → Pure, stateless functions for text manipulation like cleaning special characters and splitting text into sentences.

#### 6. Models Directory (`models/`)
*   Stores all local LLM and embedding models to keep them separate from application code.
*   Includes a script `download_models.py` that uses the `huggingface_hub` library to programmatically fetch and save required models from Hugging Face.
*   Example:
    ```
    models/
        ggml-llama-7b.bin
        all-MiniLM-L6-v2/
        download_models.py
    ```

---

## � Workflow

#### 1. File Ingestion (The "Chew" Pipeline)
1.  **Upload**: A user sends a `POST` request to `/files/upload` with a file.
2.  **Save & Enqueue**: The file is saved to `/data/uploads/`. A new file record is created in the database/metadata store with a `status` of `UPLOADED`. The `chew_pipeline` is triggered as a background task.
3.  **Process**: The pipeline updates the file `status` to `PROCESSING`.
    *   **Parse**: `file_processor.py` extracts raw text from the file.
    *   **Chunk**: `chunk_manager.py` cleans and splits the text into semantic chunks.
    *   **Embed**: `embedding_service.py` converts each chunk into a vector embedding.
    *   **Store**: `storage_service.py` persists the chunks and their embeddings into the vector store in `/data/index_store/`.
4.  **Complete**: The file `status` is updated to `COMPLETED`. If any step fails, it's marked as `FAILED` with an error message.

#### 2. Querying (The RAG Pipeline)
1.  **Query**: A user sends a `POST` request to `/query` with a question.
2.  **Retrieve**: The `query_pipeline` is triggered.
    *   The user's query is embedded using the same `embedding_service`.
    *   `query_service` performs a vector similarity search in the index to find the top-N most relevant text chunks.
3.  **Generate**:
    *   The retrieved chunks (context) and the original query are passed to the `generation_service`.
    *   The local LLM generates a synthesized answer based on the provided context.
4.  **Respond**: The generated answer and source chunks are returned to the user.

---

👉 **This design ensures:**
*   **Reusability** → Services and pipelines are modular and can be composed differently.
*   **Extensibility** → Easy to add support for new file types, vector stores, or LLMs by adding or replacing service implementations.
*   **Local-First** → All models and data remain on the local machine, ensuring privacy and offline capability.
*   **Clear Separation of Concerns** → Routes (API), Services (logic), Pipelines (orchestration), and Schemas (data) are cleanly separated.
*   **Scalability** → The use of background tasks for ingestion allows the API to remain responsive under load.
