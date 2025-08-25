import pytest
from fastapi.testclient import TestClient
from app.main import app
from pathlib import Path

client = TestClient(app)

TEST_FILES = [
    ("Dolat_Capital_KPIT_Technologies_Q2FY25_Result_Update.pdf", "KPIT"),
    ("AppBody-Sample-English.docx", "Sample Application"),
    ("AWS-Slides.pptx", "AWS"),
    ("Knowkute_File_Chewer.txt", "Knowkute"),
    ("Knowkute File Chewer - Swagger UI.mhtml", "Swagger UI"),
    ("sample.html", "Hello HTML World"),
    ("sample.xml", "Hello XML World"),
]

@pytest.mark.parametrize("filename,expected_text", TEST_FILES)
def test_file_upload_and_chunking(filename, expected_text):
    file_path = Path(__file__).parent / "resources" / "input" / filename
    with open(file_path, "rb") as f:
        response = client.post(
            "/files/upload",
            files={"file": (filename, f, "application/octet-stream")}
        )
    assert response.status_code == 200
    data = response.json()
    assert "chunks" in data
    # Check that at least one chunk contains the expected text
    assert any(expected_text.lower() in chunk.lower() for chunk in data["chunks"])
