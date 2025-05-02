## Overview

The **People Say AI Search Tool** is built to make qualitative research data more accessible, transparent, and actionable—without sacrificing rigor. Powered by LLMs and grounded in a carefully tagged, human-curated dataset from the People Say project, the tool is designed to **enhance** the researcher’s workflow—not replace it.

## Why This Tool?

The [**People Say dataset**](https://thepeoplesay.org) is a meticulously curated qualitative resource developed by researchers at [Public Policy Lab (PPL)](https://www.publicpolicylab.org). It comprises nearly 2,400 units of qualitative data derived from over 100 hours of interviews with older adults, caregivers, and subject matter experts. Each data unit is enriched with detailed metadata and tagged using a comprehensive taxonomy of 108 topic and subtopic tags. This taxonomy was developed with reference to major longitudinal studies of American older adults, including:

- The Health and Retirement Survey (HRS)  
- Medicare Current Beneficiary Survey (MCBS)  
- National Health and Aging Trends Study (NHATS)  
- Older Americans 2020: Key Indicators of Well-Being  
- 2023 Profile of Older Americans  

These tags enable researchers to filter and navigate the data effectively, facilitating manual exploration and insight derivation.

Traditionally, exploring this dataset involves:

1. Manually selecting relevant tags (e.g., *Asians*, *Healthcare*), and  
2. Reading through numerous excerpts to synthesize themes and insights.

For instance, if you're investigating:  
**“How do older Asians feel about their access to health care?”**

You might:
- Filter for relevant tags (e.g., *race/ethnicity: Asian*, *topic: healthcare*, *age: 65+*).
- Manually review excerpts across multiple participants.
- Deduce patterns and summarize findings.

### Challenges:
- **Cognitive Load:** Navigating and synthesizing large volumes of qualitative data can be mentally taxing.  
- **Time-Consuming:** Manual review and analysis are labor-intensive processes.  
- **Traceability:** Ensuring that AI-generated summaries are grounded in verifiable data is crucial for research integrity.

---

### How can we make this experience more flexible, without sacrificing rigor?

How can we allow users to explore the dataset through natural questions, while still maintaining the ability to trace every insight back to the original source?

How can we enhance—not replace—the manual process of qualitative analysis?

---

Let us introduce an approach that blends natural language interfaces, structured retrieval, and traceable AI synthesis.

## Core Workflow: From Question to Insight

### 1. Natural Language Query → SQL Generation

- **Problem:** Users come with *questions*, not filter logic.
- **Solution:** You ask in plain English (e.g., *“How do older Asians feel about healthcare?”*).  
  An LLM converts your query into a tailored SQL query based on the People Say database schema.

- **Why this matters:**  
  - No need to understand the database schema.  
  - Queries are displayed for **transparency** and **control**.

### 2. Data Retrieval

- The generated SQL is executed locally to retrieve relevant excerpts and participant metadata (age, race, insurance status, etc.).

- **Why this matters:**  
  - Ensures insights are **grounded in authentic participant voices**.
  - Keeps the process transparent and verifiable.

### 3. Summary Generation & Synthesis

- The retrieved data, your question, and your selected analysis type (e.g., *Thematic*, *Narrative*, *Policy*) are passed to a generative AI model (e.g., Gemini).
- Prompts are crafted to:
  - Identify themes or narratives  
  - Extract illustrative quotes  
  - Compare across demographics (if applicable)  
  - **Cite every insight** with a `[Source ID]`

- **Why this matters:**  
  - **Traceability:** Every insight links to real data.  
  - **Verification:** Expand citations to review full context.  
  - **No Hallucination:** Prompts restrict unsupported claims.

---

## Citation & Source Transparency

- Each summary insight includes a `[Source ID]` citation that maps directly to:
  - The original excerpt  
  - Demographics (age, gender, race/ethnicity, etc.)  
  - Contextual metadata (location, insurance, etc.)  

### Why this matters:
- **Accountability:** Researchers can audit and verify every insight.
- **Rich Context:** Demographics and context aid interpretation.
- **Manual Analysis:** Users can always return to the source.

---

## Responsible AI Use

- **LLM Limitations:** AI-generated summaries are helpful, but **require human review**.
- **Data Privacy:** All excerpts are anonymized and consented.
- **Security:** Your API key is used only during the session and never stored.

---

## Design Philosophy

- **Accessibility:** Enables natural-language querying of complex qualitative data.
- **Flexibility:** Enhances the manual workflow without removing human agency.
- **Transparency:** Shows SQL queries and source citations for every generated insight.
- **Ethical AI:** Designed to minimize hallucinations and respect participant voices.

> ✳️ This tool doesn’t replace human judgment—it augments it with speed, clarity, and traceability.

---

For more details, see the [README](https://github.com/andyrochi/ppl-peoplesay-ai?tab=readme-ov-file) or [project documentation](https://thepeoplesay.org/).