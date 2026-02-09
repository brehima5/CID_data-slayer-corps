-- Creating dim_environment_table
CREATE TABLE dim_environment (
    DBN TEXT PRIMARY KEY,
    school_name TEXT,
    enrollment INTEGER,
    instruction_performance_rating TEXT,
    teaching_environment_pct_positive REAL CHECK (
        teaching_environment_pct_positive BETWEEN 0 AND 100
    ),
    family_involvement_pct_positive REAL CHECK (
        family_involvement_pct_positive BETWEEN 0 AND 100
    ),
    advising_planning_pct_positive REAL CHECK (
        advising_planning_pct_positive BETWEEN 0 AND 100
    ),
    economic_need_index REAL CHECK (
        economic_need_index BETWEEN 0 AND 1
    ),
    percent_temp_housing REAL CHECK (
        percent_temp_housing BETWEEN 0 AND 100
    ),
    percent_hra_eligible REAL CHECK (
        percent_hra_eligible BETWEEN 0 AND 100
    ),
    avg_student_attendance REAL CHECK (
        avg_student_attendance BETWEEN 0 AND 100
    )
);

-- Populating dim environment
INSERT INTO dim_environment (
    DBN,
    school_name,
    enrollment,
    instruction_performance_rating,
    teaching_environment_pct_positive,
    family_involvement_pct_positive,
    advising_planning_pct_positive,
    economic_need_index,
    percent_temp_housing,
    percent_hra_eligible,
    avg_student_attendance
)
SELECT 
    DBN,
    "School Name",
    Enrollment,
    "instruction and Performance - Rating",
	"Teaching Environment - School Percent Positive",
	"Family Involvement - School Percent Positive", 
	"Advising and Planning - School Percent Positive",
   "Economic Need Index",
    "Percent in Temp Housing",
    "Percent HRA Eligible",
    "Average Student Attendance"
FROM env_dim;

-- creating dim_location
CREATE TABLE dim_location (
    DBN TEXT PRIMARY KEY,
    school_name TEXT NOT NULL,
    borough TEXT CHECK (
        borough IN ('Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island')
    ),
    district INTEGER,
    school_identifier INTEGER,
    latitude REAL CHECK (
        latitude BETWEEN -90 AND 90
    ),
    longitude REAL CHECK (
        longitude BETWEEN -180 AND 180
    ),
    geometry TEXT,
    FOREIGN KEY (DBN)
        REFERENCES dim_environment (DBN)
);


--populating dim location
INSERT INTO dim_location (
    DBN,
    school_name,
    borough,
    district,
    school_identifier,
    latitude,
    longitude,
    geometry
)
SELECT
    DBN,
    "school Name",
    borough,
    district,
    school_indentifier,
    Latitude,
    Longitude,
    geometry
FROM location_dim;

--creating dim_demographic
CREATE TABLE dim_demographic (
    DBN TEXT NOT NULL,
    Subgroup TEXT NOT NULL,
    nearby_student_percent REAL CHECK (
        nearby_student_percent BETWEEN 0 AND 100
    ),
    pct_students_advanced_courses REAL CHECK (
        pct_students_advanced_courses BETWEEN 0 AND 100
    ),
    student_percent REAL CHECK (
        student_percent BETWEEN 0 AND 100
    ),
    teacher_percent REAL CHECK (
        teacher_percent BETWEEN 0 AND 100
    ),
   PRIMARY KEY (DBN, Subgroup),
    FOREIGN KEY (DBN)
        REFERENCES dim_environment (DBN)
);

---- Populate dim_demographic
INSERT INTO dim_demographic (
    DBN,
    Subgroup,
    nearby_student_percent,
    pct_students_advanced_courses,
    student_percent,
    teacher_percent
)
SELECT DISTINCT
    DBN,
    Subgroup,
    Nearby_Student_Percent,
    Percentage_of_Students_Enrolled_in_Advanced_Courses,
    Student_Percent,
    Teacher_Percent
FROM demog_dim;

-- Creating fact_school_outcome
CREATE TABLE fact_school_outcomes (
			--Columns
	fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    DBN TEXT NOT NULL,
    Subgroup TEXT NOT NULL,
    n_count_ccr INTEGER,
    ccr_rate REAL,
    n_count_graduation_rate INTEGER,
    graduation_rate REAL,
    n_count_hs_persistence_rate INTEGER,
    hs_persistence_rate REAL,
    n_count_90pct_attendance INTEGER,
    attendance_90pct_rate REAL,
    n_count_enrollment INTEGER,
    enrollment_rate REAL,
    readiness_gap REAL,
	
    -- grain enforcement
    UNIQUE (DBN, Subgroup),
	
	  -- dimension relationships
    FOREIGN KEY (DBN)
        REFERENCES dim_environment (DBN),
    FOREIGN KEY (DBN, Subgroup)
        REFERENCES dim_demographic (DBN, Subgroup)
);
-- populating fact table
INSERT INTO fact_school_outcomes (
    DBN,
    Subgroup,
    n_count_ccr,
    ccr_rate,
    n_count_graduation_rate,
    graduation_rate,
    n_count_hs_persistence_rate,
    hs_persistence_rate,
    n_count_90pct_attendance,
    attendance_90pct_rate,
    n_count_enrollment,
    enrollment_rate,
    readiness_gap
)
SELECT
    DBN,
    Subgroup,
    n_count_ccr,
    ccr_rate,
    n_count_graduation_rate,
    graduation_rate,
    n_count_hs_persistence_rate,
    hs_persistence_rate,
    n_count_90pct_attendance,
    "90pct_attendance_rate",
    n_count_enrollment,
    enrollment_rate,
    readiness_gap
FROM fact_table;
