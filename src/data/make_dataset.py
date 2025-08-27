# src/data/make_dataset.py
from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple

import chromadb
from chromadb.config import Settings

from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

RAW_JSON = Path("data/raw/book_summaries.json")
CHROMA_DIR = Path("data/processed/chroma")
COLLECTION_NAME = "books"
EMBEDDING_MODEL = "text-embedding-3-small"  # per assignment suggestion

def load_book_summaries(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Create data/raw/book_summaries.json first.")
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Accept either dict(title -> summary) or list of records with fields.
    records: List[Dict[str, Any]] = []
    if isinstance(data, dict):
        # { "Title": "short_summary..." , ... }
        for title, short_summary in data.items():
            records.append({
                "title": title,
                "short_summary": short_summary,
                "themes": [],  # optional
            })
    elif isinstance(data, list):
        # [{ "title": "...", "short_summary": "...", "themes": ["..."] }, ...]
        records = data
    else:
        raise ValueError("book_summaries.json must be a dict or a list of records.")

    # Minimal validation
    cleaned = []
    for i, r in enumerate(records):
        title = (r.get("title") or "").strip()
        short_summary = (r.get("short_summary") or r.get("summary") or "").strip()
        themes = r.get("themes") or []
        if not title or not short_summary:
            raise ValueError(f"Record {i} missing title/short_summary.")
        if not isinstance(themes, list):
            themes = [str(themes)]
        cleaned.append({"title": title, "short_summary": short_summary, "themes": themes})
    return cleaned

def build_document(record: Dict[str, Any]) -> str:
    """Compact document text for embedding & retrieval."""
    parts = [
        f"Title: {record['title']}",
        record["short_summary"],
    ]
    if record["themes"]:
        parts.append("Themes: " + ", ".join(record["themes"]))
    return "\n".join(parts)

def ensure_dirs():
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

def make_client() -> chromadb.PersistentClient:
    return chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))

def get_or_create_collection(client: chromadb.PersistentClient):
    # cosine similarity is default; you can set metadata={"hnsw:space":"cosine"} explicitly if desired
    return client.get_or_create_collection(name=COLLECTION_NAME)

def embed_texts(texts: List[str]) -> List[List[float]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY not set. Put it in .env and load your environment.")
    client = OpenAI(api_key=api_key)
    # The OpenAI Embeddings API supports batching; we’ll call once with a list
    resp = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [d.embedding for d in resp.data]

def ingest(records):
    ensure_dirs()
    client = make_client()
    col = get_or_create_collection(client)

    # Optional: wipe the collection if you want a clean rebuild each run
    # col.delete(where={})

    ids, docs, metas = [], [], []
    for idx, r in enumerate(records):
        ids.append(f"book-{idx}-{r['title']}")
        docs.append(build_document(r))
        themes_str = ", ".join(r["themes"]) if r.get("themes") else ""
        metas.append({
            "title": r["title"],
            "themes": themes_str,          # was a list; now a string
        })

    embeddings = embed_texts(docs)
    col.upsert(ids=ids, documents=docs, metadatas=metas, embeddings=embeddings)
    return col.count(), CHROMA_DIR

# near embed_texts()
def embed_query(text: str) -> list[float]:
    # reuse the same OpenAI model as for upserts
    return embed_texts([text])[0]


def probe(query: str, top_k: int = 5):
    client = make_client()
    col = get_or_create_collection(client)
    q_emb = embed_query(query)                # NEW: embed with OpenAI (1536-dim)
    res = col.query(query_embeddings=[q_emb], n_results=top_k)  # not query_texts
    print("\n[Probe] Query:", query)
    for i in range(len(res["ids"][0])):
        title = res["metadatas"][0][i].get("title")
        score = res["distances"][0][i] if "distances" in res else None
        print(f"  {i+1}. {title}  (distance: {score})")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Embed book summaries into ChromaDB.")
    p.add_argument("--probe", type=str, default=None, help="Optional: run a test query after ingest.")
    p.add_argument("--top_k", type=int, default=5, help="Top-k for probe results.")
    args = p.parse_args()

    records = load_book_summaries(RAW_JSON)
    total, chroma_path = ingest(records)
    print(f"Ingested into collection='{COLLECTION_NAME}'. Total items now: {total}.")
    print(f"Chroma persisted at: {chroma_path.resolve()}")

    if args.probe:
        probe(args.probe, top_k=args.top_k)
