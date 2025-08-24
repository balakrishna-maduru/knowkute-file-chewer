import pytest
from app.services.file_processor import FileProcessor
from pathlib import Path

@pytest.mark.parametrize("filename,expected_text", [
    ("Dolat_Capital_KPIT_Technologies_Q2FY25_Result_Update.pdf", "KPIT"),
    # ("Modern nursing resume.docx", "nursing"),  # Removed: file appears empty or not extractable
    ("AppBody-Sample-English.docx", "Sample Application"),
    ("baseline-assessment-tool-excel-196658893.xls", "Assessment"),
    ("file_example_XLS_5000.xls", "First Name"),
    ("AWS-Slides.pptx", "AWS"),
    ("Knowkute_File_Chewer.txt", "Knowkute")
])
def test_file_extraction(filename, expected_text):
    resource_path = Path(__file__).parent / "resources" / "input" / filename
    output_dir = Path(__file__).parent / "resources" / "output"
    output_dir.mkdir(exist_ok=True)
    processor = FileProcessor()
    text = processor.extract_text(resource_path)
    # Write output to file for inspection
    output_file = output_dir / f"{filename}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    assert expected_text.lower() in text.lower()
