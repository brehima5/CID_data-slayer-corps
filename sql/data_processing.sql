-- This is just an EXAMPLE to show dimension vs fact tables.  This example will not run.
-- The goal is to get an understanding of how to make a star schema database. Do your research.
-- This is ran after the create_schema.py source file 


-- **************************************************************************
-- EXAMPLE SQL SCRIPT: data_processing.sql (do NOT RUN it is only an example using DATA you do not have)
-- PURPOSE: Defines the Star Schema and runs non-visual EDA queries.
-- TARGET DATABASE: SQLite (hpd_datathon.db)
-- **************************************************************************

-- ##########################################################################
-- STEP 1: CREATE DIMENSION TABLES (Define the 'Who, Where, When, What')
-- These tables store unique, descriptive attributes.
-- They MUST be created before the fact table due to foreign key constraints.
-- ##########################################################################

-- DIMENSION TABLE: dim_building
-- Grain: One row per unique building (identified by BBL).
CREATE TABLE dim_building (
    building_id INTEGER PRIMARY KEY,   -- Surrogate Key (Generated in Python)
    bbl INTEGER NOT NULL,
    borough TEXT,
    zip_code INTEGER);

-- --------------------------------------------------------------------------

-- DIMENSION TABLE: dim_violation_type
-- Grain: One row per unique violation class and description combination.
CREATE TABLE dim_violation_type (
    violation_type_id INTEGER PRIMARY KEY, -- Surrogate Key 
    violation_class TEXT NOT NULL,         -- e.g., 'A', 'B', 'C', 'I'
    violation_description TEXT,
    severity_rank INTEGER                  -- Engineered Measure (1-4)
);

-- --------------------------------------------------------------------------

-- DIMENSION TABLE: dim_date
-- Grain: One row per unique date (for time-based analysis).
CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,        -- Surrogate Key (e.g., YYYYMMDD)
    full_date DATE NOT NULL,
    year INTEGER,
    month INTEGER,
    is_weekend INTEGER
);


-- ##########################################################################
-- STEP 2: CREATE FACT TABLE
-- This central table contains the core measures and Foreign Keys (FKs).
-- Grain: One row = One Housing Violation event.
-- ##########################################################################

CREATE TABLE fact_violations (
    violation_id INTEGER PRIMARY KEY,  -- Primary Key (from the dataset)
    
    -- FOREIGN KEYS: Connects the fact to the dimensions
    building_id INTEGER,
    date_id INTEGER, 
    violation_type_id INTEGER,
    
    -- MEASURES (Metrics for analysis)
    is_open INTEGER NOT NULL,        -- 1 if open, 0 if closed
    days_open INTEGER,               -- Calculated measure
    
    -- DEFINE FOREIGN KEY CONSTRAINTS
    FOREIGN KEY (building_id) REFERENCES dim_building(building_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (violation_type_id) REFERENCES dim_violation_type(violation_type_id)
);

-- 

-- ##########################################################################
-- STEP 3: DATA INSERTION THERE ARE OTHER WAYS TO DO THIS (Conceptual - Actual loading depends on the tool)
-- AFTER the tables are created, data from the Python-prepped CSVs must be loaded.
-- This is typically done using SQLite's command-line '.import' or a Python 'to_sql' script.
-- ##########################################################################

-- Example for SQLite Command Line:
-- .mode csv
-- .import 'data/processed/dim_building.csv' dim_building
-- .import 'data/processed/fact_violations.csv' fact_violations

-- ##########################################################################
-- STEP 4: NON-VISUAL EDA & AGGREGATION QUERIES (Mandatory Deliverable)
-- These queries verify structure, run initial stats, and highlight group differences.
-- This is a low-cost analysis to guide the subsequent modeling effort.
-- ##########################################################################

-- EXAMPLE 1: Check the total number of open violations by zip code
SELECT
    t1.zip_code,
    SUM(t2.is_open) AS total_open_violations
FROM
    dim_building t1
JOIN
    fact_violations t2 ON t1.building_id = t2.building_id
GROUP BY
    t1.zip_code
ORDER BY
    total_open_violations DESC
LIMIT 10;