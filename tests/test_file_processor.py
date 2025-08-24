import pytest
from app.services.file_processor import FileProcessor
from pathlib import Path

@pytest.mark.parametrize("filename,expected_text", [
    ("Dolat_Capital_KPIT_Technologies_Q2FY25_Result_Update.pdf", "KPIT"),
    ("Modern nursing resume.docx", "nursing"),
    ("baseline-assessment-tool-excel-196658893.xls", "Assessment"),
    ("AWS-Slides.pptx", "AWS"),
    ("Knowkute_File_Chewer.txt", "Knowkute")
])
def test_file_extraction(filename, expected_text):
    resource_path = Path(__file__).parent / "resources" / filename
    processor = FileProcessor()
    text = processor.extract_text(resource_path)
    assert expected_text.lower() in text.lower()
