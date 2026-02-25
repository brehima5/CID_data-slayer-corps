"""
Page 4 — Bias & Limitations
Missingness analysis, suppression patterns, and interpretation caveats.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats

from utils.data_loader import build_subgroup_data, SUBGROUP_COLORS

st.set_page_config(page_title="Bias & Limitations", page_icon="⚠️", layout="wide")
st.title("Bias, Limitations & Data Suppression")
st.markdown(
    "Over half of subgroup-level CCR observations are **missing** — "
    "suppressed for privacy (n < 15) or absent entirely (no cohort). "
    "This page examines whether the missingness is random and what it "
    "means for interpretation."
)

sg_all, reported, _ = build_subgroup_data()

# ── tabs ─────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "Data Availability",
    "Missingness Profiles",
    "Implications & Tradeoffs",
])

STATUS_COLORS = {"reported": "#4CAF50", "suppressed": "#FF9800", "no cohort": "#EF5350"}

# =====================================================================
# TAB 1 — Data Availability
# =====================================================================
with tab1:
    st.markdown("### CCR Reporting Status by Subgroup")

    # counts & percentages
    ct = pd.crosstab(sg_all["Subgroup"], sg_all["ccr_status"])
    ct_pct = ct.div(ct.sum(axis=1), axis=0) * 100

    # stacked bar
    fig_avail = go.Figure()
    for status in ["reported", "suppressed", "no cohort"]:
        if status not in ct_pct.columns:
            continue
        fig_avail.add_trace(go.Bar(
            y=ct_pct.index,
            x=ct_pct[status],
            name=status,
            orientation="h",
            marker_color=STATUS_COLORS[status],
            text=[f"{v:.0f}%" for v in ct_pct[status]],
            textposition="inside",
        ))
    fig_avail.update_layout(
        barmode="stack",
        title="CCR Data Availability by Subgroup",
        xaxis_title="% of Schools",
        yaxis_title="",
        height=350,
        plot_bgcolor="white",
        legend=dict(orientation="h", y=-0.15),
    )
    st.plotly_chart(fig_avail, use_container_width=True)

    # raw counts table
    with st.expander("Raw counts"):
        ct["Total"] = ct.sum(axis=1)
        st.dataframe(ct, width='stretch')

    # headline metrics
    total = len(sg_all)
    n_rep  = (sg_all["ccr_status"] == "reported").sum()
    n_sup  = (sg_all["ccr_status"] == "suppressed").sum()
    n_nc   = (sg_all["ccr_status"] == "no cohort").sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Records", total)
    c2.metric("Reported", f"{n_rep} ({n_rep/total*100:.0f}%)")
    c3.metric("Suppressed (n<15)", f"{n_sup} ({n_sup/total*100:.0f}%)")
    c4.metric("No Cohort", f"{n_nc} ({n_nc/total*100:.0f}%)")

    st.markdown(
        """
        **Key observations:**
        - **Hispanic** and **Black** subgroups have the highest reporting
          rates (73 % and 59 %), because these groups are the largest
          populations in many NYC schools.
        - **Asian** and **White** subgroups are heavily suppressed or
          absent — only ~20–24 % of schools can report their CCR.
        - This means our equity analysis is **biased toward schools where
          these subgroups are large enough to report** — typically
          lower-ENI, higher-diversity schools.
        """
    )

# =====================================================================
# TAB 2 — Missingness Profiles
# =====================================================================
with tab2:
    st.markdown("### Are Suppressed Schools Different?")
    st.markdown(
        "We compare the **school-level profiles** of schools where a "
        "subgroup's CCR is reported vs. suppressed, to test whether "
        "the missingness is systematically biased."
    )

    compare_vars = {
        "economic_need_index": "Economic Need Index",
        "avg_student_attendance": "Avg Student Attendance",
        "percent_temp_housing": "% Temporary Housing",
        "student_percent": "Subgroup Student %",
    }

    sel_var = st.selectbox(
        "Select variable to compare",
        list(compare_vars.keys()),
        format_func=lambda k: compare_vars[k],
    )

    fig_comp = go.Figure()
    subgroups = ["Asian", "Black", "Hispanic", "White"]
    statuses  = ["reported", "suppressed", "no cohort"]
    bar_width = 0.25

    for j, status in enumerate(statuses):
        means = []
        for sg in subgroups:
            sub = sg_all[(sg_all["Subgroup"] == sg) & (sg_all["ccr_status"] == status)]
            val = sub[sel_var].mean() if len(sub) > 0 and sub[sel_var].notna().sum() > 0 else 0
            means.append(round(val, 4))
        fig_comp.add_trace(go.Bar(
            x=subgroups, y=means, name=status,
            marker_color=STATUS_COLORS[status],
            text=[f"{m:.3f}" for m in means],
            textposition="outside",
        ))

    fig_comp.update_layout(
        barmode="group",
        title=f"{compare_vars[sel_var]}: Reported vs Suppressed vs No Cohort",
        yaxis_title=compare_vars[sel_var],
        height=450, plot_bgcolor="white",
    )
    st.plotly_chart(fig_comp, use_container_width=True)

    # t-test table
    st.markdown("#### Statistical Test: Reported vs Suppressed")
    test_rows = []
    for sg in subgroups:
        for col in ["economic_need_index", "avg_student_attendance", "percent_temp_housing"]:
            rep = sg_all[(sg_all["Subgroup"] == sg) & (sg_all["ccr_status"] == "reported")][col].dropna()
            sup = sg_all[(sg_all["Subgroup"] == sg) & (sg_all["ccr_status"] == "suppressed")][col].dropna()
            if len(rep) >= 5 and len(sup) >= 5:
                t, p = stats.ttest_ind(rep, sup)
                sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
                test_rows.append(dict(
                    Subgroup=sg,
                    Variable=compare_vars.get(col, col),
                    Reported_Mean=round(rep.mean(), 3),
                    Suppressed_Mean=round(sup.mean(), 3),
                    Diff=round(sup.mean() - rep.mean(), 3),
                    t_stat=round(t, 2),
                    p_value=round(p, 4),
                    Sig=sig,
                ))

    if test_rows:
        st.dataframe(pd.DataFrame(test_rows), width='stretch', hide_index=True)
    else:
        st.info("Insufficient data for statistical comparison.")

    st.markdown(
        """
        **Pattern:** Suppressed schools tend to have **higher ENI**,
        **lower attendance**, and **higher housing instability** than
        schools that report, confirming that missingness is
        **not random**.
        """
    )

# =====================================================================
# TAB 3 — Implications & Tradeoffs
# =====================================================================
with tab3:
    st.markdown("### Why Data is Suppressed")

    st.markdown(
        """

        The NYC DOE suppresses subgroup CCR when the cohort has
        **fewer than 15 students** to protect student privacy. While
        this is necessary, it creates a systematic blind spot:

        - **Small subgroups** (Asian, White in many schools) are
          disproportionately suppressed.
        - Schools where a subgroup is small are often schools where
          that group is a **minority**, potentially facing different
          social dynamics than schools where the group is large.
        """
    )

    st.markdown(
        """
        #### Precision vs. Representation Tradeoff

        | Approach | Precision | Representation |
        |----------|-----------|----------------|
        | **Reported only** (current) |  High — real CCR data | ❌ Biased toward larger subgroups |
        | **Impute suppressed** | ⚠️ Lower — estimated values | ✅ All schools included |
        | **Lower threshold (n<10)** | ⚠️ Noisier estimates | ✅ More schools report |
        | **Aggregate subgroups** | ❌ Loses nuance | ✅ More reportable groups |

        This dashboard uses **reported data only** — the most precise
        approach, but one that systematically excludes the highest-need
        schools for small subgroups.
        """
    )

    st.markdown(
        """
        #### Caveats & Interpretations

        1. **Equity conclusions are conservative.** The actual
           disparities may be **larger** than shown, because the
           missing schools tend to have higher economic stress.

        2. **Borough comparisons are affected.** Boroughs with more
           diverse school populations have better subgroup coverage;
           less diverse boroughs have more suppression.

        3. **The beta regression model (school-level) is not
           affected** by subgroup suppression — it uses school-wide
           CCR, which is available for all schools. Subgroup-level
           findings (Equity page) carry the caveats above.

        4. **Policy implication:** Interventions targeting suppressed
           subgroups should **not** assume their outcomes mirror
           the reported schools. Additional qualitative data or
           lower suppression thresholds would improve visibility.
        """
    )

    st.info(
        "**Bottom line:** The data we can see already reveals "
        "significant disparities. The data we can't see likely "
        "makes those disparities even starker."
    )
