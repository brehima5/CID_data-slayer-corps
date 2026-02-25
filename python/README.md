

# Documentation for Exploratory Data Analysis (EDA) and Modeling Process

EDA was conducted using both Jupyter Notebooks and DB Browser for SQLite. This document consolidates findings across all interfaces.

> [!NOTE]
> Source file contains code for the initializion of the tables and relationships of our database. A README file is embedded within the [src](/python/src/) file.

---

# I. Quick Exploratory Analysis

## Tools Utilized
- SQLite
- Pandas

---

## 1. Schools per Borough

```sql
SELECT borough, COUNT(*) AS count_of_schools
FROM dim_location
GROUP BY borough
ORDER BY COUNT(*) DESC;
```

This query returns the count of schools across all boroughs.

| Borough        | Count of Schools | Percentage of Total |
|---------------|------------------|---------------------|
| Bronx         | 143              | 28.3%               |
| Brooklyn      | 139              | 27.5%               |
| Manhattan     | 121              | 23.9%               |
| Queens        | 89               | 17.6%               |
| Staten Island | 14               | 2.8%                |
| **Total**     | **506**          | **100%**            |

### Observations
- The Bronx and Brooklyn account for more than half of all schools.
- Staten Island has a very small sample size (14 schools), requiring cautious interpretation in borough-level comparisons.

---

## 2. Instructor Performance Rating per Borough

```sql
WITH cte AS (
    SELECT *
    FROM dim_environment e
    JOIN dim_location l
    ON e.DBN = l.DBN
)
SELECT borough, instruction_performance_rating, 
       COUNT(instruction_performance_rating) AS performance_groups
FROM cte
WHERE instruction_performance_rating IS NOT NULL
GROUP BY borough, instruction_performance_rating;
```

This query provides counts of instructor performance ratings per borough and rating label.

> **NOTE**
> `SELECT *` was used here because of our small dataset. This would not be done for larger, cost-implicated databases.


| Borough        | Instructor Performance Rating | Count |
|---------------|--------------------------------|-------|
| Bronx         | Excellent                      | 20    |
| Bronx         | Fair                           | 53    |
| Bronx         | Good                           | 57    |
| Bronx         | Needs Improvement              | 3     |
| Brooklyn      | Excellent                      | 16    |
| Brooklyn      | Fair                           | 54    |
| Brooklyn      | Good                           | 54    |
| Brooklyn      | Needs Improvement              | 7     |
| Manhattan     | Excellent                      | 41    |
| Manhattan     | Fair                           | 43    |
| Manhattan     | Good                           | 29    |
| Manhattan     | Needs Improvement              | 5     |
| Queens        | Excellent                      | 31    |
| Queens        | Fair                           | 21    |
| Queens        | Good                           | 32    |
| Staten Island | Excellent                      | 3     |
| Staten Island | Fair                           | 2     |
| Staten Island | Good                           | 8     |

### Observations
- Queens and Staten Island report no schools rated "Needs Improvement."
- Brooklyn has the highest count of "Needs Improvement" schools (7).
- Manhattan has the highest number of "Excellent" ratings.

---

# II. Statistical Testing

## Welch’s T-Test  
**Family Involvement ↔ School Attendance**

### Distribution Assessment

**Family Involvement**
- Overall distribution is left-skewed.
- Borough-level distributions appear closer to normal.
- Borough averages were used to impute missing values.

**School Attendance**
- Overall distribution appears approximately normal.
- Borough-level distributions show influence from outliers, particularly in Queens and Staten Island.
- Overall mean used for imputation where appropriate.

---

## Missing Value Handling

Multiple approaches were tested:

- Imputation using overall average
- Imputation using borough-specific averages
- Dropping missing rows

### T-Test Result

The results indicate that the average percent of positive family involvement is statistically significantly lower than the average percent of student attendance.

---

# III. Story & Analytical Framing

## Objective

The goal is to predict **CCR (College and Career Readiness)** because higher CCR is strongly associated with higher postsecondary enrollment rates. Improving CCR therefore implies improved long-term student outcomes.

---

## Outlier Framing

Two key outlier categories were explored:

- **Negative outliers**: Low ENI, Low CCR  
- **Positive outliers**: High ENI, High CCR  

These schools inform the modeling narrative but are not necessarily directly modeled.

