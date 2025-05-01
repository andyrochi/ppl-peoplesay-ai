import os
import pandas as pd
from sqlalchemy import create_engine
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_database(force_rebuild=False):
    """
    Initialize the SQLite database from the CSV file.
    
    Args:
        force_rebuild: If True, rebuild the database even if it already exists
    
    Returns:
        bool: True if database was created or already existed, False if there was an error
    """
    db_path = "peoplesay.db"
    csv_path = "data/ppl_peoplesay.csv"
    
    # Check if database already exists and is not empty
    if not force_rebuild and os.path.exists(db_path) and os.path.getsize(db_path) > 0:
        logging.info(f"Database {db_path} already exists, skipping initialization")
        return True
    
    # Check if CSV file exists
    if not os.path.exists(csv_path):
        logging.error(f"CSV file {csv_path} not found. Database initialization failed.")
        return False
    
    logging.info(f"Initializing database from {csv_path}...")
    
    try:
        # Read CSV with proper delimiter and quote handling
        df = pd.read_csv(csv_path, delimiter=',', quotechar='"', encoding='utf-8')
        
        # Generate a unique 'entry_id'
        df['entry_id'] = range(1, len(df) + 1)
        
        # Define smart_split function
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
        engine = create_engine(f'sqlite:///{db_path}')
        
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
        
        # Insert auxiliary tables
        for field, table_name in [
            ('subtopics_list', 'subtopics_table'),
            ('topics_list', 'topics_table'),
            ('common_topics_list', 'common_topics_table'),
            ('data_type_list', 'data_type_table'),
            ('insurance_list', 'insurance_table'),
            ('race_ethnicity_list', 'race_ethnicity_table'),
        ]:
            col_name = field.replace('_list', '')
            aux_df = df[['entry_id', field]].copy()
            aux_df.columns = ['entry_id', col_name]
            aux_df = aux_df.explode(col_name)
            aux_df = aux_df[aux_df[col_name].notna()]
            aux_df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        
        logging.info(f"Database {db_path} successfully initialized")
        return True
        
    except Exception as e:
        logging.error(f"Error initializing database: {e}")
        return False