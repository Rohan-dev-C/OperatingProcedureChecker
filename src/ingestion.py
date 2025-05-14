"""
Loads PDF and DOCX files from a directory and extracts plain text.
"""
from pathlib import Path
from typing import Dict

import pdfminer.high_level
from pdfminer.layout import LAParams
from docx import Document

def _extract_pdf_text(path: Path) -> str:
    """
    Extract all text from a PDF.
    
    path: Path to PDF file.
    Returns Concatenated text from all pages.
    """
    try:
        laparams = LAParams()
        return pdfminer.high_level.extract_text(str(path), laparams=laparams)
    except Exception as e:
        print(f"[Ingestion] Failed to extract PDF {path.name}: {e}")
        return ""


def _extract_docx_text(path: Path) -> str:
    """
    Extract all text from a DOCX.
    path: Path to DOCX file.
    Returns Concatenated text from all paragraphs.
    """
    try:
        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs)
    except Exception as e:
        print(f"[Ingestion] Failed to extract DOCX {path.name}: {e}")
        return ""


def _is_supported(path: Path) -> bool:
    return path.suffix.lower() in {".pdf", ".docx"}


def load_documents(root_dir: str) -> Dict[str, Dict[str, str]]:
    """
    Read all supported files (PDF, DOCX) in `directory`.
    
    
    directory: Path to folder containing docs.
    Returns Dict mapping filename → extracted text.
    """
    root = Path(root_dir).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Directory {root} not found")

    docs: Dict[str, Dict[str, str]] = {}

    for path in root.rglob("*"):
        if not path.is_file() or not _is_supported(path):
            continue

        rel_name = str(path.relative_to(root))
        if path.suffix.lower() == ".pdf":
            text = _extract_pdf_text(path)
        else: 
            text = _extract_docx_text(path)

        docs[rel_name] = {"text": text}

    print(f"[Ingestion] Scanned {len(docs)} supported files under {root_dir}")
    return docs
