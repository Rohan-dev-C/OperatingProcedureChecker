from src.vector_db import VectorDB

def test_vector_db_roundtrip(tmp_path):
    idx_path = tmp_path / "test.index"
    db = VectorDB(str(idx_path), dim=3)

    embeddings = [[0.1, 0.2, 0.3], [0.3, 0.2, 0.1]]
    metadata = [{"clause_id": "A"}, {"clause_id": "B"}]
    db.add(embeddings, metadata)
    db.save()
    db2 = VectorDB(str(idx_path), dim=3)
    res = db2.query([0.1, 0.2, 0.3], top_k=1)
    assert len(res) == 1
    assert res[0]["clause_id"] in ("A", "B")
