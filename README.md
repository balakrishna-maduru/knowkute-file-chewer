# Knowkute File Chewer

Knowkute File Chewer is a modular, document processing and querying system powered by open-source Large Language Models (LLMs) and embeddings. It enables users to upload, parse, chunk, embed, and search across a wide variety of document types (PDF, Word, Excel, PowerPoint, and plain text) using a FastAPI-based backend. All processing and storage are performed locally, ensuring data privacy and full control over your files and models.

## Key Features

- **Local-Only LLMs & Embeddings:** All models are downloaded and run locally—no data leaves your machine.
- **Multi-Format Support:** Handles PDF, DOCX, PPTX, XLSX, and TXT files.
- **Modular Architecture:** Clean separation of API routes, business logic, pipelines, and data models for easy maintenance and extensibility.
- **Efficient Chunking & Embedding:** Documents are parsed, cleaned, split into meaningful chunks, and embedded for fast vector search.
- **FastAPI REST API:** Upload files, trigger processing, and query your data via simple HTTP endpoints.
- **Extensible Storage:** Chunks and embeddings are stored locally (JSON/SQLite) but can be extended to use databases or distributed storage.
- **Health & Status Endpoints:** Built-in endpoints for monitoring and debugging.

## Typical Workflow

1. **Upload:** User uploads a document via the API.
2. **Chewing:** The system parses, cleans, splits, and embeds the document, storing the results locally.
3. **Query:** User submits a query; the system embeds the query and performs a vector search to return the most relevant document chunks.

## Use Cases

- Private document search and Q&A
- Knowledge base construction
- Local research assistant
- Secure enterprise document processing

## Why Knowkute File Chewer?

- **Privacy:** No cloud dependencies—your data and models stay on your machine.
- **Flexibility:** Easily add new file types, models, or storage backends.
- **Performance:** Optimized for fast, local vector search and retrieval.

---

See the design document for detailed architecture and component responsibilities.
