import pandas as pd
import numpy as np
import os
import sqlite3

# --- 1. CONFIGURATION ---
RAW_DATA_PATH = 'data/raw/civic_data_source_1.csv'
DB_NAME = 'hpd_datathon.db'
OUTPUT_DIR = 'data/processed/' # Used for saving cleaned CSVs for SQL loading

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_data_for_star_schema(raw_path):
    # Load the raw data
    try:
        df = pd.read_csv(raw_path)
        print(f"Loaded raw data with {len(df)} rows.")
    except FileNotFoundError:
        print(f"Error: Raw data not found at {raw_path}")
        return None, None, None, None

    # --- 2. DIMENSION GENERATION ---
    
    # 2a. dim_building: Extract unique location attributes and assign a surrogate key
    dim_building_data = df[['Borough', 'BBL', 'ZipCode']].drop_duplicates().reset_index(drop=True)
    dim_building_data['building_id'] = dim_building_data.index + 1  # Surrogate Key
    
    # 2b. dim_violation_type: Extract unique violation classes/descriptions
    dim_violation_type_data = df[['ViolationClass', 'ViolationDescription']].drop_duplicates().reset_index(drop=True)
    dim_violation_type_data['violation_type_id'] = dim_violation_type_data.index + 1 # Surrogate Key
    
    # 2c. dim_date: (Advanced) Students should generate this from unique date columns

    # --- 3. FACT TABLE PREP (Merging Foreign Keys) ---
    
    # Merge the new surrogate keys back into the main DataFrame
    fact_data = df.merge(dim_building_data, on=['Borough', 'BBL', 'ZipCode'], how='left')
    fact_data = fact_data.merge(dim_violation_type_data, on=['ViolationClass', 'ViolationDescription'], how='left')
    
    # Select only the columns needed for the fact table (measures + FKs)
    fact_table = fact_data[['ViolationID', 'building_id', 'violation_type_id', 'ViolationStatus']]
    
    # --- 4. DATA CLEANUP/ENGINEERING (Example: Creating 'is_open' measure) ---
    fact_table['is_open'] = np.where(fact_table['ViolationStatus'] == 'OPEN', 1, 0)
    
    return fact_table, dim_building_data, dim_violation_type_data

if __name__ == '__main__':
    # Replace the example columns with your actual data's column names
    fact_df, dim_b_df, dim_vt_df = process_data_for_star_schema(RAW_DATA_PATH)
    
    if fact_df is not None:
        print("\nSaving processed CSVs for SQL loading...")
        
        # Save the structured dataframes. These will be loaded via the SQL script.
        fact_df.to_csv(os.path.join(OUTPUT_DIR, 'fact_violations.csv'), index=False)
        dim_b_df.to_csv(os.path.join(OUTPUT_DIR, 'dim_building.csv'), index=False)
        dim_vt_df.to_csv(os.path.join(OUTPUT_DIR, 'dim_violation_type.csv'), index=False)
        
        print("Pre-processing complete. Proceed to data_processing.sql.")