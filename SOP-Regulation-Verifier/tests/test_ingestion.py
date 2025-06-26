import os
import tempfile
from src.ingestion import load_pdf_text, load_docx_text
from docx import Document

def test_load_pdf_text():
    text = load_pdf_text("data/regulatory_docs/REG-29_CFR_1910_119.pdf")
    assert isinstance(text, str)
    assert len(text) > 100  

def test_load_docx_text(tmp_path):
    p = tmp_path / "sample.docx"
    doc = Document()
    doc.add_paragraph("Hello, world!")
    doc.save(p)
    text = load_docx_text(str(p))
    assert "Hello, world!" in text
