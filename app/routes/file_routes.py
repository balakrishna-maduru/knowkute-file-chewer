

from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import sys

router = APIRouter()
UPLOAD_DIR = Path("data/uploads")

def ensure_models_loaded():
    try:
        import sentence_transformers
    except ImportError:
        import subprocess
        subprocess.run([sys.executable, "-m", "models.download_models"], check=True)

from app.services.file_processor import FileProcessor
file_processor = FileProcessor(UPLOAD_DIR)

@router.post("/files/upload")
def upload_file(file: UploadFile = File(...)):
    ensure_models_loaded()
    file_path = file_processor.save_upload(file.file, file.filename)
    text = file_processor.extract_text(file_path)
    if not text:
        return {"error": f"Could not extract text from {file.filename}"}
    return {"file_id": file.filename, "text": text}

