--Count of Schools per Borough
SELECT borough, COUNT(*) AS count_of_schools
FROM dim_location
GROUP BY borough
ORDER BY COUNT(*) DESC;
-- Bronx has most amount of schools, Staten Island has lowest (expected) followed by Queens.


-- Instructor Performance Counts per Borough
WITH cte AS (
SELECT *
FROM dim_environment e
JOIN dim_location l
ON e.DBN = l.DBN
)
SELECT borough, instruction_performance_rating, COUNT(instruction_performance_rating) AS performance_groups
FROM cte
WHERE instruction_performance_rating IS NOT NULL
GROUP BY borough, instruction_performance_rating;
-- Queens & Staten Island have no school performances that "need improvement"
-- Brooklyn has the most "needs improvement", with 7 schools.

