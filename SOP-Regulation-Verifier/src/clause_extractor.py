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
    """
    raw: Either a string or a dict with key "text".
    Returns The extracted string.
    """
    if isinstance(raw, str):
        return raw
    if isinstance(raw, dict) and "text" in raw:
        return raw["text"]
    return str(raw)


def _is_noise(txt: str) -> bool:
    """
    Heuristic to detect unhelpful fragments.
    Fewer than MIN_ALPHA letters.
    MAX_NONALPHA_RATIO of chars are non-letters.
    """
    letters = sum(ch.isalpha() for ch in txt)
    non_alpha_ratio = 1 - (letters / max(len(txt), 1))
    return letters < MIN_ALPHA or non_alpha_ratio > MAX_NONALPHA_RATIO


def _split_on_headings(text: str) -> List[Dict[str, str]]:
    """
    Split text into clauses at lines matching HEADINGS.
    
    Returns a list of {"clause_id": heading, "text": clause}.
    """
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
    """
    Fallback: split on double newlines, discard noise.
    """
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    return [
        {"clause_id": f"P{idx}", "text": para}
        for idx, para in enumerate(paras, 1)
        if not _is_noise(para)
    ]


def extract_clauses(raw: Any) -> List[Dict[str, str]]:
    """
    Main API: return a list of clauses with ids/text.
    
    raw: SOP or regulatory doc content (string or dict).
    Returns List of {"clause_id": ..., "text": ...}.
    """
    txt = _coerce_to_text(raw)
    clauses = _split_on_headings(txt)
    if len(clauses) <= 1:  
        clauses = _split_on_paragraphs(txt)
    return clauses or [{"clause_id": "P0", "text": txt}]
