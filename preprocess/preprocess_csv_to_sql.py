import pandas as pd
from sqlalchemy import create_engine
import json
import re

# Read CSV with proper delimiter and quote handling
df = pd.read_csv('data/ppl_peoplesay.csv', delimiter=',', quotechar='"', encoding='utf-8')

# Generate a unique 'entry_id'
df['entry_id'] = range(1, len(df) + 1)

# Replace the simple string split with regex pattern matching that preserves bracketed entries
def smart_split(text):
    if pd.isna(text):
        return []

    # First fix any malformed entries with quotes
    text = text.replace('"Dental, Vision, and Hearing Care [5]"', 'Dental Vision and Hearing Care [5]')

    # Split by commas
    items = [item.strip() for item in text.split(',')]

    # Remove any empty items
    return [item for item in items if item]

# Split comma-separated fields into lists
df['subtopics_list'] = df['Subtopics [web]'].apply(smart_split)
df['topics_list'] = df['Topics [web]'].str.split(',')
df['common_topics_list'] = df['Common Topics [web]'].str.split(',')
df['data_type_list'] = df['Data Type [web]'].str.split(',')
df['insurance_list'] = df['Insurance [web]'].str.split(',')
df['race_ethnicity_list'] = df['Race/Ethnicity [web]'].str.split(',')
df['out_links_list'] = df['Out Links'].apply(lambda x: [link.strip() for link in x.split(',')] if pd.notna(x) else [])

# Create SQLite engine
engine = create_engine('sqlite:///peoplesay.db')

# Insert main table (excluding multi-valued columns)
df_main = df[['entry_id', 'Data Unit [web]', 'Language [web]', 'Data Unit Title [web]',
              'Participant Type [web]', 'Participant Name [web]', 'Age [web]',
              'Income Range (FPL) [web]', 'Location Type [web]', 'Participant Short Code [web]',
              'State [web]', 'Gender [web]', 'Profile Picture [web]', 'Year Conducted Research [web]',
              'Full Transcript [web]']].copy()
df_main.columns = ['entry_id', 'data_unit', 'language', 'data_unit_title',
                    'participant_type', 'participant_name', 'age',
                    'income_range_fpl', 'location_type', 'participant_short_code',
                    'state', 'gender', 'profile_picture_url', 'year_conducted_research',
                    'full_transcript']
df_main.to_sql('peoplesay', con=engine, if_exists='replace', index=False)

# Insert subtopics_table
subtopics_df = df[['entry_id', 'subtopics_list']].copy()
subtopics_df.columns = ['entry_id', 'subtopics']
subtopics_df = subtopics_df.explode('subtopics')
subtopics_df = subtopics_df[subtopics_df['subtopics'].notna()]
subtopics_df.to_sql('subtopics_table', con=engine, if_exists='replace', index=False)

# Insert topics_table
topics_df = df[['entry_id', 'topics_list']].copy()
topics_df.columns = ['entry_id', 'topics']
topics_df = topics_df.explode('topics')
topics_df = topics_df[topics_df['topics'].notna()]
topics_df.to_sql('topics_table', con=engine, if_exists='replace', index=False)

# Insert common_topics_table
common_topics_df = df[['entry_id', 'common_topics_list']].copy()
common_topics_df.columns = ['entry_id', 'common_topics']
common_topics_df = common_topics_df.explode('common_topics')
common_topics_df = common_topics_df[common_topics_df['common_topics'].notna()]
common_topics_df.to_sql('common_topics_table', con=engine, if_exists='replace', index=False)

# Insert data_type_table
data_type_df = df[['entry_id', 'data_type_list']].copy()
data_type_df.columns = ['entry_id', 'data_type']
data_type_df = data_type_df.explode('data_type')
data_type_df = data_type_df[data_type_df['data_type'].notna()]
data_type_df.to_sql('data_type_table', con=engine, if_exists='replace', index=False)

