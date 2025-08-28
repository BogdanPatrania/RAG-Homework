# Smart Librarian – AI with RAG + Tool

An AI-powered chatbot that recommends books based on user interests, using **OpenAI GPT** combined with **Retrieval-Augmented Generation (RAG)** via **ChromaDB**, and then enriches the recommendation with a detailed summary from a custom tool.

---

## Features

- **Semantic search (RAG)**: store and retrieve book summaries with embeddings.
- **AI-powered chatbot**: natural language recommendations using GPT.
- **Custom tool integration**: `get_summary_by_title(title)` provides detailed summaries.
- **Moderation (Romanian)**: offensive queries are censored and **not sent** to the LLM (works in CLI and Streamlit).
- **Optional extensions**: Text-to-Speech (TTS), Speech-to-Text (STT), image generation, richer UI.

---

## Project Structure

```
.
├── README.md
├── requirements.txt
├── app.py                      # Streamlit UI chatbot
├── src/
│   ├── chat.py                 # CLI chatbot
│   ├── data/
│   │   └── make_dataset.py     # Build ChromaDB from summaries
│   ├── models/
│   │   └── rag_pipeline.py     # Retriever
│   └── utils/
│       ├── summaries.py        # Summary tool
│       └── moderation.py       # Romanian profanity filter
├── data/
│   ├── raw/book_summaries.json
│   ├── processed/chroma/       # ChromaDB persistent store
│   └── external/badwords_ro.txt
└── tests/
    ├── test_utils.py
    ├── test_summaries.py
    └── test_retriever.py
```

---

## Quickstart

### 1. Environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Secrets

Create `.env` and set:

```
OPENAI_API_KEY=your_real_key
```

### 3. Book Summaries

Add at least 10 entries in `data/raw/book_summaries.json`:

```json
[
  {
    "title": "1984",
    "short_summary": "A dystopian story about a totalitarian society...",
    "themes": ["libertate", "control social", "distopie"]
  },
  {
    "title": "The Hobbit",
    "short_summary": "Bilbo Baggins embarks on an adventure with dwarves...",
    "themes": ["prietenie", "aventură", "magie"]
  }
]
```

### 4. Build Vector Store

```bash
python -m src.data.make_dataset
# optional probe
python -m src.data.make_dataset --probe "prietenie și magie" --top_k 5
```

### 5. Run the Chatbot

**CLI**:

```bash
python -m src.chat
```

**Streamlit**:

```bash
streamlit run app.py
```

Both versions:
- Retrieve candidates from ChromaDB.
- Ask GPT for one recommendation (`RECOMMENDATION_TITLE: ...`).
- Append detailed summary from the tool.
- Block inappropriate inputs with the Romanian profanity filter.

### 6. Run Tests

```bash
pytest -q
```

---

## Deliverables

- `data/raw/book_summaries.json` (10+ books)
- ChromaDB init (`src/data/make_dataset.py`)
- Retriever (`src/models/rag_pipeline.py`)
- Tool (`src/utils/summaries.py`)
- Chatbot: CLI (`src/chat.py`) + Streamlit (`app.py`)
- Moderation (`src/utils/moderation.py`)
- README (this file)
- Tests (`tests/`)

---

## Example Queries

- „Vreau o carte despre libertate și control social.”
- „Ce-mi recomanzi dacă iubesc poveștile fantastice?”
- „Ce este 1984?”

---

## Notes

- Alternative vector stores are acceptable; if you use OpenAI’s vector store, document issues.
- Focus: demonstrate **RAG + tool calling** and understand the flow.
- Extensions (TTS, STT, images, advanced UI) are optional but encouraged.
