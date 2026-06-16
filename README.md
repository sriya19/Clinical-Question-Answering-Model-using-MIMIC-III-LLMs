# Clinical Question Answering Model using MIMIC-III & LLMs

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sriya19/Clinical-Question-Answering-Model-using-MIMIC-III-LLMs/blob/main/CLinical%20QA.ipynb)

A clinical QA system that leverages Retrieval-Augmented Generation (RAG) to answer clinical questions from the MIMIC-III dataset. Combines Sentence-BERT + FAISS for retrieval and OpenAI GPT-4 for grounded, cited answer generation.

## Quick Start — Open in Colab

**Click the badge above** or open directly:

https://colab.research.google.com/github/sriya19/Clinical-Question-Answering-Model-using-MIMIC-III-LLMs/blob/main/CLinical%20QA.ipynb

## Prerequisites

1. **MIMIC-III access** — Apply at [PhysioNet](https://physionet.org/content/mimiciii/1.4/) and place these CSV files in your Google Drive (`My Drive/`):
   - `ADMISSIONS.csv`, `Diagnosis.csv` (TSV, UTF-16), `Procedures.csv` (TSV, UTF-16)
   - `NOTEEVENTS.csv`, `PATIENTS.csv`, `PRESCRIPTIONS.csv`

2. **OpenAI API key** — Add as a [Colab secret](https://medium.com/@parthdasawant/how-to-use-secrets-in-google-colab-450c38e3ec75) named `OPENAI_API_KEY` (the notebook will prompt you if not set).

3. **`test.final.json`** — Downloaded automatically by the notebook from this repo. No manual upload needed.

## Workflow

| Step | Description |
|---|---|
| 1. Mount Drive | Connect Google Drive with MIMIC-III CSVs |
| 2. Preprocessing | Clean and merge clinical notes, admissions, diagnoses, procedures, prescriptions |
| 3. Embedding & Indexing | Sentence-BERT (`all-MiniLM-L6-v2`) + FAISS for fast retrieval |
| 4. RAG QA | GPT-4 generates a cited ≤75-word answer from top-8 retrieved sentences |
| 5. Gradio UI | Interactive interface for patient + clinician question pairs |
| 6. Evaluation | BERTScore (factuality) + ROUGE (relevance) against `test.final.json` gold pairs |

## Files

| File | Description |
|---|---|
| `CLinical QA.ipynb` | Main notebook |
| `test.final.json` | SQuAD-style evaluation dataset (ArchEHR-QA 2025) |

## Example Output

**Input:**
- Patient: *"I had severe abdomen pain…diagnosed with CBD sludge. Was ERCP the only cure?"*
- Clinician: *"Why was ERCP recommended over medication-based treatment?"*

**Answer:** *ERCP was recommended due to gallstones obstructing the bile ducts (3) and a dilated CBD (1). Medications may not effectively clear these obstructions. The ERCP allowed sphincterotomy and placement of a CBD stent (2), necessary to treat cholangitis (6).*

**Scores:** BERTScore F1 ≈ 0.809 · ROUGE-1 F1 ≈ 0.312

## Attribution

- **MIMIC-III**: [PhysioNet](https://physionet.org/content/mimiciii/1.4/) — requires credentialed access
- **Evaluation set**: `test.final.json` from ArchEHR-QA 2025 Shared Task
- **LLM**: OpenAI GPT-4

## License

Apache 2.0 — see [LICENSE](LICENSE).
