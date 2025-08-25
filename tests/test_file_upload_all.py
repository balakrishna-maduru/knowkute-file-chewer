import pytest
from fastapi.testclient import TestClient
from app.main import app
from pathlib import Path

client = TestClient(app)

INPUT_DIR = Path(__file__).parent / "resources" / "input"
OUTPUT_DIR = Path(__file__).parent / "resources" / "output"

import json
import shutil
if OUTPUT_DIR.exists():
    for f in OUTPUT_DIR.glob("*.json"):
        f.unlink()
else:
    OUTPUT_DIR.mkdir(exist_ok=True)

ALL_FILES = [f for f in INPUT_DIR.iterdir() if f.is_file()]

@pytest.mark.parametrize("file_path", ALL_FILES)
def test_file_upload_and_store_response(file_path):
    with open(file_path, "rb") as f:
        response = client.post(
            "/files/upload",
            files={"file": (file_path.name, f, "application/octet-stream")}
        )
    output_file = OUTPUT_DIR / f"{file_path.name}.json"
    # Save as formatted JSON
    try:
        data = response.json()
    except Exception:
        data = response.text
    with open(output_file, "w", encoding="utf-8") as out:
        if isinstance(data, dict):
            json.dump(data, out, indent=2, ensure_ascii=False)
        else:
            out.write(data)
    assert response.status_code == 200