---

# IV. Deep-Dive EDA & Modeling Implications

---

# 1. Economic Need Index (ENI)

### Key Statistics

| Statistic | Value |
|-----------|--------|
| Mean | 0.8039 |
| Median | 0.8510 |
| Std Dev | 0.1369 |
| Skewness | −1.3803 |
| Kurtosis | 1.3204 |

### Insights
- Distribution is negatively skewed (clustered at high economic need).
- Even the 25th percentile exceeds 0.5.
- ENI alone explains approximately 62% of CCR variance (R² ≈ 0.62).

### Model Implication
ENI is the dominant predictor and must serve as the foundational feature in any CCR prediction model.

---

# 2. Percent Temporary Housing

### Key Statistics

| Statistic | Value |
|-----------|--------|
| Mean | 0.1664 |
| Median | 0.1450 |
| Skewness | 1.9377 |
| Kurtosis | 6.0422 |

### Insights
- Strong right skew with heavy tails.
- Threshold effects observed at ~15–20%.

### Model Implication
- Consider log transformation or threshold binning.
- Adds independent predictive power beyond ENI.

---

# 3. Temp Housing and ENI Relationship

| Correlation | Value |
|------------|--------|
| Pearson r | 0.6893 |
| Spearman r | 0.7736 |

### Insights
- Strong but not redundant correlation.
- Temp housing captures housing instability specifically.

### Model Implication
Both ENI and temp housing should be included. Monitor multicollinearity but retain both.

---

# 4. Temp Housing and Outcome Metrics

| Outcome | Pearson r |
|----------|-----------|
| CCR | −0.5409 |
| Postsecondary Enrollment | −0.4880 |
| Graduation Rate | −0.3773 |

### Insight
CCR is most sensitive to housing instability.

---

# 5. Family Involvement and CCR

- Overall weak negative correlation.
- Evidence of confounding.
- Not a useful standalone predictor.

### Model Implication
Exclude as a main effect. Consider interaction only if theoretically justified.

---

# 6. Teaching Environment and CCR

- Weak but positive overall association.
- Stronger effect in high-ENI schools.

### Model Implication
Candidate feature.
Interaction term (ENI × Teaching Environment) recommended in linear models.

---

# 7. CCR and Postsecondary Enrollment

| Metric | Value |
|--------|--------|
| Pearson r | 0.7665 |

### Insight
CCR strongly predicts postsecondary enrollment.
Validates CCR as a meaningful target variable.

---

# 8. ENI Sensitivity: Graduation vs CCR

| Model | R² |
|--------|-----|
| Graduation ~ ENI | 0.2767 |
| CCR ~ ENI | 0.6187 |

### Insight
CCR is dramatically more sensitive to structural disadvantage than graduation rate.

---

# 9. Hierarchical Regression: ENI + Temp Housing

| Model | R² |
|--------|------|
| ENI only | 0.6187 |
| ENI + Temp Housing | 0.6455 |

Temp housing significantly improves model fit.

---

# 10. Moderation: Teaching Environment × ENI

- Modest buffering effect observed.
- ΔR² ≈ 0.0055.

### Model Implication
Interaction term warranted in linear models.

---

# V. Feature Importance Summary

| Feature | Role | Priority |
|----------|------|----------|
| economic_need_index | Primary driver | Critical |
| percent_temp_housing | Independent secondary driver | High |
| teaching_environment_pct_positive | Protective factor | Medium |
| enrollment | Weak | Low |
| family_involvement_pct_positive | Confounded | Exclude |
| borough | Redundant with ENI | Optional |

---

# VI. Recommendations for Model Development

## Core Features
- economic_need_index  
- percent_temp_housing  
- teaching_environment_pct_positive  

## Feature Engineering
- ENI × Teaching interaction
- Log or threshold transform temp housing

## Model Benchmarks
- ENI baseline R² ≈ 0.62
- ENI + Temp Housing R² ≈ 0.645

## Key Stakeholder Takeaways
1. Economic need is the dominant structural driver.
2. Housing instability independently suppresses CCR.
3. Teaching environment is the only strong modifiable lever.
4. CCR is significantly more sensitive to disadvantage than graduation rate.
5. Improving CCR strongly correlates with improved postsecondary enrollment outcomes.

---
