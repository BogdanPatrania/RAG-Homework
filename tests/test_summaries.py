from src.utils.summaries import get_summary_by_title

def test_get_summary_known_book():
    result = get_summary_by_title("1984")
    assert isinstance(result, str)
    assert "Big Brother" in result or len(result) > 10

def test_get_summary_unknown_book():
    result = get_summary_by_title("Unknown Title")
    assert "Nu am găsit" in result
