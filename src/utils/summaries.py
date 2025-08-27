import json
from pathlib import Path

DATA = Path("data/raw/book_summaries.json")

def _load_map():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return {k.lower(): v for k, v in data.items()}
    return {r["title"].lower(): r.get("full_summary") or r.get("short_summary","") for r in data}

def get_summary_by_title(title: str) -> str:
    m = _load_map()
    return m.get(title.lower(), "Nu am găsit rezumatul pentru acest titlu.")
