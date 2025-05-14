from src.report_generator import generate_markdown_report

def test_generate_markdown_report():
    sections = [{"section_id": "1", "title": "Intro", "text": "SOP content"}]
    suggestions = [
        {"section_id": "1", "clause_id": "1.1", "suggestion": "- Add detail"}
    ]
    md = generate_markdown_report(sections, suggestions)
    assert "# Compliance Analysis Report" in md
    assert "## Section 1: Intro" in md
    assert "- **Clause 1.1**" in md
