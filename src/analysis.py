"""
Defines logic for generating human-readable compliance suggestions
by comparing SOP excerpts to regulatory clauses via Claude LLM.
"""
from typing import List, Dict
import os
import json
import re
import textwrap

from langchain_anthropic import ChatAnthropic

def _short(txt: str, n: int = 160) -> str:
    clean = " ".join(txt.split())
    return clean if len(clean) <= n else clean[:n].rsplit(" ", 1)[0] + "…"

JSON_RE = re.compile(r"\{.*\}", re.DOTALL)


def suggest_adjustments(
    section: Dict[str, str],
    clauses: List[Dict[str, str]],
    llm_temperature: float = 0.2,
) -> List[Dict[str, str]]:
    """
    For each candidate clause, ask Claude to:
      1. Summarize the key difference (≤40 words)
      2. Provide 2–3 actionable bullet edits
    Parses the first JSON object in the response.
    """
    use_llm = bool(os.getenv("ANTHROPIC_API_KEY"))
    claude = (
        ChatAnthropic(
            model_name="claude-3-5-haiku-20241022",
            temperature=llm_temperature,
            max_tokens=1024,
        )
        if use_llm
        else None
    )

    sop_excerpt = _short(section["text"])
    output: List[Dict[str, str]] = []

    for c in clauses:
        reg_clause_full = c["text"].strip()
        prompt = textwrap.dedent(f"""
            You are a senior compliance analyst.

            REGULATORY CLAUSE (from {c['source']} | id {c['clause_id']}):
            \"\"\"{reg_clause_full}\"\"\"

            SOP EXCERPT:
            \"\"\"{section['text']}\"\"\"

            1. Write ONE clear sentence (≤40 words) explaining how the SOP diverges from this clause.
            2. Provide 2–3 bullet edits for the SOP to achieve compliance.

            Return JSON ONLY in this schema:
            {{
              "difference": "<sentence>",
              "suggestion": "- bullet1\\n- bullet2"
            }}
        """).strip()

        if claude:
            raw_msg = claude.invoke(prompt)
            raw = raw_msg.content
            match = JSON_RE.search(raw)
            if match:
                try:
                    data = json.loads(match.group(0))
                    diff = data.get("difference", "No difference provided.")
                    sugg = data.get("suggestion", "- No suggestion provided.")
                except Exception:
                    diff = "Claude JSON parsing failed."
                    sugg = "- Review and align SOP section."
            else:
                diff = "Claude did not return JSON."
                sugg = "- Review and align SOP section."
        else:
            diff = "LLM disabled; manual review needed."
            sugg = "- Review and align SOP section."

        output.append({
            "section_id": section["section_id"],
            "sop_excerpt": sop_excerpt,
            "clause_id": c["clause_id"],
            "reg_clause": _short(reg_clause_full, 180),
            "source": c["source"],
            "difference": diff,
            "suggestion": sugg,
        })

    return output
