# Documentation for Ro's EDA

> !NOTE
> EDA was done in both Jupyter Notebooks and DB_Browser. This page documents EDA done across all interfaces.

## Quick EDA

Tools Utilized:
- SQLite
- Pandas

***

### Schools per Borough

`SELECT borough, COUNT(*) AS count_of_schools
FROM dim_location
GROUP BY borough
ORDER BY COUNT(*) DESC;`

<div align='center'>

This query reveals the the count of schools across all boroughs.

| Borough | Count of Schools | Percentage of Total |
| :--- | :--- | :--- |
| **Bronx** | 143 | 28.3% |
| **Brooklyn** | 139 | 27.5% |
| **Manhattan** | 121 | 23.9% |
| **Queens** | 89 | 17.6% |
| **Staten Island** | 14 | 2.8% |
| **Total** | **506** | **100%** |

</div>

<br>

### Instructor Performance Count per Borough

`WITH cte AS (
SELECT *
FROM dim_environment e
JOIN dim_location l
ON e.DBN = l.DBN
)
SELECT borough, instruction_performance_rating, COUNT(instruction_performance_rating) AS performance_groups
FROM cte
WHERE instruction_performance_rating IS NOT NULL
GROUP BY borough, instruction_performance_rating;`

<div align='center'>

This query gives us the count of instructor performance ratings per borough, per rating label. It gives us a birds-eye view of the instructor ratings across all schools in each borough.

| Borough | Instructor Performance Rating | Count |
| :--- | :--- | :--- |
| **Bronx** | Excellent | 20 |
| **Bronx** | Fair | 53 |
| **Bronx** | Good | 57 |
| **Bronx** | Needs Improvement | 3 |
| **Brooklyn** | Excellent | 16 |
| **Brooklyn** | Fair | 54 |
| **Brooklyn** | Good | 54 |
| **Brooklyn** | Needs Improvement | 7 |
| **Manhattan** | Excellent | 41 |
| **Manhattan** | Fair | 43 |
| **Manhattan** | Good | 29 |
| **Manhattan** | Needs Improvement | 5 |
| **Queens** | Excellent | 31 |
| **Queens** | Fair | 21 |
| **Queens** | Good | 32 |
| **Staten Island** | Excellent | 3 |
| **Staten Island** | Fair | 2 |
| **Staten Island** | Good | 8 |

<br>

</div>

**Note**

- Queens & Staten Island have no school performances that "need improvement"

- Brooklyn has the most "needs improvement," with 7 schools.


### More Analysis here

***

<br>

## Statistical Testing

**ANOVA:**

Family Involvement --> School attendance

**Handling Missing Values**

<div align='center'>

We'll try multiple methods of clearing missing values

- Filling in with overall average
    - or Borough Average

- Dropping rows




***

## AI use

AI was used sparsely during EDA, mainly for quick debugging or clarification of code.