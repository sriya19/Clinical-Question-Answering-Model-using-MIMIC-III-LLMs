# Clinical Question Answering Model using MIMIC-III & LLMs

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sriya19/Clinical-Question-Answering-Model-using-MIMIC-III-LLMs/blob/claude/elegant-shannon-mpdao6/CLinical%20QA.ipynb)

An end-to-end clinical QA system using **Retrieval-Augmented Generation (RAG)** over MIMIC-III data. Sentence-BERT + FAISS retrieve relevant clinical text and OpenAI GPT-4 generates cited answers. The notebook is fully self-contained: it clones this repo for data, so no Google Drive is required.

## Run it (one click)

Open the notebook in Colab using the badge above, then run the cells top to bottom.

**Direct link (this branch):**
https://colab.research.google.com/github/sriya19/Clinical-Question-Answering-Model-using-MIMIC-III-LLMs/blob/claude/elegant-shannon-mpdao6/CLinical%20QA.ipynb

## Where to put your OpenAI API key

You need an OpenAI key (`sk-...`) from https://platform.openai.com/api-keys. The notebook reads it in **Cell 3 (“Set your OpenAI API key”)** via one of two ways:

1. **Colab Secrets (recommended):** in Colab, click the **🔑 key icon** in the left sidebar → **Add new secret** → name it exactly `OPENAI_API_KEY`, paste your key, enable **Notebook access**. The notebook picks it up automatically.
2. **Prompt:** if no secret is set, running Cell 3 shows a password box — paste your key there.

The key is never written into the notebook or committed to git.

## How it works

| Step (cell) | What it does |
|---|---|
| 1. Install | Installs `openai`, `faiss-cpu`, `sentence-transformers`, `gradio`, `bert-score`, `rouge-score` |
| 2. Get data | Clones this repo (all MIMIC-III CSVs are committed here) |
| 3. API key | Loads your OpenAI key (see above) |
| 4. Build corpus | Turns structured admissions/diagnoses/procedures into retrievable clinical narratives |
| 5. Retriever + LLM | Builds a Sentence-BERT + FAISS index and the GPT-4 answer generator |
| 6. Sample query | Runs one end-to-end question so you can confirm it works |
| 7. Gradio UI | Interactive app for patient + clinician question pairs |
| 8. Evaluation | BERTScore + ROUGE against `test.final.json` |

## Data note (important)

The original system read free-text discharge summaries from `NOTEEVENTS.csv`. That file is **not** in this repo (it requires separate MIMIC-III credentialed download and is very large). So the notebook instead builds an equivalent retrievable corpus from the structured tables that **are** committed here: `ADMISSIONS`, `DIAGNOSES_ICD`, `PROCEDURES_ICD`, `PATIENTS`, and the ICD dictionaries.

If you add `NOTEEVENTS.csv` to the repo, set `USE_NOTEEVENTS = True` in Cell 4 and the notebook will use the real notes (which is required to reproduce the paper's factuality scores against `test.final.json`).

## Attribution

- **MIMIC-III**: https://physionet.org/content/mimiciii/1.4/ (credentialed access)
- **Evaluation set**: `test.final.json` from the ArchEHR-QA 2025 Shared Task
- **LLM**: OpenAI GPT-4

## License

Apache 2.0 — see [LICENSE](LICENSE).
