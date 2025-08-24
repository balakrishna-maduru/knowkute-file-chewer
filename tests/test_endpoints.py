import pytest
from fastapi.testclient import TestClient
from app.main import app
from pathlib import Path

client = TestClient(app)

@pytest.mark.parametrize("filename", [
    "sample.pdf",
    "sample.docx",
    "sample.xlsx",
    "sample.pptx",
    "sample.txt"
])
def test_upload_file(filename):
    resource_path = Path(__file__).parent / "resources" / filename
    with open(resource_path, "rb") as f:
        response = client.post("/files/upload", files={"file": (filename, f)})
    assert response.status_code == 200
    assert "file_id" in response.json()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
