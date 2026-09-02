"""Build docs/corpus.json for the browser RAG demo from the MIMIC-III tables in this repo."""
import pandas as pd, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "docs", "corpus.json")
MAX_ADM = 1200

def load(name, **kw):
    for cand in (f"{HERE}/{name}.csv", f"{HERE}/{name}.csv.gz"):
        if os.path.exists(cand):
            return pd.read_csv(cand, **kw)
    raise FileNotFoundError(name)

admissions = load("ADMISSIONS")
patients   = load("PATIENTS")
diagnoses  = load("DIAGNOSES_ICD")
d_diag     = load("D_ICD_DIAGNOSES")
procs      = load("PROCEDURES_ICD")
d_proc     = load("D_ICD_PROCEDURES")

diag_titles = dict(zip(d_diag["ICD9_CODE"].astype(str), d_diag["LONG_TITLE"]))
proc_titles = dict(zip(d_proc["ICD9_CODE"].astype(str), d_proc["LONG_TITLE"]))
diagnoses["TITLE"] = diagnoses["ICD9_CODE"].astype(str).map(diag_titles)
procs["TITLE"]     = procs["ICD9_CODE"].astype(str).map(proc_titles)

diag_by_hadm = (diagnoses.dropna(subset=["TITLE"]).sort_values("SEQ_NUM")
                .groupby("HADM_ID")["TITLE"].apply(list).to_dict())
proc_by_hadm = (procs.dropna(subset=["TITLE"]).sort_values("SEQ_NUM")
                .groupby("HADM_ID")["TITLE"].apply(list).to_dict())
gender_by_subj = dict(zip(patients["SUBJECT_ID"], patients["GENDER"]))

sentences, seen = [], set()
for _, row in admissions.head(MAX_ADM).iterrows():
    hadm, subj = int(row["HADM_ID"]), row["SUBJECT_ID"]
    gender = {"M": "male", "F": "female"}.get(gender_by_subj.get(subj, ""), "patient")
    admtype = str(row.get("ADMISSION_TYPE", "")).lower()
    loc = str(row.get("ADMISSION_LOCATION", "an unknown location")).lower()
    out = []
    if pd.notna(row.get("DIAGNOSIS")):
        out.append(f"A {gender} patient was admitted via {admtype} admission from {loc} "
                   f"with a presenting complaint of {str(row['DIAGNOSIS']).lower()}.")
    else:
        out.append(f"A {gender} patient was admitted via {admtype} admission from {loc}.")
    for d in diag_by_hadm.get(hadm, [])[:8]:
        out.append(f"The patient was diagnosed with {d.lower()}.")
    for p in proc_by_hadm.get(hadm, [])[:8]:
        out.append(f"The procedure performed was {p.lower()}.")
    if pd.notna(row.get("DISCHARGE_LOCATION")):
        out.append(f"The patient was discharged to {str(row['DISCHARGE_LOCATION']).lower()}.")
    if row.get("HOSPITAL_EXPIRE_FLAG", 0) == 1:
        out.append("The patient expired during this hospital admission.")
    for s in out:
        if len(s) > 15 and s not in seen:
            seen.add(s)
            sentences.append({"t": s, "h": hadm})

os.makedirs(os.path.join(HERE, "docs"), exist_ok=True)
with open(OUT, "w") as f:
    json.dump({"sentences": sentences, "source": "MIMIC-III (structured tables)",
               "n_admissions": MAX_ADM}, f, separators=(",", ":"))
print(f"Wrote {len(sentences)} sentences to {OUT}")
