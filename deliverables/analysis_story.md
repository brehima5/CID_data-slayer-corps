# What Shapes College Readiness in NYC — and Who's Beating the Odds?

*An analysis of 423 NYC high schools using beta regression, subgroup equity decomposition, and positive deviance identification.*

---

## The Story in Three Acts

**Act 1** asks: *What environmental forces shape whether students leave high school college-ready?*
**Act 2** asks: *Does it hit every student group equally — or do some bear more of the burden?*
**Act 3** asks: *Which schools succeed despite facing the worst conditions — and what can we learn from them?*

Each act builds on the last. The model identifies the forces. The subgroup lens reveals who's most affected. The residuals point us to the schools worth studying.

---

## Act 1 — What Drives College & Career Readiness?

A beta regression model trained on 338 schools (tested on 85) explains **~74% of the variance** in school-level CCR using environmental and geographic features.

### The Three Forces That Matter

| Driver | Effect (per 1-SD shift) | Direction | Significance |
|--------|:-----------------------:|-----------|:------------:|
| **Economic Need Index** | **−14.3 pts** | More poverty → lower CCR | ** |
| **Housing Instability** | −5.5 pts | More temp housing → lower CCR | *** |
| **Student Attendance** | +4.8 pts | Higher attendance → higher CCR | *** |

### What Doesn't Matter (After Controlling for Poverty)

| Factor | Effect | Significance |
|--------|:------:|:------------:|
| Teaching Environment | −5.3 pts | Not significant |
| ENI × Teaching Interaction | +3.6 pts | Not significant |
| Student Support | +1.6 pts | Borderline (*) |

### What This Means for Policy

**Poverty is the dominant force.** A single standard deviation increase in ENI (0.136 raw units — roughly the difference between a moderate-need and high-need school) is associated with a 14-point CCR drop. Housing instability compounds this by another 5.5 points. Together, these two structural factors account for the majority of the model's explanatory power.

**Attendance is the strongest modifiable lever.** Unlike poverty and housing — which schools can't control — attendance is partially within reach of school-level intervention. A 5-percentage-point improvement in attendance (~1 SD) is associated with nearly 5 points higher CCR.

**Teaching environment surveys don't predict CCR** once poverty and attendance are accounted for. This doesn't mean teaching doesn't matter — it means the survey instrument doesn't capture what matters, or that good teaching is absorbed by the attendance pathway.

**The model generalizes well.** Train/test MAE gap is only 0.11 pts, r² gap is 0.026 — no overfitting.

---

## Act 2 — Does It Hit Everyone Equally?

The model predicts school-wide CCR. But within each school, outcomes differ by race/ethnicity. Using the `fact_school_outcomes` table (4 subgroups × 506 schools), we decompose CCR at the subgroup level.

### Within-School Gaps (Same Building, Different Outcomes)

For schools that report CCR for multiple subgroups, we compute each group's deviation from the school mean:

| Subgroup | Gap from School Mean | Interpretation |
|----------|:--------------------:|----------------|
| **Asian** | **+14.3 pts** | Consistently above the school average |
| **White** | +2.9 pts | Slightly above |
| **Black** | −0.7 pts | Slightly below |
| **Hispanic** | −1.0 pts | Slightly below |

These gaps exist **within the same school** — same principal, same neighborhood, same budget. The stressors from Act 1 don't fully explain them.

### A Data Visibility Problem

Not all subgroups are equally visible. NYC suppresses CCR when a subgroup has fewer than 15 graduates:

| Subgroup | Schools with Reported CCR | Suppressed |
|----------|:-------------------------:|:----------:|
| Hispanic | 73% | 27% |
| Black | 59% | 41% |
| Asian | 24% | **76%** |
| White | 20% | **80%** |

We can only observe Asian and White CCR at schools where those groups form large cohorts — which tend to be the better-resourced schools. **The students we can't see are in the highest-need schools.** Any raw comparison between subgroups inflates the apparent gap.

### What This Means for Policy

**The disparities are real but smaller than they appear.** Raw reported data shows a 28+ point Asian–Black gap. After accounting for the selection bias in who reports, the gap likely shrinks to roughly half that. Still meaningful — but the narrative changes.

**Within-school gaps point to internal factors** — course tracking, counseling access, support programs — that school-level stressor models can't capture. Addressing equity requires looking inside schools, not just between them.

---

## Act 3 — Who's Beating the Odds?

Acts 1 and 2 describe the problem. Act 3 looks for solutions — not by modeling, but by identifying real schools that succeed where others don't.

### The Method

The model predicts each school's CCR based on its stressors. The **residual** (actual − predicted) captures unexplained performance. Schools with residuals above +1 SD are **positive deviants** — they outperform what their environment predicts.

We focus specifically on **high-need schools** (ENI ≥ 0.85, the top half) to find success under adversity.

### The Numbers

| Tier | N (high-ENI) | Mean ENI | Predicted CCR | Actual CCR | Residual |
|------|:---:|:---:|:---:|:---:|:---:|
| **⭐ Beating the Odds** | **30** | 0.91 | 42.8% | **56.2%** | **+13.4** |
| Expected Range | 161 | 0.90 | 46.7% | 46.6% | −0.1 |
| Struggling | 21 | 0.91 | 49.3% | 37.2% | −12.1 |

These 30 schools face the same poverty level (ENI 0.91) as the struggling 21 — yet produce CCR rates **19 points higher**.

