
# Knowkute File Chewer

Knowkute File Chewer is a modular, extensible file extraction system. It allows users to upload and extract plain text from a wide variety of document types (PDF, Word, Excel, PowerPoint, HTML, MHTML, XML, images, and plain text) using a FastAPI-based backend. All processing is performed locally, ensuring data privacy and full control over your files. The architecture is designed for maintainability and privacy, making it suitable for secure enterprise and private use cases.

---


## 🚀 Features

- **Local-Only Processing:** All file parsing and extraction is performed locally—no data leaves your machine.
- **Multi-Format Support:** Handles PDF, DOCX, PPTX, XLSX, HTML, MHTML, XML, images, and TXT files.
- **Modular Architecture:** Clean separation of API routes and business logic for easy maintenance and extensibility.
- **FastAPI REST API:** Upload files and extract plain text via simple HTTP endpoints.
- **Robust Fallbacks:** Includes OCR for PDFs, HTML/MHTML fallback, and XML text extraction.
- **Health & Status Endpoints:** Built-in endpoints for monitoring and debugging.

---


## 🗂️ Project Structure

```
knowkute-file-chewer/
│── models/                         # Pre-downloaded local models and configs
│    ├── download_models.py         # Script to fetch all required models
│    └── <model files/folders>      # Model binaries, configs, tokenizers, etc.
│── app/
│    │── main.py                    # FastAPI app startup, router mounting
│    │── config.py                  # Centralized config (if used)
│    │── __init__.py
│
│    ├── routes/                    # REST API endpoints
│    │    ├── __init__.py
│    │    ├── file_routes.py        # Upload & extract file APIs
│    │    └── health_routes.py      # Healthcheck / status endpoints
│
│    ├── services/                  # File processing logic
│    │    ├── __init__.py
│    │    └── file_processor.py     # File type detection & plain text extraction
│
│── tests/                          # API and integration tests
│    ├── __init__.py
│    ├── test_file_upload_api.py
│    ├── test_file_upload_all.py
│    └── resources/
│         ├── input/                # Test input files
│         └── output/               # Test output files
│
│── data/                           # Uploaded files (runtime)
│    └── uploads/                   # Uploaded raw files
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

### 1. Routes (`app/routes/`)
- `file_routes.py`: 
  - `POST /files/upload`: Upload a file and extract plain text.
- `health_routes.py`: 
  - `/health`: Service health checks.

### 2. Services (`app/services/`)
- `file_processor.py`: Detects file type and extracts plain text from files (PDF, DOCX, PPTX, XLSX, HTML, MHTML, XML, images, TXT, etc.), with robust fallbacks (OCR, HTML/MHTML, XML tree extraction).

### 3. Models Directory (`models/`)
- Stores all local models and configs required for file parsing and extraction.
- `download_models.py`: Script to fetch models if needed.

---

## 📦 Included Models and Artifacts

The `models/` directory contains all the local LLM and embedding models, tokenizers, and configuration files required for file parsing, chunking, and querying. Below is a list of the main files and folders:

- **Model binaries:**
  - `pytorch_model.bin` (PyTorch model)
  - `model.safetensors` (Safetensors format)
  - `model.onnx` (ONNX format)
  - `tf_model.h5` (TensorFlow model)
  - `flax_model.msgpack` (Flax model)
  - `rust_model.ot` (Rust model)
- **Tokenizers and configs:**
  - `tokenizer.json`, `tokenizer_config.json`, `sentencepiece.bpe.model`, `vocab.json`, `vocab.txt`, `merges.txt`, `special_tokens_map.json`
- **Pooling and modules:**
  - `1_Pooling/`, `modules.json`
- **ONNX/OpenVINO:**
  - `onnx/`, `openvino/`
- **Model configs:**
  - `config.json`, `config_sentence_transformers.json`, `data_config.json`, `generation_config.json`, `generation_config_for_summarization.json`, `sentence_bert_config.json`
- **Scripts:**
  - `download_models.py` (script to fetch all required models)
  - `train_script.py`
- **Other:**
  - `.cache/`, `.gitattributes`, `README.md`

> All these files are required for local, private, and robust file processing using LlamaIndex readers. Make sure to run `poetry run python models/download_models.py` after setup to ensure all models are present.

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
poetry run uvicorn app.main:app --reload
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


### 1. File Ingestion
- Upload a file via `POST /files/upload`.
- File is saved and plain text is extracted and returned in the response.

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

## 🖥️ Setup on a New Laptop (from Scratch)

Follow these steps to set up Knowkute File Chewer on a new machine:

### 1. Install Prerequisites
- **Python 3.11**: Download and install from [python.org](https://www.python.org/downloads/).
- **Poetry**: Install via pip:
  ```bash
  pip install poetry
  ```
- **Git**: Download and install from [git-scm.com](https://git-scm.com/downloads).
- **Tesseract OCR** (for PDF OCR fallback):
  - **macOS**: `brew install tesseract`
  - **Ubuntu**: `sudo apt-get install tesseract-ocr`
  - **Windows**: Download from [UB Mannheim builds](https://github.com/UB-Mannheim/tesseract/wiki).

### 2. Clone the Repository
```bash
git clone https://github.com/balakrishna-maduru/knowkute-file-chewer.git
cd knowkute-file-chewer
```

### 3. Install Python Dependencies
```bash
poetry install
```

### 4. Download Required Models
```bash
poetry run python models/download_models.py
```

### 5. Start the API Server
```bash
poetry run uvicorn app.main:app --reload
```
- The API will be available at: http://localhost:8000
- Interactive docs: http://localhost:8000/docs

### 6. (Optional) Run Tests
```bash
poetry run pytest --maxfail=3 --disable-warnings -v
```

### 7. (Optional) Clean Up Unwanted Files and Empty Directories
```bash
find . -type d -empty -delete
```

---

For detailed architecture and component responsibilities, see the design document.
