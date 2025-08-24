from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from pathlib import Path
from app.services.file_processor import FileProcessor
from app.services.chunk_manager import ChunkManager
from app.services.embedding_service import EmbeddingService
from app.services.query_service import QueryService
import shutil

router = APIRouter()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/files/upload")
def upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    if background_tasks:
        background_tasks.add_task(process_file, file_path)
    return {"file_id": file.filename, "status": "PROCESSING"}

def process_file(file_path: Path):
    processor = FileProcessor()
    chunker = ChunkManager()
    embedder = EmbeddingService()
    query_service = QueryService()
    text = processor.extract_text(file_path)
    chunks = chunker.create_chunks(text)
    embeddings = [embedder.embed_text(chunk) for chunk in chunks]
    # Here you would store chunks and embeddings in your vector store
    # For demo, just print
    print(f"Processed {file_path.name}: {len(chunks)} chunks")
