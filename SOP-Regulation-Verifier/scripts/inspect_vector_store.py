# scripts/inspect_vector_store.py

import pickle
import faiss
import env

INDEX_PATH = "vector_store/clauses.index"
META_PATH  = INDEX_PATH + ".meta"

index = faiss.read_index(INDEX_PATH)
print(f"➤ FAISS index contains {index.ntotal} vectors.")

with open(META_PATH, "rb") as f:
    metadata = pickle.load(f)
print(f"➤ Metadata list contains {len(metadata)} entries.")

if index.ntotal != len(metadata):
    print("⚠️  Warning: vector count and metadata count do not match!")