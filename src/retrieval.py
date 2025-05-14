from typing import List, Dict, Any
import os, json, numpy as np
from collections import defaultdict
from langchain_anthropic import ChatAnthropic
from anthropic import BadRequestError
from src.embeddings import embed_texts
from src.vector_db import VectorDB


class Retrieval:
    """
    • Pull up to `top_k_per_doc` nearest vectors *per* regulatory file.
    • Ask Claude to pick the truly relevant ones.
    """

    def __init__(self,
                 db: VectorDB,
                 top_k_per_doc: int = 3,
                 temperature: float = 0.2,
                 **_ignored):
        self.db = db
        self.top_k_per_doc = top_k_per_doc
        self.llm = None
        if os.getenv("ANTHROPIC_API_KEY"):
            try:
                self.llm = ChatAnthropic(
                    model_name="claude-3-5-haiku-20241022",
                    temperature=temperature,
                    max_tokens=1024,
                )
            except Exception as e:
                print("[Retrieval] ❕ Could not init Claude:", e)

    def _batch_top_per_doc(self, q_vec: List[float]) -> List[Dict[str, Any]]:
        """Return ≤ top_k_per_doc vectors from *each* source PDF."""
        D, I = self.db.index.search(np.asarray([q_vec], dtype="float32"),
                                    self.db.index.ntotal)

        buckets: Dict[str, List[tuple]] = defaultdict(list)
        for dist, idx in zip(D[0], I[0]):
            meta = self.db.metadata[idx]
            src = meta["source"]
            if len(buckets[src]) < self.top_k_per_doc:
                buckets[src].append((dist, meta))

        return [meta for src in buckets for _, meta in buckets[src]]

    def retrieve(self, sop_text: str) -> List[Dict[str, Any]]:
        q_vec = embed_texts([sop_text])[0]
        return self._batch_top_per_doc(q_vec)

    def filter_relevant(self, sop_text: str, candidates: List[Dict[str, Any]]):
        """Use Claude to keep only relevant clauses, else return all."""
        if not self.llm:
            return candidates

        numbered = "\n".join(
            f"{i+1}. ({c['source']}) {c['clause_id']} — {c['text']}"
            for i, c in enumerate(candidates)
        )
        prompt = f"""
You are a strict compliance analyst.

SOP EXCERPT:
\"\"\"{sop_text[:1200]}\"\"\"

Below is a numbered list of clauses.
Return a JSON array with ONLY the numbers that are relevant, e.g. [1,3,5].

CLAUSES:
{numbered}
"""

        try:
            raw_msg = self.llm.invoke(prompt)
            raw = raw_msg.content
            ids = json.loads(raw)
            return [
                candidates[int(i) - 1]
                for i in ids
                if isinstance(i, int) or (isinstance(i, str) and i.isdigit())
            ]
        except BadRequestError as e:
            print("[Retrieval] Claude quota hit heuristic fallback:", e)
            return candidates
        except Exception as e:
            print("[Retrieval] Claude relevance failed heuristic fallback:", e)
            return candidates
