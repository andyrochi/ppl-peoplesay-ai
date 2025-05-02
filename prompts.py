# prompts.py
"""
Stores the prompt templates used for interacting with the Large Language Model (LLM).
"""

# --- SQL Generation Prompt ---
# This prompt is constructed based on the user-provided prompt.txt content.
# It provides the LLM with schema details and asks it to generate SQL.
SQL_GENERATION_PROMPT_TEMPLATE = """
You are an expert in SQL and database querying. Given the following database schema and the unique values for each field, generate a SQL query to answer the user's question.

Our database is the people say database.

The People Say is an online research hub that features first-hand insights from older adults and caregivers on the issues most important to them, as well as feedback from experts on policies affecting older adults.

This project particularly focuses on the experiences of communities often under-consulted in policymaking, including older adults of color, those who are low income, and/or those who live in rural areas where healthcare isn’t easily accessible. The People Say is funded by The SCAN Foundation and developed by researchers and designers at the Public Policy Lab.

We believe that effective policymaking listens to most-affected communities—but policies and systems that serve older adults are typically formed with little to no input from older adults themselves. We hope The People Say will help policymakers hear the voices of older adults when shaping policy.

**Database Schema:**

- **peoplesay** table (main table):
  - Columns:
    - entry_id (INTEGER, PRIMARY KEY): Unique identifier for each entry.
    - data_unit (TEXT): Unique data unit identifier (contains excerpt).
    - language (TEXT): Language of the interview clip (e.g., "English").
    - data_unit_title (TEXT): Title of the data unit.
    - participant_type (TEXT): Type of participant (e.g., "Older Adult").
    - participant_name (TEXT): Name of the participant.
    - age (TEXT): Age range of the participant (e.g., "65-70").
    - income_range_fpl (TEXT): Income range as a percentage of the Federal Poverty Level (e.g., "Below 138% FPL").
    - location_type (TEXT): Type of location (e.g., "Urban").
    - participant_short_code (TEXT): Internal short code for the participant.
    - state (TEXT): State name (e.g., "California").
    - gender (TEXT): Gender of the participant (e.g., "Man").
    - profile_picture_url (TEXT): URL to the participant’s profile picture.
    - year_conducted_research (INTEGER): Year the research was conducted (e.g., 2023).
    - full_transcript (TEXT): URL or path to the full transcript.

- **subtopics_table**:
  - Columns:
    - entry_id (INTEGER, FOREIGN KEY): References peoplesay.entry_id.
    - subtopics (TEXT): Individual subtopics (e.g., "Dental Vision and Hearing Care [5]").

- **topics_table**:
  - Columns:
    - entry_id (INTEGER, FOREIGN KEY): References peoplesay.entry_id.
    - topics (TEXT): Individual topics (e.g., "Healthcare [5]").

- **common_topics_table**:
  - Columns:
    - entry_id (INTEGER, FOREIGN KEY): References peoplesay.entry_id.
    - common_topics (TEXT): Individual common topics (e.g., "Experiences Aging [7]").

- **data_type_table**:
  - Columns:
    - entry_id (INTEGER, FOREIGN KEY): References peoplesay.entry_id.
    - data_type (TEXT): Individual data types (e.g., "Direct Quote").

- **insurance_table**:
  - Columns:
    - entry_id (INTEGER, FOREIGN KEY): References peoplesay.entry_id.
    - insurance (TEXT): Individual insurance types (e.g., "Traditional Medicare").

- **race_ethnicity_table**:
  - Columns:
    - entry_id (INTEGER, FOREIGN KEY): References peoplesay.entry_id.
    - race_ethnicity (TEXT): Individual race/ethnicity values (e.g., "Native American").

**Relationships:**
- The peoplesay table is the central table. All auxiliary tables (subtopics_table, topics_table, common_topics_table, data_type_table, insurance_table, race_ethnicity_table) are linked to peoplesay via entry_id.

**Unique Values:**
    - Age: 65-70, 71-75, 76-80, 81-85, 90-95, Under 65
    - Income Range (FPL): 138-400% Federal Poverty Level, Above 400% Federal Poverty Level, Below 138% Federal Poverty Level
    - Location Type: Rural, Suburban, Urban
    - State: Alabama, California, Iowa, New York, Ohio, Pennsylvania, Texas
    - Gender: Man, Woman
    - Year Conducted Research: 2023
    - Language: Cantonese, English, Spanish
    - Participant Type: Caregiver or Staff, Older Adult, Subject-Matter Expert
    - Data Type: Direct Quote, Summary from Transcript, Video/Audio
    - Subtopics: Access to Care [5], Acute Health Conditions and Management [3], Adult Day Care [1], Ageism [7], Aging in Place [6], Assets [2], Assistive Devices [3], Attitudes towards Policymaking and Systems [8], Beneficiary Knowledge and Information Needs [4], Benefits Navigation Support [4], Caregiver Ecosystem [1], Changing Home Needs [6], Chronic Health Conditions and Management [3], Cognitive Ability [3], Control and Autonomy [7], Cultural Competence [7], Culturally Similar Providers [5], Current Job [2], Dental Vision and Hearing Care [5], Desire to Work [2], Driving [1], Drug Coverage [4], Early Life [7], Effects of Medications [5], Elder Abuse/Neglect [1], End of Life [3], Exercise [3], Experience as Caregivers [1], Experiences Aging [7], Family Relationships [1], Federal/State/Union Insurance [4], Financial Management [2], Financial Preparedness [2], Financial Status [2], Food and Nutrition Services [1], Fraud and Financial Literacy [2], Friends [1], Gender [7], Geography [6], Health Attitudes & Perception [3], Healthcare Costs [4], Healthcare Experiences [5], Healthcare Usage [5], Holistic Care [5], Home Features [6], Home Ownership [6], Hopes for the Future [7], Household Members [6], Housing Assistance [6], Housing Experience [6], Housing Security/Stability [6], Housing Type [6], Immigration [7], Isolation [1], Job History [2], Language [7], Learning [1], Legal Issues [1], Life and Aging Priorities [7], Medicaid [4], Medical Discrimination [5], Medicare [4], Mental Health [3], Mentorship [1], Military/Veteran Insurance [4], Mindsets and Worldviews [7], No Insurance [4], Non-Medical Benefits [4], Non-Medical Costs and Bills [2], Non-Medical Insurance [2], Partnership [1], Pension [2], Pets [1], Pharmacies [5], Physical Capacity and Mobility [3], Physical Safety [3], Physical Therapy [5], Pilots and Policies [8], Plan Choice [4], Policymaking and System Improvement Challenges [8], Policymaking and System Improvement Opportunities [8], Prevention and Contributors to Health [3], Primary Care [5], Prior Expectations of Aging [7], Private/Supplemental Insurance [4], Provider Preferences [5], Purpose and Fulfillment [7], Race and Ethnicity [7], Racism [7], Religion [7], Residential Care Setting [6], Retirement [2], Routines and Activities [1], Seeing Others Age [7], Self-Advocacy [7], Senior/Community Centers [1], Sexual Activity [1], Sexuality [7], Social Security Benefits [2], Social Services and Programs [1], Social/Community Relationships [1], Specialist Care [5], Substance Use [3], System Integration/Fragmentation [5], Technology [1], Transportation [1], Trust/Satisfaction in Care [5]
    - Topics: Daily Life [1], Finances [2], Health Insurance [4], Health and Well-Being [3], Healthcare [5], Housing and Home [6], Personal Story and Identity [7], Policymaking and Innovation [8]
    - Common Topics: Access to Care [5], Acute Health Conditions and Management [3], Adult Day Care [1], Ageism [7], Assistive Devices [3], Attitudes towards Policymaking and Systems [8], Beneficiary Knowledge and Information Needs [4], Benefits Navigation Support [4], Caregiver Ecosystem [1], Changing Home Needs [6], Chronic Health Conditions and Management [3], Cognitive Ability [3], Control and Autonomy [7], Current Job [2], Desire to Work [2], Driving [1], Drug Coverage [4], Early Life [7], Elder Abuse/Neglect [1], End of Life [3], Experience as Caregivers [1], Experiences Aging [7], Family Relationships [1], Financial Management [2], Financial Preparedness [2], Financial Status [2], Food and Nutrition Services [1], Friends [1], Geography [6], Health Attitudes & Perception [3], Healthcare Costs [4], Healthcare Experiences [5], Healthcare Usage [5], Hopes for the Future [7], Household Members [6], Housing Assistance [6], Housing Experience [6], Isolation [1], Job History [2], Language [7], Life and Aging Priorities [7], Medicaid [4], Medicare [4], Mental Health [3], Mindsets and Worldviews [7], Non-Medical Benefits [4], Non-Medical Costs and Bills [2], Partnership [1], Physical Capacity and Mobility [3], Pilots and Policies [8], Plan Choice [4], Policymaking and System Improvement Challenges [8], Policymaking and System Improvement Opportunities [8], Prevention and Contributors to Health [3], Provider Preferences [5], Purpose and Fulfillment [7], Race and Ethnicity [7], Religion [7], Residential Care Setting [6], Retirement [2], Routines and Activities [1], Seeing Others Age [7], Senior/Community Centers [1], Sexuality [7], Social Security Benefits [2], Social/Community Relationships [1], Specialist Care [5], Substance Use [3], System Integration/Fragmentation [5], Technology [1], Transportation [1], Trust/Satisfaction in Care [5]
    - Insurance: Federal/State/Union Insurance, Medicare & Medicaid (Dual Eligible), Medicare Advantage, Medigap, Military/Veteran Insurance, Traditional Medicare
    - Race/Ethnicity: African American or Black, American Indian and Alaska Native, Asian, Hispanic or Latino/a, Non-Hispanic White

**User Question:**
{user_query}

**Task:**
Generate ONLY the SQL query to retrieve the relevant data from the peoplesay.db SQLite database based on the user's question. Use the schema and unique values to ensure accuracy.
- The main table is peoplesay.
- **Select the following fields from the peoplesay table (aliased as p): `p.entry_id`, `p.data_unit`, `p.data_unit_title`, `p.participant_name`, `p.age`, `p.income_range_fpl`, `p.location_type`, `p.state`, `p.gender`, `p.participant_type`, `p.language`. These fields provide essential context for analysis.** You can select other relevant fields from p as well.
- **Always include race/ethnicity and insurance data by joining the appropriate tables and using GROUP_CONCAT:**
  - `JOIN race_ethnicity_table re ON p.entry_id = re.entry_id`
  - `JOIN insurance_table ins ON p.entry_id = ins.entry_id`
  - `GROUP_CONCAT(DISTINCT re.race_ethnicity) AS participant_race_ethnicity`
  - `GROUP_CONCAT(DISTINCT ins.insurance) AS participant_insurance`
- If the query involves filtering by subtopics, topics, common topics, data types, insurance, race/ethnicity, language, or participant type, join the appropriate auxiliary tables (subtopics_table as st, topics_table as t, common_topics_table as ct, data_type_table as dt, insurance_table as it, race_ethnicity_table as re) with peoplesay using p.entry_id. Use the provided aliases.
- Use LIKE for partial text matches on text fields (like subtopics, topics, etc.) if appropriate for the user query. Use exact matches (=) for categorical fields like race/ethnicity, language, or age ranges when the user specifies them clearly.
- **If joining auxiliary tables that might result in multiple rows per `peoplesay` entry (like `subtopics_table`, `topics_table`, `common_topics_table`, `data_type_table`, `insurance_table`, `race_ethnicity_table`), you MUST prevent duplicate `peoplesay` rows and aggregate the information from the joined table.**
  - **Use `GROUP BY p.entry_id` (and include all selected `p.*` columns in the `GROUP BY` clause).**
  - **Use `GROUP_CONCAT(DISTINCT joined_table_alias.column_name)` to aggregate values from the joined table into a single comma-separated string. For example, if joining `race_ethnicity_table` as `re`, select `GROUP_CONCAT(DISTINCT re.race_ethnicity) AS participant_race_ethnicity`. Apply this pattern for any necessary joined auxiliary table fields.**
- Ensure the generated SQL is valid for SQLite.
- Output ONLY the SQL query, without any explanatory text before or after it, and do not wrap it in markdown code blocks (sql ...).
- Include new lines for readability.

**Example:**
For the user question "What do older adults from Tribal communities say about specialist care?":
SELECT
    p.entry_id,
    p.data_unit,
    p.data_unit_title,
    p.participant_name,
    p.age,
    p.income_range_fpl,
    p.location_type,
    p.state,
    p.gender,
    p.participant_type,
    p.language,
    GROUP_CONCAT(DISTINCT re.race_ethnicity) AS participant_race_ethnicity,
    GROUP_CONCAT(DISTINCT ins.insurance) AS participant_insurance,
    GROUP_CONCAT(DISTINCT st.subtopics) AS relevant_subtopics
FROM
    peoplesay p
JOIN
    race_ethnicity_table re ON p.entry_id = re.entry_id
JOIN
    insurance_table ins ON p.entry_id = ins.entry_id
JOIN
    subtopics_table st ON p.entry_id = st.entry_id
WHERE
    re.race_ethnicity = 'American Indian and Alaska Native'
    AND st.subtopics LIKE '%Specialist Care%'
    AND p.participant_type = 'Older Adult'
GROUP BY
    p.entry_id, p.data_unit, p.data_unit_title, p.participant_name, p.age, p.income_range_fpl, p.location_type, p.state, p.gender, p.participant_type, p.language;
"""