### The Surprise: It's Not the Obvious Factors

| Modifiable Factor | Beating Odds | Expected | Struggling |
|-------------------|:---:|:---:|:---:|
| Attendance | 84% | 84% | 87% |
| Student Support | 74% | 75% | 75% |
| Teaching Environment | 81% | 82% | 82% |

The three modifiable factors in our model are **virtually identical** across tiers. Struggling schools actually have *slightly higher* attendance. Whatever positive deviants are doing differently **is not captured in the data we have** — it likely lives in leadership quality, school culture, community partnerships, internal resource allocation, or counseling practices.

This is the most important finding: **the model tells us where to look, but the answer requires going there.**

### The Equity Question

Among positive deviants, reported subgroup gaps show Asian students benefiting the most (+14.3 pts above school mean), but sample sizes are very small (n=4 Asian, n=2 White). Black and Hispanic students at beating-the-odds schools show gaps close to zero (−2.0 and −0.1 respectively), suggesting the overperformance partially extends across groups — but more data is needed to confirm.

### What This Means for Policy

**These 30 schools are case study candidates.** The model can't explain their success — but it can identify them. A qualitative investigation (site visits, interviews, program audits) could surface the practices that make them work.

**The value is in the method, not just the list.** As new data becomes available, the model can re-identify positive deviants annually, creating a pipeline of schools to study and replicate.

---

## Limitations

| Limitation | Impact |
|------------|--------|
| **Single year of data** | Can't distinguish persistent practices from one-time cohort effects |
| **Correlation, not causation** | ENI is associated with lower CCR; we can't say it causes it |
| **Subgroup suppression** | 76–80% of Asian/White data is invisible; equity findings are provisional |
| **No individual student data** | Can't separate school effects from student-level selection |
| **Teaching environment surveys** | May not capture actual instructional quality |
| **Positive deviant explanation gap** | The model identifies *who* beats the odds but not *how* |

---

## Streamlit App — Proposed Structure

A 3-page app that mirrors the 3 acts, plus a landing page. Minimum viable — static data, no live model retraining.

### Page 0: Landing

A single summary card per act. Three headline numbers:
- "Poverty explains 74% of CCR variance"
- "Within-school racial gaps persist: +14 pts (Asian) to −1 pt (Hispanic)"
- "30 high-poverty schools beat their predicted CCR by +13 pts"

Each links to its corresponding page.

### Page 1: What Drives CCR?

**Components:**
1. **Coefficient bar chart** — horizontal bars showing the effect of each feature (in CCR points per SD), colored by direction, with significance markers
2. **Marginal effect slider** — user picks a baseline CCR (e.g., 40%), sees how a 1-SD change in each feature shifts it. This makes the logit non-linearity visible: the same feature hurts more at 50% than at 20%.
3. **Borough comparison** — actual vs predicted mean CCR by borough (bar chart from Step 6 Panel F)

**Data needed:** `coef_df`, `beta_model_full.params`, `scaler.scale_`, `borough_summary`

### Page 2: Who's Being Impacted?

**Components:**
1. **Suppression heatmap** — schools × subgroups, showing where data exists vs is hidden, sorted by ENI. Makes the "invisible students" problem tangible.
2. **Within-school gap chart** — bar chart of each subgroup's average gap from school mean, with a filter by ENI quintile to show how poverty amplifies the disparity
3. **Key callout** — a text box summarizing the selection bias: "Raw gap = X pts. After accounting for who reports, likely ~half."

**Data needed:** `fact_school_outcomes` (subgroup CCR, n_count), `deviance_base` (ENI per school)

### Page 3: Schools Beating the Odds

**Components:**
1. **Scatter plot** — ENI (x) vs residual (y), colored by tier. Interactive: hover shows school name, actual/predicted CCR, residual. The top-right quadrant (high ENI, positive residual) is highlighted.
2. **School roster table** — the 30 beating-the-odds schools listed with DBN, borough, ENI, predicted CCR, actual CCR, residual. Sortable. Exportable.
3. **Profile comparison** — side-by-side bars: beating-the-odds vs expected-range vs struggling on attendance, support, teaching. The visual punchline: they look the same. A text callout explains the implication.

**Data needed:** `deviance_base` (all schools with residuals, tier labels, features)

### Technical Requirements

```
deployment/
├── app.py              # Landing page + page router
├── pages/
│   ├── 1_What_Drives_CCR.py
│   ├── 2_Equity_Analysis.py
│   └── 3_Beating_the_Odds.py
├── data/
│   ├── model_results.parquet    # deviance_base: all schools with predictions, residuals, tiers
│   ├── coef_table.csv           # coef_df: coefficient table
│   ├── subgroup_data.parquet    # fact_school_outcomes with ccr_pct and gap computed
│   └── model_params.json        # scaler means/stds, intercept, feature names
```

**No live model needed.** Export the pre-computed results from the notebook as flat files. The app reads and visualizes — no `statsmodels` or `sklearn` required at runtime.

### Packages

```
streamlit
pandas
plotly           # interactive charts (hover, click)
```

### Export Cell (add to notebook)

A single cell at the end of the notebook that saves everything the app needs:
- `deviance_base` → parquet (all schools, features, predictions, residuals, tiers)
- `coef_df` → CSV
- Subgroup data with computed gaps → parquet
- Model parameters (intercept, scaler means/stds) → JSON
