# Clinical Question Answering Model using MIMIC-III & LLMs

An end-to-end clinical QA system using **Retrieval-Augmented Generation (RAG)** over MIMIC-III data. It retrieves relevant clinical evidence and produces citation-grounded answers.

## 🔴 Live demo (no install, no API key)

**▶ https://sriya19.github.io/Clinical-Question-Answering-Model-using-MIMIC-III-LLMs/**

A fully in-browser demo: ask a clinical question and it retrieves the most relevant evidence from real MIMIC-III records (via a BM25 ranker) and shows a grounded, cited answer. Runs entirely client-side — nothing to install, no server, no OpenAI key. Perfect for portfolios.

The demo's clinical corpus is built automatically from the MIMIC-III tables in this repo by `build_corpus.py`, and published to GitHub Pages by `.github/workflows/deploy-pages.yml`.

## Full pipeline (Colab notebook + GPT-4)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sriya19/Clinical-Question-Answering-Model-using-MIMIC-III-LLMs/blob/main/CLinical%20QA.ipynb)

The notebook runs the complete system — Sentence-BERT + FAISS retrieval, **OpenAI GPT-4** answer generation, a Gradio UI, and BERTScore/ROUGE evaluation. It is self-contained (clones this repo for data, no Google Drive needed).

**Open in Colab:**
https://colab.research.google.com/github/sriya19/Clinical-Question-Answering-Model-using-MIMIC-III-LLMs/blob/main/CLinical%20QA.ipynb

### Where to put your OpenAI API key

You need an OpenAI key (`sk-...`) from https://platform.openai.com/api-keys. The notebook reads it in **Cell 3 (“Set your OpenAI API key”)** two ways:

1. **Colab Secrets (recommended):** in Colab, click the **🔑 key icon** in the left sidebar → **Add new secret** → name it exactly `OPENAI_API_KEY`, paste your key, enable **Notebook access**.
2. **Prompt:** if no secret is set, running Cell 3 shows a password box — paste your key there.

The key is never written into the notebook or committed to git. *(The live web demo above needs no key at all.)*

## How it works

| Component | What it does |
|---|---|
| `build_corpus.py` | Turns MIMIC-III structured tables (admissions, diagnoses, procedures, patients) into a retrievable clinical corpus |
| `docs/index.html` | The live browser demo: BM25 retrieval + grounded cited answers, 100% client-side |
| `CLinical QA.ipynb` | Full pipeline: Sentence-BERT + FAISS retrieval, GPT-4 generation, Gradio UI, BERTScore/ROUGE evaluation |

## Data note

The original system read free-text discharge summaries from `NOTEEVENTS.csv`, which is **not** in this repo (it needs separate MIMIC-III credentialed download and is very large). Both the demo and the notebook therefore build an equivalent retrievable corpus from the structured tables that **are** committed here. If you later add `NOTEEVENTS.csv`, set `USE_NOTEEVENTS = True` in the notebook's corpus cell to use the real notes (required to reproduce the paper's factuality scores against `test.final.json`).

## Attribution

- **MIMIC-III**: https://physionet.org/content/mimiciii/1.4/ (credentialed access)
- **Evaluation set**: `test.final.json` from the ArchEHR-QA 2025 Shared Task
- **LLM**: OpenAI GPT-4

## License

Apache 2.0 — see [LICENSE](LICENSE).