# Insert insurance_table
insurance_df = df[['entry_id', 'insurance_list']].copy()
insurance_df.columns = ['entry_id', 'insurance']
insurance_df = insurance_df.explode('insurance')
insurance_df = insurance_df[insurance_df['insurance'].notna()]
insurance_df.to_sql('insurance_table', con=engine, if_exists='replace', index=False)

# Insert race_ethnicity_table
race_ethnicity_df = df[['entry_id', 'race_ethnicity_list']].copy()
race_ethnicity_df.columns = ['entry_id', 'race_ethnicity']
race_ethnicity_df = race_ethnicity_df.explode('race_ethnicity')
race_ethnicity_df = race_ethnicity_df[race_ethnicity_df['race_ethnicity'].notna()]
race_ethnicity_df.to_sql('race_ethnicity_table', con=engine, if_exists='replace', index=False)

# # Insert out_links_table
# out_links_df = df[['entry_id', 'out_links_list']].copy()
# out_links_df.columns = ['entry_id', 'out_link']
# out_links_df = out_links_df.explode('out_link')
# out_links_df = out_links_df[out_links_df['out_link'].notna()]
# out_links_df.to_sql('out_links_table', con=engine, if_exists='replace', index=False)


# Extract unique values for LLM
all_subtopics = set(subtopics_df['subtopics'].dropna())
all_topics = set(topics_df['topics'].dropna())
all_common_topics = set(common_topics_df['common_topics'].dropna())
all_data_types_exploded = set(data_type_df['data_type'].dropna())
all_insurance = set(insurance_df['insurance'].dropna())
all_race_ethnicity = set(race_ethnicity_df['race_ethnicity'].dropna())
# all_out_links = set(out_links_df['out_link'].dropna())
all_languages = set(df_main['language'].dropna())
all_participant_types = set(df_main['participant_type'].dropna())

unique_age = set(df_main['age'].dropna())
unique_income_range_fpl = set(df_main['income_range_fpl'].dropna())
unique_location_type = set(df_main['location_type'].dropna())
unique_state = set(df_main['state'].dropna())
unique_gender = set(df_main['gender'].dropna())
unique_year_conducted_research = set(df_main['year_conducted_research'].dropna())
# unique_data_type_main = set(df_main['data_type'].dropna()) # Unique values from the main table

# Save unique labels to a file
with open('unique_labels.txt', 'w') as f:
    f.write('Age: ' + ', '.join(sorted(unique_age)) + '\n')
    f.write('Income Range (FPL): ' + ', '.join(sorted(unique_income_range_fpl)) + '\n')
    f.write('Location Type: ' + ', '.join(sorted(unique_location_type)) + '\n')
    f.write('State: ' + ', '.join(sorted(unique_state)) + '\n')
    f.write('Gender: ' + ', '.join(sorted(unique_gender)) + '\n')
    f.write('Year Conducted Research: ' + ', '.join(map(str, sorted(unique_year_conducted_research))) + '\n')
    f.write('Subtopics: ' + ', '.join(sorted(all_subtopics)) + '\n')
    f.write('Topics: ' + ', '.join(sorted(all_topics)) + '\n')
    f.write('Common Topics: ' + ', '.join(sorted(all_common_topics)) + '\n')
    f.write('Data Types: ' + ', '.join(sorted(all_data_types_exploded)) + '\n')
    f.write('Insurance: ' + ', '.join(sorted(all_insurance)) + '\n')
    f.write('Race/Ethnicity: ' + ', '.join(sorted(all_race_ethnicity)) + '\n')
    # f.write('Out Links: ' + ', '.join(sorted(all_out_links)) + '\n')
    f.write('Language: ' + ', '.join(sorted(all_languages)) + '\n')
    f.write('Participant Type: ' + ', '.join(sorted(all_participant_types)) + '\n')

print("Data cleaned and loaded into SQLite database. Unique labels saved to unique_labels.txt")