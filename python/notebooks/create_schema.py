import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

path = "/Users/Marcy_Student/Desktop/CID_data-slayer-corps/data/Relational_Tables.xlsx"

# Fact table loading
fact_table = pd.read_excel(path, sheet_name=2)
fact_table.head()

# demographic table loading
demog_dim = pd.read_excel(path, sheet_name=3)

# environment table loading
env_dim = pd.read_excel(path, sheet_name=4)

# location table loading
location_dim = pd.read_excel(path, sheet_name=5)


columns_names = fact_table.columns.tolist() + demog_dim.columns.tolist() + env_dim.columns.tolist() + location_dim.columns.tolist()
print("Column Names:")
for col in columns_names:
    print(f"  {col}")

# Rename columns in fact table
fact_table.rename(columns={
    '4Year_College_and_Career_Readiness_N_count': 'n_count_ccr',
    '4Year_College_and_Career_Readiness_Metric_Value': 'ccr_rate',
    '4Year_Graduation_Rate_N_count': 'n_count_graduation_rate',
    '4Year_Graduation_Rate_Metric_Value': 'graduation_rate',
    '4Year_High_School_Persistence_Rate_N_count': 'n_count_hs_persistence_rate',
    '4Year_High_School_Persistence_Rate_Metric_Value': 'hs_persistence_rate',
    'Percentage_of_Students_with_gt90pct_Attendance_N_count': 'n_count_90pct_attendance',
    'Percentage_of_Students_with_gt90pct_Attendance_Metric_Value': '90pct_attendance_rate',
    'Postsecondary_Enrollment_Rate__6_Months_N_count': 'n_count_enrollment',
    'Postsecondary_Enrollment_Rate__6_Months_Metric_Value': 'enrollment_rate'
}, inplace=True)

fact_table.head()

# Fact table cleaning
# Update datatypes with error coercion
fact_table['n_count_ccr'] = pd.to_numeric(fact_table['n_count_ccr'], errors='coerce').astype('Int64')
fact_table['ccr_rate'] = pd.to_numeric(fact_table['ccr_rate'], errors='coerce').astype(float)
fact_table['n_count_graduation_rate'] = pd.to_numeric(fact_table['n_count_graduation_rate'], errors='coerce').astype('Int64')
fact_table['graduation_rate'] = pd.to_numeric(fact_table['graduation_rate'], errors='coerce').astype(float)
fact_table['n_count_hs_persistence_rate'] = pd.to_numeric(fact_table['n_count_hs_persistence_rate'], errors='coerce').astype('Int64')
fact_table['hs_persistence_rate'] = pd.to_numeric(fact_table['hs_persistence_rate'], errors='coerce').astype(float)
fact_table['n_count_90pct_attendance'] = pd.to_numeric(fact_table['n_count_90pct_attendance'], errors='coerce').astype('Int64')
fact_table['90pct_attendance_rate'] = pd.to_numeric(fact_table['90pct_attendance_rate'], errors='coerce').astype(float)
fact_table['n_count_enrollment'] = pd.to_numeric(fact_table['n_count_enrollment'], errors='coerce').astype('Int64')
fact_table['enrollment_rate'] = pd.to_numeric(fact_table['enrollment_rate'], errors='coerce').astype(float)

# Convert ccr_rate from percentage to proportion
fact_table['ccr_rate'] = fact_table['ccr_rate'] / 100
fact_table.dtypes

display(fact_table.head())

fact_table.isna().sum()
fact_table.shape

# demographic table cleaning
demog_dim.columns

cols = ['Nearby_Student_Percent',
       'Percentage_of_Students_Enrolled_in_Advanced_Courses',
       'Student_Percent', 'Teacher_Percent']

for col in cols:
    demog_dim[col] = pd.to_numeric(demog_dim[col],errors='coerce')
demog_dim.dtypes

# environment table cleaning
env_dim.dtypes
env_dim.columns

cols = ['Teaching Environment - School Percent Positive',
       'Family Involvement - School Percent Positive', 'Economic Need Index',
       'Percent in Temp Housing', 'Percent HRA Eligible',
       'Average Student Attendance',
       'Advising and Planning - School Percent Positive']
for col in cols:
    env_dim[col] = pd.to_numeric(env_dim[col],errors='coerce')
env_dim.dtypes
env_dim.head()

# Location table
location_dim.dtypes # Looks perfect

# 1. READINESS GAP
fact_table['readiness_gap'] = fact_table['graduation_rate'] - fact_table['ccr_rate']

# 2. 

# Create unique identifier (primary key)
demog_dim['subgroup_id'] = demog_dim['DBN'] + '_' + demog_dim['Subgroup']

# Move subgroup_id to first column
cols = ['subgroup_id'] + [col for col in demog_dim.columns if col != 'subgroup_id']
demog_dim = demog_dim[cols]
demog_dim.head()