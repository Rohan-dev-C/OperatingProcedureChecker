"""

Generates a grouped Markdown compliance report from
analysis suggestions and SOP sections.

"""

from typing import List, Dict
from collections import defaultdict
import os


def generate_markdown_report(sections: List[Dict[str, str]],
                             suggestions: List[Dict[str, str]],
                             path: str = "compliance_report.md"):
    """
    Write `compliance_report.md` summarizing
    each SOP section and the relevant clauses
    and their differences, suggestions, source filenames.
    
    Creates the output directory if needed.
    """
    grouped = defaultdict(list)
    for s in suggestions:
        grouped[s["section_id"]].append(s)

    lines = ["# Compliance Analysis Report\n"]
    for sec in sections:
        sid, title = sec["section_id"], sec.get("title", "")
        lines.append(f"\n## Section {sid}: {title}\n")

        if sid not in grouped:
            lines.append("_No relevant clauses found._")
            continue

        for s in grouped[sid]:
            lines += [
                f"- **Clause {s['clause_id']}** *(from `{s['source']}`)*",
                f"  - **Regulatory Text:** {s['reg_clause']}",
                f"  - **SOP Excerpt:** {s['sop_excerpt']}",
                f"  - **Difference:** {s['difference']}",
                f"  - **Suggested Edit(s):**",
                *(f"    {ln}" for ln in s['suggestion'].splitlines()),
                ""
            ]

    if os.path.dirname(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Report saved to: {path}")
