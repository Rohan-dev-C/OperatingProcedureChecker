import re
from typing import List, Dict


def parse_sop(text: str) -> List[Dict[str, str]]:
    """
    Split SOP text into sections based on numeric headings (e.g., '1. Purpose').
    Returns a list of dicts: [{"section_id": "1", "title": "Purpose", "text": ...}, ...]
    """
    sections = []
    pattern = re.compile(r'^(\d+)\.\s+(.*)$', re.MULTILINE)
    matches = list(pattern.finditer(text))
    for idx, m in enumerate(matches):
        sec_id = m.group(1)
        title = m.group(2).strip()
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        sections.append({
            "section_id": sec_id,
            "title": title,
            "text": body,
        })
    return sections