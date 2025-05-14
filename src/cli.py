import argparse
from collections import Counter

from src.ingestion import load_documents
from src.clause_extractor import extract_clauses, _coerce_to_text
from src.embeddings import embed_texts
from src.vector_db import VectorDB
from src.retrieval import Retrieval
from src.analysis import suggest_adjustments
from src.report_generator import generate_markdown_report


def run_pipeline(sop_dir: str, regs_dir: str, top_k_per_doc: int = 3) -> None:
    print("Loading SOP and regulatory documents...")
    sop_texts = load_documents(sop_dir)
    reg_texts = load_documents(regs_dir)
    print(f"Loaded {len(sop_texts)} SOP files, {len(reg_texts)} regulatory docs.")

    clause_dicts = []
    for fname, doc in reg_texts.items():
        text = _coerce_to_text(doc)
        for clause in extract_clauses(text):
            clause["source"] = fname
            clause_dicts.append(clause)

    print(f"Extracted {len(clause_dicts)} regulatory clauses.")
    counts = Counter(c["source"] for c in clause_dicts)
    print("Clause count per regulatory file:")
    for src, n in counts.items():
        print(f"  • {src}: {n} clauses")

    vecs = embed_texts([c["text"] for c in clause_dicts])
    db = VectorDB(dim=len(vecs[0]), reset=True)
    db.add(vecs, clause_dicts)
    db.save()
    print("Clause embeddings stored in vector DB.")

    sop_sections = []
    for fname, doc in sop_texts.items():
        sop_sections.append({
            "section_id": fname,
            "title": "Full Document",
            "text": _coerce_to_text(doc)
        })
    print(f"Created {len(sop_sections)} SOP sections.")
    
    retriever = Retrieval(db, top_k_per_doc=top_k_per_doc)
    suggestions = []
    for section in sop_sections:
        initial = retriever.retrieve(section["text"])
        relevant = retriever.filter_relevant(section["text"], initial)
        suggestions.extend(suggest_adjustments(section, relevant))

    print(f"✏️  Generated {len(suggestions)} compliance suggestions.")

    print("Generating markdown report…")
    generate_markdown_report(sop_sections, suggestions, "compliance_report.md")
    print("Report written to: compliance_report.md")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SOP ↔ Regulation compliance pipeline")
    parser.add_argument("sop_dir", help="Directory of SOP PDF/DOCX files")
    parser.add_argument("regs_dir", help="Directory of regulatory PDF/DOCX files")
    parser.add_argument("--top_k_per_doc", type=int, default=3,
                        help="Max similar clauses to pull per regulatory file (default 3)")
    args = parser.parse_args()

    run_pipeline(args.sop_dir, args.regs_dir, args.top_k_per_doc)