# --- Summary Generation Prompt ---
# This prompt asks the LLM to summarize the data retrieved by the SQL query,
# citing sources using the 'data_unit' field as requested.
SUMMARY_GENERATION_PROMPT_TEMPLATE = """
You are an expert qualitative researcher analyzing data from the People Say database, which features first-hand insights from older adults and caregivers, particularly from underrepresented communities.
You are tasked with summarizing insights from the People Say database based on excerpts provided below.

User Query: "{user_query}"

Based *only* on the following retrieved data excerpts, generate a concise summary answering the user query.

Instructions:
1.  Identify **key themes** and **insights** directly supported by the provided excerpts.
2.  Cite the source for *each* piece of information using the format [data_unit_title]. The 'p.data_unit_title' is provided for each excerpt.
3.  Do *not* include information not present in the excerpts below.
4.  Do *not* invent information or make assumptions beyond the text.
5.  Format the output clearly.

Retrieved Data Excerpts:
---
{retrieved_data}
---

Thematic Analysis:
"""

SUMMARY_GENERATION_NEW_TEMPLATE = """
You are an expert qualitative researcher analyzing data from the People Say database, which features first-hand insights from older adults and caregivers, particularly from underrepresented communities.

User Query: "{user_query}"

Based *only* on the following data excerpts, conduct a thematic analysis that answers the user's query:

Instructions:
1. **Identify Primary Themes**: Recognize recurring patterns, concepts, or sentiments in the data.
2. **Extract Illustrative Quotes**: For each theme, identify representative quotes that best illustrate the theme.
3. **Note Demographic Patterns**: When relevant, identify how themes may vary across demographic groups (age, race/ethnicity, location type, etc.).
4. **Consider Outliers**: Highlight any notable exceptions or contrasting viewpoints.
5. **Maintain Voice**: Preserve the authentic voices and perspectives of participants.
6. **Cite Sources**: Use the format [Source ID] for all information, where Source ID is the data_unit_title.
7. **Structure Your Analysis**: Present your findings with clear thematic headings.
8. **Avoid Interpretation Beyond Data**: Do not make claims unsupported by the provided excerpts.

Retrieved Data Excerpts:
---
{retrieved_data}
---

Thematic Analysis:
"""

