# app.py
from __future__ import annotations
import os, re
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Local modules
from src.models.rag_pipeline import retrieve
from src.utils.summaries import get_summary_by_title

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Smart Librarian", page_icon="📖", layout="centered")

st.title("Smart Librarian – RAG Chatbot")
st.caption("OpenAI GPT + ChromaDB. Ask for a book by theme or interest.")

# Sidebar controls
with st.sidebar:
    st.header("Settings")
    top_k = st.slider("Top-k retrieved", 1, 8, 4, 1)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.4, 0.1)
    show_retrieval = st.checkbox("Show retrieved candidates", value=True)
    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o", "gpt-4o-mini-2024-07-18"], index=0)

SYSTEM = "Ești un asistent care recomandă o singură carte din contextul primit."
PROMPT = """Context (top cărți):
{context}

Întrebare: {query}

Instrucțiuni:
- Alege o singură recomandare din context.
- Prima linie trebuie să fie exact: RECOMMENDATION_TITLE: <titlu>
- După prima linie, oferă un răspuns conversațional scurt (2–4 propoziții) în română.
"""

def recommend(query: str, top_k: int, model: str, temperature: float) -> dict:
    hits = retrieve(query, top_k=top_k)
    if not hits:
        return {"text": "Nu am găsit o potrivire. Încearcă să reformulezi.", "title": None, "hits": []}
    ctx = "\n\n".join(f"- {h['title']}\n{h['document']}" for h in hits)
    msg = PROMPT.format(context=ctx, query=query)

    if not OPENAI_API_KEY:
        return {"text": "Lipsește OPENAI_API_KEY în .env sau în mediul curent.", "title": None, "hits": hits}

    client = OpenAI(api_key=OPENAI_API_KEY)
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": msg}],
        temperature=temperature,
    )
    text = resp.choices[0].message.content.strip()
    m = re.search(r"^RECOMMENDATION_TITLE:\s*(.+)$", text, flags=re.IGNORECASE | re.MULTILINE)
    title = m.group(1).strip() if m else None
    return {"text": text, "title": title, "hits": hits}

# Main input
query = st.text_input("Ce carte ți-ai dori? (ex: „o carte despre prietenie și magie”)")
submit = st.button("Recomandă")

if submit and query.strip():
    with st.spinner("Caut…"):
        result = recommend(query.strip(), top_k=top_k, model=model, temperature=temperature)

    if show_retrieval and result["hits"]:
        with st.expander("Candidați (retrieval)"):
            for i, h in enumerate(result["hits"], 1):
                st.markdown(f"**{i}. {h['title']}**")
                st.caption(f"distance: {h.get('distance')}, similarity: {h.get('similarity')}")
                st.write(h["document"])

    st.markdown("---")
    st.subheader("Recomandare")
    st.write(result["text"])

    if result["title"]:
        st.markdown("### Rezumat detaliat (tool)")
        summary = get_summary_by_title(result["title"])
        st.write(summary)

else:
    st.info("Introdu o întrebare de recomandare și apasă „Recomandă”.")
