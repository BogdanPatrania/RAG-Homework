from src.models.rag_pipeline import retrieve

def test_retrieve_returns_books():
    hits = retrieve("prietenie", top_k=2)
    assert len(hits) > 0
    assert "title" in hits[0]
