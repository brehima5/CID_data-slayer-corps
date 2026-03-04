# 📄 AI.md

**Civic Innovation Datathon — The Marcy Lab School**
**Team Name:** Data Slayer Corps
**Project Title:** Closing NYC's College Readiness Gap — Poverty, Housing, and the Schools Beating the Odds

---

## 1. Purpose of This Document

This document describes:

- How AI tools were used in this project
- The specific prompts we used
- How outputs were validated
- What was modified or rejected
- Risks, limitations, and ethical considerations

We treat AI as a **co-pilot, not an authority**. All final outputs were reviewed and tested by our team.

---

## 2. AI Tools Used

| Tool | Use Case | Version | Notes |
|------|----------|---------|-------|
| GitHub Copilot | Code completion, pandas boilerplate, refactoring | VSCode Extension | Used for routine code; all suggestions manually reviewed |
| ChatGPT | Documentation revision, grammar/clarity, summarization | GPT-4.1 | Used for writing refinement only |
| ChatGPT | Brainstorming, quick lookups | GPT-5 mini | Supplementary ideation |

---

## 3. AI Use by Technical Category

### A. SQL Schema Design

**Why AI Was Used**
We wrote all SQL queries and schema definitions manually without AI assistance. The star schema (`dim_environment`, `dim_location`, `dim_demographic`, `fact_school_outcomes`) was designed by the team based on class notes on database normalization.

**Validation Process**
- ✅ Schema tested with constraint checks (`CHECK`, `FOREIGN KEY`, `UNIQUE`) in SQLite
- ✅ Verified referential integrity across all four tables
- ✅ Confirmed no duplication via `UNIQUE (DBN, Subgroup)` grain enforcement on the fact table

**AI Role:** None for SQL.

---

### B. Exploratory Data Analysis (EDA)

**Why AI Was Used**
GitHub Copilot assisted with writing repetitive pandas code — transformations, `.fillna()` patterns, `.groupby()` aggregations, and plotting boilerplate. This sped up routine EDA without replacing analytical decisions.

**Example Prompt 1**
```
Refer to our merged dataframe df, with ENI, temp_housing, and CCR columns,
write code to compute Pearson and Spearman correlations between ENI
and CCR, and display a LOESS-smoothed scatter plot.
```

**AI Output Summary**
- Suggested `scipy.stats.pearsonr` and `scipy.stats.spearmanr` calls
- Generated `seaborn.regplot` with `lowess=True`

**Validation Process**
- ✅ Verified correlation values against manual computation
- ✅ Confirmed statistical significance of p-values
- ✅ Ensured visualizations reflected actual distributions (no misleading scaling)

**Example of Rejected Output**
Copilot suggested using `.corr()` on the full dataframe without filtering out suppressed/missing CCR rows. We rejected this and ensured all correlations were computed only on rows with reported data.

**Equity Lens Check**
- We asked: Does our EDA framing blame low-income communities?
- We ensured structural factors (ENI, housing instability) were framed as systemic stressors — not student deficits.

---

### C. Statistical Testing

**Why AI Was Used**
AI assisted in generating boilerplate code for t-tests, ANOVA, and VIF checks. Interpretation of test results was done by the team.

**Example Prompt 2**
```
Write an independent samples t-test comparing mean ENI between schools
with reported CCR data vs suppressed CCR data, using scipy.stats.
```

**AI Output Summary**
- Generated `scipy.stats.ttest_ind` code with equal-variance assumption check
- Suggested printing effect size alongside p-value

**Validation Process**
-  Verified normality and variance assumptions before running tests
-  Confirmed sample sizes were sufficient
-  Cross-checked p-values by re-running tests independently
-  Compared effect sizes to ensure practical significance


---

### D. Modeling

**Why AI Was Used**
AI was used sparingly during modeling — primarily for debugging pipeline errors and clarifying Beta Regression syntax in `statsmodels`. All modeling decisions (choice of Beta Regression, feature selection, train/test split strategy, Smithson-Verkuilen squeeze) were made by the team through iterative notebook exploration.

**Example Prompt 3**
```
We are fitting a Beta Regression using statsmodels BetaModel with a logit link.
The target is a proportion (CCR / 100). How do we back-transform the logit-scale
coefficients to the CCR percentage scale for interpretation?
```

**AI Output Summary**
- Explained inverse-logit transformation: `CCR = 100 / (1 + exp(-logit))`
- Plotted multiple model evaluation charts to visualize performance

