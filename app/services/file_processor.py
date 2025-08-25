from pathlib import Path
import mimetypes
import shutil
import tempfile

from llama_index.readers.file import (
    DocxReader, PDFReader, PptxReader, MarkdownReader, HTMLTagReader, XMLReader,
    PandasCSVReader, PandasExcelReader, EpubReader, MboxReader, IPYNBReader, ImageReader
)

class FileProcessor:
    MIMETYPE_READERS = {
        'application/pdf': PDFReader(),
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': DocxReader(),
        'application/msword': DocxReader(),
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': PptxReader(),
        'text/plain': MarkdownReader(),
        'text/markdown': MarkdownReader(),
        'text/html': HTMLTagReader(),
        'application/xml': XMLReader(),
        'text/xml': XMLReader(),
        'application/epub+zip': EpubReader(),
        'application/mbox': MboxReader(),
        'application/x-ipynb+json': IPYNBReader(),
        'image/jpeg': ImageReader(),
        'image/png': ImageReader(),
        'image/gif': ImageReader(),
        'image/bmp': ImageReader(),
        'image/tiff': ImageReader(),
        'text/csv': PandasCSVReader(),
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': PandasExcelReader(),
        'application/vnd.ms-excel': PandasExcelReader(),
    }

    def __init__(self, upload_dir: Path):
        self.upload_dir = upload_dir
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def get_reader_for_file(self, file_path: Path):
        mime_type, _ = mimetypes.guess_type(str(file_path))
        reader = self.MIMETYPE_READERS.get(mime_type)
        if reader is None:
            reader = MarkdownReader()
        return reader

    def save_upload(self, file, filename: str) -> Path:
        file_path = self.upload_dir / filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file, buffer)
        return file_path

    def extract_text(self, file_path: Path) -> str:
        # Special handling for .mhtml files
        if file_path.suffix.lower() == ".mhtml":
            import email
            html_content = None
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                msg = email.message_from_file(f)
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/html":
                        html_content = part.get_payload(decode=True)
                        if html_content:
                            html_content = html_content.decode(errors="ignore")
                            break
            if not html_content:
                return ""
            with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp_html:
                tmp_html.write(html_content)
                tmp_html_path = tmp_html.name
            docs = HTMLTagReader().load_data(tmp_html_path)
            import os
            os.unlink(tmp_html_path)
            if not docs or len(docs) == 0:
                return ""
            return docs[0].text
        # Standard file types
        reader = self.get_reader_for_file(file_path)
        docs = reader.load_data(str(file_path))
        # Fallback for .html files if HTML reader fails
        if (not docs or len(docs) == 0) and file_path.suffix.lower() == ".html":
            docs = MarkdownReader().load_data(str(file_path))
        if not docs or len(docs) == 0:
            return ""
        # PDF fallback to OCR if text is not meaningful
        if file_path.suffix.lower() == ".pdf":
            import re
            text = docs[0].text
            alpha_count = len(re.findall(r'[A-Za-z]', text))
            total_count = len(text)
            ratio = alpha_count / total_count if total_count > 0 else 0
            needs_ocr = alpha_count < 50 or ratio < 0.2 or "/gid" in text
            if needs_ocr:
                try:
                    import pytesseract
                    from pdf2image import convert_from_path
                    ocr_text = ""
                    images = convert_from_path(str(file_path))
                    for img in images:
                        ocr_text += pytesseract.image_to_string(img) + "\n"
                    ocr_alpha_count = len(re.findall(r'[A-Za-z]', ocr_text))
                    if ocr_alpha_count > alpha_count:
                        return ocr_text
                except Exception:
                    pass
            return text
        # XML: extract all text content from XML tree
        elif file_path.suffix.lower() in [".xml"]:
            import xml.etree.ElementTree as ET
            try:
                tree = ET.parse(str(file_path))
                root = tree.getroot()
                def get_all_text(elem):
                    text = elem.text or ""
                    for child in elem:
                        text += get_all_text(child)
                    if elem.tail:
                        text += elem.tail
                    return text
                return get_all_text(root)
            except Exception:
                return docs[0].text
        else:
            return docs[0].text