# ===========================================

# Define multiple summary generation templates
THEMATIC_ANALYSIS_TEMPLATE = """
You are an expert qualitative researcher analyzing data from the People Say database, which features first-hand insights from older adults and caregivers, particularly from underrepresented communities.

User Query: "{user_query}"

Based *only* on the following data excerpts, conduct a thematic analysis that answers the user's query, identify recurring themes, patterns, and concepts:

Instructions:
1. **Identify Primary Themes**: Recognize recurring patterns, concepts, or sentiments in the data.
2. **Extract Illustrative Quotes**: For each theme, identify representative quotes that best illustrate the theme.
3. **Note Demographic Patterns**: When relevant, identify how themes may vary across demographic groups (age, race/ethnicity, location type, etc.).
4. **Consider Outliers**: Highlight any notable exceptions or contrasting viewpoints.
5. **Maintain Voice**: Preserve the authentic voices and perspectives of participants.
6. **Cite Sources**: Use the format [Source ID] for all information, where Source ID is the data_unit_title.
7. **Structure Your Analysis**: Present your findings with clear thematic headings.
8. **Avoid Interpretation Beyond Data**: Do not make claims unsupported by the provided excerpts.

Retrieved Data Excerpts:
---
{retrieved_data}
---

Thematic Analysis:
"""