**Validation Process**
-  Manually recalculated back-transformed coefficients at the intercept baseline (54.3%)
-  Verified multicollinearity using VIF on raw features
-  Confirmed no overfitting: train-test MAE gap = 0.19 pts, R² gap = 0.012
-  Compared Beta Regression against baseline OLS and logistic classification (explored in earlier notebook)

**Example of Rejected Output**
AI initially suggested using OLS with a logit-transformed target as a simpler alternative. We rejected this because Beta Regression natively handles bounded proportions and heteroscedasticity — OLS with transformed targets can produce misleading confidence intervals.

**Ethical Review**
- Could this model stigmatize neighborhoods? → We framed predictions as systemic stressor effects, not school "quality" labels
- Would policymakers misuse predictions? → We added a Bias & Limitations page to the Streamlit dashboard
- Does it reinforce structural bias? → We explicitly surfaced that ENI and housing instability are systemic — not school-controllable — in all outputs

---

### E. Visualization & Deployment (Streamlit)

**AI Use:**
- Copilot assisted with Streamlit layout code and Plotly chart configurations
- Syntax suggestions for `st.columns()`, `st.metric()`, and `plotly.graph_objects`

**Validation Process**
-  Confirmed all visualizations matched notebook outputs
-  Checked for colorblind-accessible palettes
-  Simplified metric labels for non-technical audiences
-  Peer-tested dashboard navigation and readability

---

### F. Documentation & Narrative

**AI was used to:**
- Improve grammar and clarity in README, presentation script, and this document
- Refine executive summary language
- Suggest structure for policy recommendations

**Validation Process**
-  All claims manually verified against model outputs and EDA results
-  Technical accuracy reviewed by all team members
-  Ensured language did not overstate findings (e.g., association vs. causation)

---

## 4. Prompt Log

| Category | Prompt Summary | Accepted / Modified / Rejected | Validation Method |
|----------|---------------|-------------------------------|-------------------|
| EDA | Correlation + LOESS scatter code | Accepted | Manual stat verification |
| EDA | Full-dataframe `.corr()` without filtering | Rejected | Would include suppressed rows |
| Statistical Testing | Independent t-test boilerplate | Modified | Added Welch's correction |
| Modeling | Beta Regression back-transformation | Accepted | Manual recalculation |
| Modeling | Use OLS with logit-target instead of BetaModel | Rejected | Beta Regression is more appropriate for bounded data |
| Visualization | Plotly horizontal bar chart for coefficients | Modified | Adjusted CI display and color coding |
| Documentation | Grammar and structure revision | Modified | Peer review for accuracy |

---

## 5. AI Limitations Observed

- Suggested causal language ("X causes Y") in correlational analysis — we corrected to associational framing
- Copilot auto-completed `.corr()` without accounting for missing/suppressed data
- Recommended OLS over Beta Regression for a bounded proportion target
- Did not account for NYC DOE's n < 15 suppression threshold and its impact on subgroup analysis
- Generated boilerplate that assumed equal variance without testing assumptions first

---

## 6. Responsible AI Reflection

We recognize:

- AI systems are trained on historical data that may encode bias
- Over-reliance on AI-generated code could reduce critical thinking about statistical assumptions
- Civic analytics requires **contextual understanding** beyond pattern recognition — NYC school data has unique suppression rules, borough-specific dynamics, and policy implications that AI tools cannot fully grasp
- Our equity analysis specifically investigates how data infrastructure (n < 15 suppression) can create systematic visibility gaps — a concern that extends to AI training data as well

**We treated AI outputs as hypotheses — not truth.** Every statistical claim, model coefficient, and policy recommendation was validated against our data and reviewed by the full team.

---

## 7. Division of Labor

| Team Member | Role | AI Interaction |
|-------------|------|----------------|
| Thierno Barry | EDA lead, visualization, Tableau | Copilot for pandas/plotting code; manual review |
| Rolando Mancilla-Rojas | SQL schema, data extraction, modeling, Documentation | No AI for SQL; minimal AI for model debugging |
| Adebola (Debo) Odutola | EDA, geospatial analysis, subgroup equity | Copilot for routine code; manual statistical validation |

Each member validated their respective AI-assisted components.

---

## 8. Reproducibility Commitment

- All AI-assisted code was reviewed and rewritten in our own words where needed
- All SQL queries are included in `/sql/data_processing.sql` and `/sql/db_queries.sql`
- Model notebooks are fully documented in `/python/model_notebook/`
- EDA notebooks are reproducible in `/python/eda_notebooks/`
- The Streamlit dashboard replicates the full model pipeline in `/deployment/utils/data_loader.py`
- This prompt log serves as our archive of AI interactions
