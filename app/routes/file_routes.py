from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from pathlib import Path
from app.services.file_processor import FileProcessor
from app.services.chunk_manager import ChunkManager
import shutil

router = APIRouter()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/files/upload")
def upload_file(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    processor = FileProcessor()
    chunker = ChunkManager()
    text = processor.extract_text(file_path)
    chunks = chunker.create_chunks(text)
    return {"file_id": file.filename, "num_chunks": len(chunks), "chunks": chunks}

