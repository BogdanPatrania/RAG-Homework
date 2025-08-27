import os, re
from dotenv import load_dotenv
from openai import OpenAI
from src.models.rag_pipeline import retrieve
from src.utils.summaries import get_summary_by_title

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM = "Ești un asistent care recomandă o singură carte din contextul primit."
PROMPT = """Context (top cărți):
{context}

Întrebare: {query}

Instrucțiuni:
- Alege o singură recomandare din context.
- Prima linie trebuie să fie exact: RECOMMENDATION_TITLE: <titlu>
- După prima linie, oferă un răspuns conversațional scurt (2–4 propoziții) în română.
"""

def recommend(query: str, top_k=4) -> str:
    hits = retrieve(query, top_k)
    if not hits:
        return "Nu am găsit o potrivire. Încearcă să reformulezi."
    ctx = "\n\n".join(f"- {h['title']}\n{h['document']}" for h in hits)
    msg = PROMPT.format(context=ctx, query=query)

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":SYSTEM},{"role":"user","content":msg}],
        temperature=0.4,
    )
    text = resp.choices[0].message.content.strip()
    m = re.search(r"^RECOMMENDATION_TITLE:\s*(.+)$", text, flags=re.IGNORECASE|re.MULTILINE)
    title = m.group(1).strip() if m else None
    if title:
        summary = get_summary_by_title(title)
        return f"{text}\n\nRezumat detaliat:\n{summary}"
    return text

if __name__ == "__main__":
    print("Type your question (or 'exit'):")
    while True:
        q = input("> ").strip()
        if not q or q.lower() in {"exit","quit"}:
            break
        print(recommend(q))
