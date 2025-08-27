from pathlib import Path
from typing import List, Dict, Any
import os
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

CHROMA_DIR = Path("data/processed/chroma")
COLLECTION_NAME = "books"
EMBEDDING_MODEL = "text-embedding-3-small"

def _client() -> chromadb.PersistentClient:
    return chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))

def _collection():
    return _client().get_or_create_collection(COLLECTION_NAME)

def _embed_query(text: str) -> list[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return client.embeddings.create(model=EMBEDDING_MODEL, input=[text]).data[0].embedding

def retrieve(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    col = _collection()
    q_emb = _embed_query(query)
    res = col.query(query_embeddings=[q_emb], n_results=top_k)
    out = []
    for i in range(len(res["ids"][0])):
        distance = res.get("distances", [[None]])[0][i]
        similarity = None if distance is None else 1 - distance  # cosine similarity approx
        out.append({
            "title": res["metadatas"][0][i].get("title"),
            "distance": distance,
            "similarity": similarity,
            "document": res["documents"][0][i],
        })
    return out

if __name__ == "__main__":
    q = "o carte despre prietenie și magie"
    hits = retrieve(q, 5)
    print("Query:", q)
    for h in hits:
        print(f" - {h['title']} (distance={h['distance']:.3f}, similarity={h['similarity']:.3f})")
