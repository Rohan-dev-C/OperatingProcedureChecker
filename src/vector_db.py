import os
import pickle
import numpy as np
import faiss
from typing import List, Dict, Any


class VectorDB:
    """
    Wrapper around a FAISS IndexFlatL2 and aligned metadata.

    Args:
        index_path: path to the FAISS .index file (default: vector_store/clauses.index)
        dim: dimensionality of embeddings
        reset: if True, ignore existing index and create a new one
    """

    def __init__(self, index_path: str = "vector_store/clauses.index", dim: int = 1536, reset: bool = False):
        self.index_path = index_path
        self.dim = dim

        if reset:
            self._init_empty()
            return

        try:
            if os.path.exists(index_path) and os.path.exists(index_path + ".meta"):
                self.index = faiss.read_index(index_path)
                with open(index_path + ".meta", "rb") as f:
                    self.metadata = pickle.load(f)
                print(f"[VectorDB] Loaded existing index with {self.index.ntotal} vectors.")
            else:
                self._init_empty()
        except Exception as e:
            print(f"[VectorDB] Failed to load index ({e}) — creating a new one.")
            self._init_empty()

    def _init_empty(self):
        self.index = faiss.IndexFlatL2(self.dim)
        self.metadata = []
        print("[VectorDB] Initialized new empty FAISS index.")

    def add(self, embeddings: List[List[float]], metadatas: List[Dict[str, Any]]):
        vecs = np.array(embeddings, dtype='float32')
        self.index.add(vecs)
        self.metadata.extend(metadatas)

    def query(self, query_vec: List[float], top_k: int = 5):
        q = np.array([query_vec], dtype='float32')
        D, I = self.index.search(q, top_k)
        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx < len(self.metadata):
                item = self.metadata[idx].copy()
                item["score"] = float(dist)
                results.append(item)
        return results

    def save(self):
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.index_path + ".meta", "wb") as f:
            pickle.dump(self.metadata, f)
        print(f"[VectorDB] Saved index to {self.index_path} and metadata.")
