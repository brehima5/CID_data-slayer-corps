# Thierno's EDA Summary — Insights & Model Implications

> **Notebook:** `eda.ipynb` (Thierno's Section)  
> **Target Variable:** `metric_value_4yr_ccr_all_students` (4-Year College & Career Readiness)  
> **Database:** `CID_database_clean.db` — tables: `dim_environment`, `dim_location`, `dim_demographic`, `fact_school_outcomes`

---

## Table of Contents

1. [Economic Need Index (ENI) — Distribution & Geography](#1-economic-need-index-eni--distribution--geography)
2. [Percent Temporary Housing — Distribution](#2-percent-temporary-housing--distribution)
3. [Temp Housing ↔ ENI Relationship](#3-temp-housing--eni-relationship)
4. [Temp Housing → Outcome Metrics](#4-temp-housing--outcome-metrics)
5. [Family Involvement → CCR (Moderated by ENI)](#5-family-involvement--ccr-moderated-by-eni)
6. [Teaching Environment → CCR (Moderated by ENI)](#6-teaching-environment--ccr-moderated-by-eni)
7. [CCR → Postsecondary Enrollment](#7-ccr--postsecondary-enrollment)
8. [Hypothesis Test: Graduation Rate vs CCR Sensitivity to ENI](#8-hypothesis-test-graduation-rate-vs-ccr-sensitivity-to-eni)
9. [Partial Regression: Temp Housing → CCR After Controlling for ENI](#9-partial-regression-temp-housing--ccr-after-controlling-for-eni)
10. [Moderation Analysis: Does Teaching Environment Buffer ENI's Impact on CCR?](#10-moderation-analysis-does-teaching-environment-buffer-enis-impact-on-ccr)
11. [Summary of Feature Importance for CCR Prediction](#11-summary-of-feature-importance-for-ccr-prediction)
12. [Recommendations for Model Build](#12-recommendations-for-model-build)

---

## 1. Economic Need Index (ENI) — Distribution & Geography

### Key Statistics
| Statistic | Value |
|---|---|
| Mean | 0.8039 |
| Median | 0.8510 |
| Std Dev | 0.1369 |
| Q1 / Q3 | 0.7470 / 0.9040 |
| IQR | 0.1570 |
| Min / Max | 0.3140 / 0.9500 |
| Skewness | −1.3803 (left-skewed) |
| Kurtosis | 1.3204 |

### Insights
- **Negatively skewed** — the distribution is clustered toward the **high end**. Most NYC high schools serve communities with substantial economic need.
- **Q1 = 0.747** — even the 25th percentile exceeds 0.5, meaning the vast majority of schools operate under high economic disadvantage.
- A small group of low-ENI outliers exists (min = 0.314), representing atypical schools.

### ENI by Borough
| Borough | Median ENI | Mean ENI | N |
|---|---|---|---|
| **Bronx** | **0.9075** | 0.8818 | 100 |
| Manhattan | 0.8550 | 0.7701 | 111 |
| Brooklyn | 0.8545 | 0.8254 | 130 |
| Queens | 0.7625 | 0.7443 | 84 |
| **Staten Island** | **0.6750** | 0.6733 | 14 |

- **Bronx has the highest median ENI** (0.9075) — schools there face the most concentrated economic disadvantage.
- **Staten Island is the lowest** (0.6750) but only has 14 schools — small sample, interpret with caution.
- Manhattan has the **widest spread** (std = 0.1733), reflecting its economic diversity.

### ENI vs Enrollment
- **Pearson r = −0.2908**, **Spearman r = −0.3923**
- Larger schools tend to have **lower** ENI — school size does NOT indicate greater structural disadvantage.

### 🔧 Model Implication
> **ENI is the single strongest predictor candidate for CCR.** It should be the primary feature. Borough can serve as a categorical grouping variable, but ENI already captures most of the borough-level variation. Enrollment has a weak inverse relationship and may add marginal value.

---

## 2. Percent Temporary Housing — Distribution

### Key Statistics
| Statistic | Value |
|---|---|
| Mean | 0.1664 |
| Median | 0.1450 |
| Q1 / Q3 | 0.0960 / 0.2077 |
| Skewness | 1.9377 (right-skewed) |
| Kurtosis | 6.0422 (heavy tails) |
| Min / Max | 0.0000 / 0.7690 |

### Insights
- **Heavily right-skewed** with a long tail — most schools have moderate temp housing, but a few have extreme concentrations (up to 76.9%).
- **72.7% of schools** (368) exceed 10% temp housing — this is a widespread issue.
- **26.9% of schools** (136) exceed 20% — these represent the most acute housing instability.
- **Leptokurtic** (kurtosis = 6.04) — extreme outlier schools exist.

### 🔧 Model Implication
> Consider **log-transforming or binning** `percent_temp_housing` before model training due to heavy skew. A threshold feature (e.g., `temp_housing_above_20pct`) may capture the non-linear drop in outcomes better than the raw value.

---

## 3. Temp Housing ↔ ENI Relationship

| Correlation | Value |
|---|---|
| Pearson r | 0.6893 |
| Spearman r | 0.7736 |

### Insights
- **Moderate-to-strong positive correlation** — temp housing and ENI are related but not redundant.
- The LOESS curve shows the relationship is **non-linear**: temp housing rises sharply once ENI exceeds ~0.75.
- They carry **independent information** about disadvantage — temp housing captures housing instability specifically, while ENI reflects broader economic need.

### 🔧 Model Implication
> Both features should be included in the model despite correlation. The partial regression analysis (Section 9) confirms temp housing adds unique predictive power beyond ENI. Monitor for multicollinearity (VIF) during model training but **do not drop temp housing** — it captures a distinct dimension of structural disadvantage.

---

## 4. Temp Housing → Outcome Metrics

| Outcome | Pearson r | Spearman r |
|---|---|---|
| **4-Year CCR** | **−0.5409** | **−0.6970** |
| Postsecondary Enrollment (6 Mo) | −0.4880 | −0.6065 |
| 4-Year Graduation Rate | −0.3773 | −0.5003 |

### Insights
- Temp housing has the **strongest negative correlation with CCR** (r = −0.54).
- The LOESS curves reveal **non-linear thresholds**: outcomes drop most sharply when temp housing exceeds ~15–20%.
- Graduation rate is the **least sensitive** to temp housing — it appears more resilient to structural disadvantage.

### 🔧 Model Implication
> Temp housing is the **second strongest predictor of CCR** after ENI. The non-linear LOESS pattern suggests the model may benefit from polynomial features or tree-based methods that can capture threshold effects.

---

## 5. Family Involvement → CCR (Moderated by ENI)

### Overall Relationship
- **Pearson r = −0.1237**, Spearman r = −0.1151
- **No clear linear relationship** between family involvement and CCR overall.

### Stratified by ENI (split at median = 0.845)

| ENI Group | N | Mean CCR | Pearson r (Fam Inv → CCR) |
|---|---|---|---|
| Lower ENI | 166 | 65.3 | −0.158 |
| Higher ENI | 166 | 45.4 | −0.009 |

### Insights
- The correlation is **negative** in both groups (counterintuitive) — likely a **confounding artifact** where high-ENI schools report high family involvement survey scores but still have low CCR.
- High-ENI schools have **20 points lower average CCR** (45.4 vs 65.3).
- The family involvement → CCR link is **weaker in high-ENI schools** (r = −0.009 vs −0.158) — structural disadvantage overwhelms any family engagement signal.

### 🔧 Model Implication
> **Family involvement is NOT a useful standalone predictor of CCR.** The negative/near-zero correlations and Simpson's paradox pattern suggest it would add noise rather than signal. If included, it should be as an **interaction term with ENI**, not as a main effect.

---

## 6. Teaching Environment → CCR (Moderated by ENI)

### Overall Relationship
- **Pearson r = 0.1784**, Spearman r = 0.1842
- **Weak positive association** — better teaching environments are modestly linked to higher CCR.

### Stratified by ENI (split at median = 0.844)

| ENI Group | N | Mean CCR | Pearson r (Teach Env → CCR) |
|---|---|---|---|
| Lower ENI | 165 | 64.8 | 0.130 |
| **Higher ENI** | 164 | 45.3 | **0.234** |

### Insights
- Unlike family involvement, teaching environment has a **positive** correlation with CCR, and it is **stronger in high-ENI schools** (r = 0.234 vs 0.130).
- This suggests teaching environment may be a **protective factor** — in schools facing high economic disadvantage, a strong teaching environment is more impactful.
- Teaching environment has a **stronger association with CCR than family involvement** (r = 0.178 vs r = −0.124).

### 🔧 Model Implication
> **Teaching environment is a candidate feature**, especially as an interaction with ENI. Its protective effect in high-ENI schools suggests an `ENI × teaching_environment` interaction term could improve model accuracy for disadvantaged schools. It represents a **lever that schools can influence**, unlike ENI.

---

## 7. CCR → Postsecondary Enrollment

| Metric | Value |
|---|---|
| Pearson r | 0.7665 |
| Spearman r | 0.7631 |
| N | 413 |

### Group Comparison (split at median CCR = 49.6)
| CCR Group | Mean Postsec. Enrollment | N |
|---|---|---|
| Lower CCR | 0.543 | 207 |
| Higher CCR | 0.750 | 206 |

### Insights
- **Strong positive correlation** (r = 0.77) — CCR is a strong predictor of postsecondary enrollment.
- Higher-CCR schools average **20.7 percentage points higher** postsecondary enrollment.
- The LOESS curve and linear fit closely overlap, indicating a **linear relationship** (no complex non-linearity).

### 🔧 Model Implication
> This validates **CCR as a meaningful target variable** — predicting CCR is effectively predicting postsecondary success. If the model is extended to predict postsecondary enrollment, CCR could serve as an intermediate feature. However, for the primary CCR prediction model, postsecondary enrollment is a **downstream outcome and should NOT be used as a predictor** (it would create data leakage).

---

## 8. Hypothesis Test: Graduation Rate vs CCR Sensitivity to ENI

### OLS Regression Results
| Model | Slope (β) | SE | p-value | R² |
|---|---|---|---|---|
| Graduation Rate ~ ENI | −0.29 | 0.025 | 1.92e-26 | 0.2767 |
| **CCR ~ ENI** | **−89.89** | **3.772** | **2.83e-75** | **0.6187** |

### Paired Slope Difference Test
- **H₀:** ENI affects both outcomes equally (β_grad = β_ccr)
- **H₁:** CCR is significantly more sensitive to ENI
- **t = 23.84, p ≈ 0.0000** → **REJECT H₀**

### Insights
- CCR is **dramatically more sensitive to ENI** than graduation rate — a 1-unit increase in ENI drops CCR by ~90 points vs only ~0.29 for graduation.
- **ENI explains 61.9% of CCR variance** (R² = 0.6187) but only 27.7% of graduation rate variance.
- Graduation rate appears to be a **more resilient metric** — it is less impacted by structural disadvantage.

### 🔧 Model Implication
> This confirms that **ENI is the dominant predictor for a CCR model** (R² = 0.62 from ENI alone). Any CCR prediction model must account for ENI as the primary feature. The high R² also sets a **baseline benchmark**: a model should substantially exceed R² = 0.62 to justify added complexity. The stark difference from graduation rate suggests CCR captures something fundamentally different — career readiness and college preparation are much more sensitive to economic context than mere graduation.

---

## 9. Partial Regression: Temp Housing → CCR After Controlling for ENI

### Hierarchical Regression
| Model | R² | Adj R² |
|---|---|---|
| Model 1: CCR ~ ENI | 0.6187 | 0.6176 |
| Model 2: CCR ~ ENI + Temp Housing | **0.6455** | **0.6435** |
| **ΔR²** | **0.0268** | — |

### Model 2 Coefficients
| Predictor | Unstandardized β | Standardized β | p-value |
|---|---|---|---|
| ENI | −70.09 | **−0.613** | 1.25e-32 |
| Temp Housing | −50.16 | **−0.238** | 4.61e-07 |

### Statistical Test
- **Nested F-test: F = 26.41, p = 4.61e-07** → **REJECT H₀**
- **Partial correlation** (temp housing | ENI) = **−0.2652**

### Insights
- **YES — temp housing significantly predicts CCR beyond what ENI explains** (p < 0.001).
- Adding temp housing improves R² by 2.68% — statistically significant but modest.
- Even among schools with **similar ENI**, higher temp housing → lower CCR.
- **Housing instability is a distinct barrier** beyond general economic need.
- Both predictors remain significant in the combined model — they are **independently informative**.

### 🔧 Model Implication
> **Include both ENI and temp housing as features.** Temp housing adds a unique signal (housing instability) that ENI alone misses. The standardized coefficients show ENI is ~2.6× more influential (β = −0.613 vs −0.238), confirming ENI as the primary driver but temp housing as a meaningful secondary predictor. The combined R² of 0.6455 is the new benchmark for Model 2.

---

## 10. Moderation Analysis: Does Teaching Environment Buffer ENI's Impact on CCR?

### Hierarchical OLS with Interaction
| Model | R² |
|---|---|
| Model 1: CCR ~ ENI | 0.6138 |
| Model 2: CCR ~ ENI + Teaching Env | 0.6226 (ΔR² = 0.0088) |
| Model 3: CCR ~ ENI + Teaching Env + ENI×Teaching | 0.6280 (ΔR² = 0.0055) |

### ENI Slopes by Teaching Environment Tercile
| Teaching Env Group | ENI → CCR Slope (β) | Significance |
|---|---|---|
| Low Teaching Env | −93.9 | *** |
| Mid Teaching Env | −91.7 | *** |
| High Teaching Env | −82.7 | *** |

### Insights
- The ENI slope is **less steep** in schools with high teaching environments (−82.7 vs −93.9) — a difference of ~11 points per unit ENI.
- Teaching environment has a significant **direct effect** on CCR (raises CCR across the board).
- The interaction term provides a modest improvement (ΔR² = 0.0055), suggesting the buffering effect is **present but small**.

### 🔧 Model Implication
> **Include `teaching_environment_pct_positive` and consider an ENI × Teaching interaction term.** While the moderation effect is modest, the tercile analysis shows that ENI's damage is measurably reduced in schools with strong teaching environments. In a tree-based model, this interaction would be captured automatically. For linear models, an explicit interaction term is warranted.

---

## 11. Summary of Feature Importance for CCR Prediction

| Feature | Correlation with CCR | Standardized β (controlled) | Role | Priority |
|---|---|---|---|---|
| `economic_need_index` | r = −0.79 | β = −0.613 | **Primary predictor** | 🔴 Critical |
| `percent_temp_housing` | r = −0.54 | β = −0.238 | **Secondary predictor** (independent of ENI) | 🟠 High |
| `teaching_environment_pct_positive` | r = 0.18 | Modest direct + interaction | **Moderator / protective factor** | 🟡 Medium |
| `enrollment` | r = −0.29 | — | Weak inverse association | 🟢 Low |
| `family_involvement_pct_positive` | r = −0.12 | — | Confounded / not useful alone | ⚪ Exclude or interaction only |
| `borough` | Varies | — | Captured by ENI already | ⚪ Optional |

---

## 12. Recommendations for Model Build

### Feature Engineering
1. **Core features:** `economic_need_index`, `percent_temp_housing`, `teaching_environment_pct_positive`
2. **Interaction term:** `ENI × teaching_environment` — captures the protective buffering effect
3. **Transformation:** Consider log-transforming `percent_temp_housing` (skewness = 1.94) or creating a binary `temp_housing_above_20pct` threshold feature
4. **Drop or deprioritize:** `family_involvement_pct_positive` (confounded negative correlation), `borough` (redundant with ENI)

### Model Selection Considerations
- **Baseline:** OLS with ENI alone achieves R² = 0.62 — any model must beat this
- **Current best linear model:** ENI + Temp Housing achieves R² = 0.645
- **Non-linearity:** LOESS curves show threshold effects (especially for temp housing at ~15–20%) — **tree-based models** (Random Forest, Gradient Boosting) may outperform linear regression
- **Multicollinearity:** ENI and temp housing are correlated (r = 0.69) — monitor VIF, but partial regression confirms both contribute independently

### Key Takeaways for Stakeholders
1. **Economic need is the dominant factor** — ENI alone explains 62% of CCR variance
2. **Housing instability is an independent barrier** — even at the same ENI level, temp housing drags down CCR
3. **Teaching environment is a modifiable lever** — it modestly buffers ENI's negative impact and is the only predictor schools can directly influence
4. **CCR is much more fragile than graduation rate** — structural disadvantage hits career readiness 300× harder than graduation
5. **CCR reliably predicts postsecondary enrollment** (r = 0.77) — improving CCR has real downstream impact

---

*Generated from Thierno's EDA section in `eda.ipynb` — Data Slayer Corps, CID Project*
