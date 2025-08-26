
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

The `models/` directory contains all the local models, tokenizers, and configuration files required for file parsing and extraction. These models are downloaded automatically using the `models/download_models.py` script. Below is a detailed list of the main files and folders, with source URLs and usage notes where applicable:


### Model Binaries
- `pytorch_model.bin` (PyTorch model)
  - **Source:** [Hugging Face](https://huggingface.co/) (see `download_models.py`)
  - **Usage:** Used for local inference with PyTorch backend.
- `model.safetensors` (Safetensors format)
  - **Source:** [Hugging Face](https://huggingface.co/docs/safetensors/index)
  - **Usage:** Secure, fast model loading alternative to PyTorch.
- `model.onnx` (ONNX format)
  - **Source:** [ONNX Model Zoo](https://onnx.ai/)
  - **Usage:** For inference with ONNX Runtime or compatible backends.
- `tf_model.h5` (TensorFlow model)
  - **Source:** [Hugging Face](https://huggingface.co/) or [TensorFlow Hub](https://tfhub.dev/)
  - **Usage:** For TensorFlow-based inference.
- `flax_model.msgpack` (Flax model)
  - **Source:** [Hugging Face](https://huggingface.co/)
  - **Usage:** For JAX/Flax-based inference.
- `rust_model.ot` (Rust model)
  - **Source:** [Hugging Face](https://huggingface.co/)
  - **Usage:** For Rust-based inference (rare, advanced use).


### Tokenizers and Configs
- `tokenizer.json`, `tokenizer_config.json`, `sentencepiece.bpe.model`, `vocab.json`, `vocab.txt`, `merges.txt`, `special_tokens_map.json`
  - **Source:** [Hugging Face](https://huggingface.co/) (model card/tokenizer tab)
  - **Usage:** Required for text preprocessing and tokenization for all model types.


### Pooling and Modules
- `1_Pooling/` (directory), `modules.json`
  - **Source:** [Hugging Face](https://huggingface.co/)
  - **Usage:** Used for pooling layers and module configs in sentence transformers.


### ONNX Models
- `onnx/` (directory)
    - `model.onnx`, `model_O1.onnx`, `model_O2.onnx`, `model_O3.onnx`, `model_O4.onnx`, `model_qint8_arm64.onnx`, `model_qint8_avx512.onnx`, `model_qint8_avx512_vnni.onnx`, `model_quint8_avx2.onnx`
  - **Source:** [ONNX Model Zoo](https://onnx.ai/) or [Hugging Face](https://huggingface.co/)
  - **Usage:** For optimized inference on various hardware (CPU, ARM, AVX, etc.).


### OpenVINO Models
- `openvino/` (directory)
    - `openvino_model.bin`, `openvino_model.xml`, `openvino_model_qint8_quantized.bin`, `openvino_model_qint8_quantized.xml`
  - **Source:** [OpenVINO Model Zoo](https://docs.openvino.ai/latest/omz_models.html)
  - **Usage:** For optimized inference on Intel hardware.


### Model Configs
- `config.json`, `config_sentence_transformers.json`, `data_config.json`, `generation_config.json`, `generation_config_for_summarization.json`, `sentence_bert_config.json`
  - **Source:** [Hugging Face](https://huggingface.co/)
  - **Usage:** Model architecture, generation, and data configs for all supported backends.


### Scripts
- `download_models.py` (script to fetch all required models)
  - **Usage:** Run `poetry run python models/download_models.py` to download all required models and configs from Hugging Face or other sources.
- `train_script.py`
  - **Usage:** (Optional) For advanced users to fine-tune or train models locally.

### Other
- `.cache/` (directory)
- `.gitattributes`
- `README.md`

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
