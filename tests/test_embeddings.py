from src.embeddings import embed_with_sbert

def test_sbert_embedding_shape():
    texts = ["Clause one", "Clause two"]
    vectors = embed_with_sbert(texts)
    assert len(vectors) == 2
    assert all(len(vec) == 384 for vec in vectors)
