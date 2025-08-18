<<<<<<< HEAD
# RAG-Homework
=======
# Essentials of LLM — Assignment Repo

Scaffold generated on 2025-08-18. Fill in the TODO sections with your assignment specifics from the PDF.

## Project Structure

```
.
├── README.md
├── .gitignore
├── LICENSE
├── environment.yml
├── requirements.txt
├── Makefile
├── docker/
│   └── Dockerfile
├── src/
│   ├── data/
│   │   └── make_dataset.py
│   ├── models/
│   │   ├── rag_pipeline.py
│   │   └── fine_tune.py
│   └── utils/
│       ├── io.py
│       └── eval.py
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_prompt_engineering.ipynb
│   ├── 03_rag.ipynb
│   └── 04_finetuning.ipynb
├── data/
│   ├── raw/.gitkeep
│   ├── processed/.gitkeep
│   └── external/.gitkeep
├── docs/
│   └── report.md
└── tests/
    └── test_utils.py
```

## Quickstart

### 1) Create and activate environment

Using conda (recommended):

```bash
conda env create -f environment.yml
conda activate llm-assignment
```

Or with venv + pip:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Configure secrets

Copy `.env.example` to `.env` and set your keys (e.g., OpenAI). Never commit `.env`.

### 3) Run notebooks

Start Jupyter and work through `notebooks/` in order. Each notebook includes TODO blocks tied to the assignment.

### 4) Tests

```bash
pytest -q
```

### 5) Make common tasks easier

```bash
make help
```

## Repo Tasks (align with your assignment)

- [ ] Data exploration and preprocessing (notebooks/01_exploration.ipynb)
- [ ] Prompt engineering experiments (notebooks/02_prompt_engineering.ipynb)
- [ ] Retrieval-Augmented Generation (src/models/rag_pipeline.py, notebooks/03_rag.ipynb)
- [ ] Fine-tuning experiments (src/models/fine_tune.py, notebooks/04_finetuning.ipynb)
- [ ] Evaluation & report (src/utils/eval.py, docs/report.md)

## GitHub Setup

After unzipping:

```bash
git init
git add .
git commit -m "Initial scaffold for Essentials of LLM assignment"
# Create a repo on GitHub, then:
git branch -M main
git remote add origin https://github.com/<your-user>/essentials-llm-assignment.git
git push -u origin main
```

>>>>>>> a8c2cba (Initial scaffold for RAG Homework)
