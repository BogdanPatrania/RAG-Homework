# Smart Librarian – AI with RAG + Tool

An AI-powered chatbot that recommends books based on user interests, using **OpenAI GPT** combined with **Retrieval-Augmented Generation (RAG)** via **ChromaDB**, and then enriches the recommendation with a detailed summary from a custom tool.

---

## Features

* **Semantic search (RAG)**: Store and retrieve book summaries with embeddings.
* **AI-powered chatbot**: Natural language recommendations using GPT.
* **Custom tool integration**: `get_summary_by_title(title)` provides detailed summaries.
* **Optional extensions**:

  * Inappropriate language filter
  * Text-to-Speech (TTS)
  * Speech-to-Text (STT)
  * Book cover or scene image generation
  * Alternative frontend (React, Angular, Vue) with Python backend【111†source】

---

## Project Structure

```
.
├── README.md                # Project documentation
├── .gitignore
├── LICENSE
├── environment.yml          # Conda environment
├── requirements.txt         # Pip requirements
├── Makefile                 # Common tasks
├── docker/
│   └── Dockerfile
├── src/
│   ├── data/
│   │   └── make_dataset.py  # Load and embed summaries into ChromaDB
│   ├── models/
│   │   ├── rag_pipeline.py  # Retrieval + GPT pipeline
│   │   └── fine_tune.py     # (Optional) fine-tuning scripts
│   └── utils/
│       ├── io.py            # I/O helpers
│       └── eval.py          # Evaluation helpers
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_prompt_engineering.ipynb
│   ├── 03_rag.ipynb
│   └── 04_finetuning.ipynb
├── data/
│   ├── book_summaries.json  # Main dataset (10+ books)
│   ├── raw/.gitkeep
│   ├── processed/.gitkeep
│   └── external/.gitkeep
├── docs/
│   └── report.md
└── tests/
    └── test_utils.py
```

---

## Quickstart

### 1. Environment Setup

**With Conda**

```bash
conda env create -f environment.yml
conda activate llm-assignment
```

**With pip/venv**

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Secrets

Copy `.env.example` to `.env` and add your **OpenAI API key**.

### 3. Add Book Summaries

Create `data/book_summaries.json` with at least 10 books, e.g.:

```json
{
  "1984": "A dystopian story about a totalitarian society...",
  "The Hobbit": "Bilbo Baggins embarks on an adventure with dwarves..."
}
```

### 4. Initialize Vector Store

```bash
python src/data/make_dataset.py
```

### 5. Run the Chatbot

* **CLI version**:

```bash
python src/chat.py
```

* **Streamlit version**:

```bash
streamlit run app.py
```

### 6. Run Tests

```bash
pytest -q
```

---

## Deliverables

* `book_summaries.json` with 10+ books
* ChromaDB initialization scripts
* `get_summary_by_title()` tool
* Chatbot with GPT + tool integration
* CLI or Streamlit interface
* Updated `README.md` with build & run instructions【111†source】

---

## Example Queries

* „Vreau o carte despre libertate și control social.”
* „Ce-mi recomanzi dacă iubesc poveștile fantastice?”
* „Ce este 1984?”【111†source】

---

## Notes

* Alternative vector stores are acceptable; if OpenAI vector store is used, document issues encountered【111†source】.
* The focus is on understanding the **code and flow** of RAG + tool calling【111†source】.
* Extensions (TTS, STT, images, advanced UI) are optional but encouraged for extra functionality.
