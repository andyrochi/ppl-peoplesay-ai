"""
Analyze the data in the CSV file to get a summary of unique values and their counts.
This script reads a CSV file, processes specific columns to find unique values,
and prints the results. It also handles multi-valued columns by splitting them into individual tokens.
"""
import pandas as pd, os, json, textwrap

df = pd.read_csv('data/ppl_peoplesay.csv')
cols = [
    "Data Type [web]",
    "Language [web]",
    # "Data Unit Title [web]",
    # "Subtopics [web]", # multi
    # "Topics [web]", # multi
    "Participant Type [web]",
    # "Participant Name [web]",
    "Age [web]",
    # "Insurance [web]", # multi
    "Income Range (FPL) [web]",
    "Location Type [web]",
    # "Participant Short Code [web]",
    "State [web]",
    # "Race/Ethnicity [web]", # multi
    "Gender [web]",
    # "Profile Picture [web]",
    "Year Conducted Research [web]",
    # "Common Topics [web]", # multi
    # "Life Timeline [web]",
    # "Out Links", # multi
    # "Related Studies [web]",
    # "Full Transcript [web]",
]
multi_cols = [
    "Subtopics [web]", # multi
    "Topics [web]", # multi
    "Insurance [web]", # multi
    "Race/Ethnicity [web]", # multi
    "Common Topics [web]", # multi
    "Out Links", # multi
]

unique_vals = {col: sorted({str(x).strip() for x in df[col].dropna().unique()}) for col in cols}
summary = {col: len(vals) for col, vals in unique_vals.items()}
print(summary)

for col, vals in unique_vals.items():
    print(f"{col}: {len(vals)}")
    print(f"{col}: {vals}")


split_categories = {}
for col in multi_cols:
    tokens = set()
    for val in df[col].dropna().unique():
        for tok in str(val).split(','):
            tok = tok.strip()
            if tok:
                tokens.add(tok)
    split_categories[col] = sorted(tokens)
    print(f"{col}: {len(tokens)}")
    print(f"{col}: {split_categories[col]}")