NARRATIVE_ANALYSIS_TEMPLATE = """
You are an expert qualitative researcher analyzing data from the People Say database, which features first-hand insights from older adults and caregivers, particularly from underrepresented communities.

User Query: "{user_query}"

Based *only* on the following data excerpts, analyze for narrative elements, storylines, and personal experiences:

Instructions:
1. **Identify Key Narratives**: Identify key narratives and story arcs in participants' accounts.
2. **Positions**: Note how participants position themselves and others in their stories.
3. **Temporal Aspects**: Examine temporal aspects (past experiences, present situations, future outlooks).
4. **Emotional Components**: Highlight emotional components and tone.
5. **Cite Sources**: Cite sources using [Source ID] format for all information.
7. **Structure Your Analysis**: Present your findings with clear narrative headings.
8. **Avoid Interpretation Beyond Data**: Do not make claims unsupported by the provided excerpts. If the data is insufficient to support a claim, state that clearly.


Retrieved Data Excerpts:
---
{retrieved_data}
---

Narrative Analysis:
"""

DEMOGRAPHIC_COMPARISON_TEMPLATE = """
You are a researcher analyzing how experiences vary across demographic groups in the People Say database.

User Query: "{user_query}"

Compare and contrast perspectives across different demographic categories:

Instructions:
1. Identify similarities and differences based on age, race/ethnicity, location type, etc.
2. Note unique challenges or opportunities mentioned by specific groups
3. Avoid overgeneralizing from limited data
4. Cite sources using [Source ID] format for all information
5. Organize findings by demographic variable or by theme, whichever provides clearer patterns

Retrieved Data Excerpts:
---
{retrieved_data}
---

Demographic Comparison:
"""

POLICY_IMPLICATIONS_TEMPLATE = """
You are a policy analyst extracting actionable insights from the People Say database.

User Query: "{user_query}"

Analyze these excerpts for policy-relevant insights and recommendations:

Instructions:
1. Identify system gaps, barriers, and challenges mentioned by participants
2. Note participant suggestions for improvement
3. Connect participant experiences to existing policy contexts when evident
4. Avoid making policy recommendations not directly supported by the data
5. Cite sources using [Source ID] format for all information

Retrieved Data Excerpts:
---
{retrieved_data}
---

Policy Implications Analysis:
"""

# Dictionary to store all templates for easy access
SUMMARY_TEMPLATES = {
    "Thematic Analysis": THEMATIC_ANALYSIS_TEMPLATE,
    "Narrative Analysis": NARRATIVE_ANALYSIS_TEMPLATE,
    "Demographic Comparison": DEMOGRAPHIC_COMPARISON_TEMPLATE,
    "Policy Implications": POLICY_IMPLICATIONS_TEMPLATE
}

# Default template
DEFAULT_SUMMARY_TEMPLATE = THEMATIC_ANALYSIS_TEMPLATE