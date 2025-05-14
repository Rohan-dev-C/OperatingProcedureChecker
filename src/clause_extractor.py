"""
Robust clause extraction & cleaning.

If headings like "Section 5.1" exist, split on them. 
Otherwise split on paragraphs, but discard fragments that are
shorter than 30 alphabetic characters or are >40 % non-alpha.
"""

from typing import List, Dict, Any
import re

_HEADING_RE = re.compile(r"(?:Section|Article)\s+(\d+(?:\.\d+)*)", re.IGNORECASE)
MIN_ALPHA = 30           
MAX_NONALPHA_RATIO = 0.4 


def _coerce_to_text(raw: Any) -> str:
    if isinstance(raw, str):
        return raw
    if isinstance(raw, dict) and "text" in raw:
        return raw["text"]
    return str(raw)


def _is_noise(txt: str) -> bool:
    letters = sum(ch.isalpha() for ch in txt)
    non_alpha_ratio = 1 - (letters / max(len(txt), 1))
    return letters < MIN_ALPHA or non_alpha_ratio > MAX_NONALPHA_RATIO


def _split_on_headings(text: str) -> List[Dict[str, str]]:
    out, cur = [], {"clause_id": "Intro", "text": ""}
    for ln in text.splitlines():
        m = _HEADING_RE.match(ln.strip())
        if m:
            if not _is_noise(cur["text"]):
                out.append(cur)
            cur = {"clause_id": m.group(1), "text": ""}
        cur["text"] += ln + "\n"
    if not _is_noise(cur["text"]):
        out.append(cur)
    return out


def _split_on_paragraphs(text: str) -> List[Dict[str, str]]:
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    return [
        {"clause_id": f"P{idx}", "text": para}
        for idx, para in enumerate(paras, 1)
        if not _is_noise(para)
    ]


def extract_clauses(raw: Any) -> List[Dict[str, str]]:
    txt = _coerce_to_text(raw)
    clauses = _split_on_headings(txt)
    if len(clauses) <= 1:  
        clauses = _split_on_paragraphs(txt)
    return clauses or [{"clause_id": "P0", "text": txt}]
