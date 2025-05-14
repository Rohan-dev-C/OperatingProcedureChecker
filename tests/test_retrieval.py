from src.retrieval import Retrieval

class DummyDB:
    def query(self, vec, top_k):
        return [{"clause_id": "X", "text": "dummy"}]

def test_retrieve_with_mock():
    retr = Retrieval(DummyDB())
    results = retr.retrieve("some text", top_k=1)
    assert isinstance(results, list)
    assert results[0]["clause_id"] == "X"
