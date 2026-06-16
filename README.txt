# Clinical Question Answering (QA) System using RAG and OpenAI

## Overview

This project implements a clinical QA system that leverages Retrieval-Augmented Generation (RAG) to answer clinical questions from the MIMIC-III dataset. It combines Sentence-BERT embeddings and FAISS for sentence retrieval, and uses OpenAI’s GPT-4 model to generate grounded, cited answers from clinical notes. Evaluation is done using BERTScore and ROUGE.

## Setup Instructions 
Note: The instructions for setup is for the implementation on Google Collab.

1. Mount Google Drive:
   Your CSV files must be stored in Google Drive.

   ```python
   from google.colab import drive
   drive.mount('/content/drive/')
   ```

2. Install Required Libraries:

   Install the dependencies using:
   ```bash
   pip install -r requirements.txt
   ```

3. Files Required in Google Drive:

   Place these files in `/content/drive/My Drive/`:
   - `ADMISSIONS.csv`
   - `Diagnosis.csv` (tab-separated, UTF-16)
   - `Procedures.csv` (tab-separated, UTF-16)
   - `NOTEEVENTS.csv`
   - `PATIENTS.csv`
   - `PRESCRIPTIONS.csv`
   - `test.final.json` (SQuAD-style QA dataset)

---

## Workflow

### 1. Data Loading and Preprocessing

- Read MIMIC-III CSVs using `pandas`.
- Drop rows with missing crucial values.
- Clean and extract `ADMISSION_DATE` and `DISCHARGE_DATE` from notes.
- Rename columns to match for merging.

### 2. Sentence Embedding and Retrieval

- Load and split clinical notes into sentences (subset).
- Encode using Sentence-BERT (`all-MiniLM-L6-v2`).
- Index with FAISS for fast top-k sentence retrieval.

### 3. Answer Generation with OpenAI

- Use OpenAI's `gpt-4` model to generate answers.
- Cite evidence using numbered sentences (e.g., (1), (2)).
- Limit answer to 75 words.

### 4. Interactive QA using Gradio

- The user provides:
  - `patient_q`: Patient's question
  - `clinician_q`: Clinician's question
- System retrieves sentences and generates an answer with citations.

### 5. Evaluation

- Match user input to the closest gold QA pair from `test.final.json`.
- Evaluate generated answer with:
  - BERTScore: Factuality
  - ROUGE: Relevance

### Files Included

- AIT526 Team 6.ipynb: Main notebook to run the clinical QA system with RAG.
- test.final.json: SQuAD-style dataset containing clinical question-answer pairs for evaluation.
- README.txt: List of required guidelines.

## Example Use 

```python
# Run the interactive QA system
file_path = '/content/drive/MyDrive/NOTEEVENTS.csv'
answer, top_sentences, clinician_q, patient_q = interactive_qa_with_openai_rag(file_path)

# Evaluate the answer
factuality_scores = evaluate_factuality(answer, gold_answer)
relevance_scores = evaluate_relevance(answer, top_sentences)
```

## Expected Output

Example Input:
```
Patient Question: I had severe abdomen pain and was hospitalised for 15 days in ICU, diagnoised with CBD sludge. Doctor advised for ERCP. My question is if the sludge was there does not any medication help in flushing it out? Whether ERCP was the only cure?
Clinician Question: Why was ERCP recommended over a medication-based treatment for CBD sludge?
```

Example Output:
```
Answer: ERCP was recommended over medication-based treatment due to the presence of gallstones obstructing the bile ducts (3), and a dilated CBD (1). Medications may not effectively clear these obstructions. The ERCP procedure allowed for a sphincterotomy and placement of a CBD stent to alleviate the obstruction (2). This intervention was necessary to treat the cholangitis (6), a serious infection that can occur due to blocked bile ducts.
```

Evaluation Scores:

=== Factuality Evaluation ===
BERTScore Precision: 0.8000
BERTScore Recall: 0.8185
BERTScore F1: 0.8091

=== Relevance Evaluation ===
ROUGE-1 F1: 0.3116
ROUGE-L F1: 0.1709
BERTScore F1: 0.8400

## License and Attribution

- Dataset: MIMIC-III (https://physionet.org/content/mimiciii/1.4/)
- Evaluation Dataset: `test.final.json` from ArchEHR-QA 2025 Shared Task
- GPT-4 powered by OpenAI API

Note : All the datasets except for the NOTEEVENTS is attached in the zip folder. The NOTEVENTS can be downloaded from the link provided above.