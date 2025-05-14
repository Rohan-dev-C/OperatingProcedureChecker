from src.clause_extractor import extract_clauses

def test_extract_clauses_simple():
    text = """
    Section 1.1 Introduction
    This is the intro.

    Section 1.2 Scope
    This is the scope.
    """
    clauses = extract_clauses(text)
    assert len(clauses) == 2
    assert clauses[0]["clause_id"] == "1.1"
    assert "intro" in clauses[0]["text"]
