"""
Page 3 — Subgroup Equity Analysis
Stressor impact by subgroup, within-school gaps, interactive filters.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

from utils.data_loader import build_subgroup_data, SUBGROUP_COLORS, BOROUGHS

st.set_page_config(page_title="Equity Analysis", page_icon="⚖️", layout="wide")
st.title("⚖️ Subgroup-Level Equity Analysis")
st.markdown(
    "Explore how **CCR outcomes differ across racial/ethnic subgroups** "
    "and how environmental stressors impact each group."
)

sg_all, reported, multi_sg = build_subgroup_data()

# ── filters ──────────────────────────────────────────────────────────
fcol1, fcol2 = st.columns(2)
with fcol1:
    sel_boroughs = st.multiselect(
        "Filter by Borough",
        BOROUGHS,
        default=BOROUGHS,
    )
with fcol2:
    sel_subgroups = st.multiselect(
        "Filter by Ethnicity",
        ["Asian", "Black", "Hispanic", "White"],
        default=["Asian", "Black", "Hispanic", "White"],
    )

# apply filters
mask_r = reported["borough"].isin(sel_boroughs) & reported["Subgroup"].isin(sel_subgroups)
filtered = reported[mask_r]

mask_m = multi_sg["borough"].isin(sel_boroughs) & multi_sg["Subgroup"].isin(sel_subgroups)
filtered_multi = multi_sg[mask_m]

if filtered.empty:
    st.warning("No data matches the current filter. Broaden your selection.")
    st.stop()

# ── tabs ─────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📊 CCR Distributions",
    "🔬 Stressor Impact",
    "🏫 Within-School Gaps",
])

# =====================================================================
# TAB 1 — CCR Distributions
# =====================================================================
with tab1:
    st.markdown("### CCR Distribution by Subgroup")

    # summary stats
    summary = (
        filtered.groupby("Subgroup")["ccr_pct"]
        .agg(["count", "mean", "median", "std", "min", "max"])
        .round(1)
        .rename(columns={"count": "N", "mean": "Mean", "median": "Median",
                         "std": "Std", "min": "Min", "max": "Max"})
    )
    st.dataframe(summary, width='stretch')

    c1, c2 = st.columns(2)

    # histogram
    with c1:
        fig_hist = go.Figure()
        for sg in sel_subgroups:
            data = filtered[filtered["Subgroup"] == sg]["ccr_pct"]
            if len(data) == 0:
                continue
            fig_hist.add_trace(go.Histogram(
                x=data, name=f"{sg} (n={len(data)}, μ={data.mean():.1f})",
                marker_color=SUBGROUP_COLORS[sg], opacity=0.55,
                nbinsx=20,
            ))
        overall_mean = filtered["ccr_pct"].mean()
        fig_hist.add_vline(x=overall_mean, line_dash="dash",
                           annotation_text=f"Mean = {overall_mean:.1f}")
        fig_hist.update_layout(
            barmode="overlay", title="CCR Distribution",
            xaxis_title="CCR (%)", yaxis_title="Schools",
            height=420, plot_bgcolor="white",
        )
        st.plotly_chart(fig_hist, width='stretch')

    # box plot
    with c2:
        fig_box = go.Figure()
        for sg in sel_subgroups:
            data = filtered[filtered["Subgroup"] == sg]["ccr_pct"]
            if len(data) == 0:
                continue
            fig_box.add_trace(go.Box(
                y=data, name=sg,
                marker_color=SUBGROUP_COLORS[sg],
                boxmean=True,
            ))
        fig_box.update_layout(
            title="CCR by Subgroup (Box Plot)",
            yaxis_title="CCR (%)", height=420, plot_bgcolor="white",
        )
        st.plotly_chart(fig_box, width='stretch')

    # gap callout
    sg_means = filtered.groupby("Subgroup")["ccr_pct"].mean().sort_values(ascending=False)
    if len(sg_means) >= 2:
        top, bottom = sg_means.index[0], sg_means.index[-1]
        gap = sg_means.iloc[0] - sg_means.iloc[-1]
        st.warning(
            f"⚠️ **{top}–{bottom} gap: {gap:.1f} percentage points** "
            f"({sg_means.iloc[0]:.1f} % vs {sg_means.iloc[-1]:.1f} %)"
        )

# =====================================================================
# TAB 2 — Stressor × Subgroup
# =====================================================================
with tab2:
    st.markdown("### How Stressors Impact CCR by Subgroup")
    st.markdown(
        "Each scatter plot shows the relationship between a stressor and "
        "subgroup CCR. The **Pearson r** quantifies the linear association."
    )

    stressors = {
        "economic_need_index": "Economic Need Index",
        "percent_temp_housing": "% Temporary Housing",
        "avg_student_attendance": "Avg Student Attendance",
        "teaching_environment_pct_positive": "Teaching Environment",
    }

    sel_stressor = st.selectbox("Select Stressor", list(stressors.keys()),
                                format_func=lambda k: stressors[k])

    fig_sc = go.Figure()
    corr_rows = []
    for sg in sel_subgroups:
        sg_data = filtered[(filtered["Subgroup"] == sg) & filtered[sel_stressor].notna()]
        if len(sg_data) < 10:
            continue
        r, p = pearsonr(sg_data[sel_stressor], sg_data["ccr_pct"])
        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
        corr_rows.append(dict(Subgroup=sg, r=round(r, 3), p=round(p, 4), sig=sig, N=len(sg_data)))

        fig_sc.add_trace(go.Scatter(
            x=sg_data[sel_stressor], y=sg_data["ccr_pct"],
            mode="markers",
            marker=dict(color=SUBGROUP_COLORS[sg], size=6, opacity=0.5),
            name=f"{sg} (r={r:.2f}{sig})",
        ))

        # trend line
        z = np.polyfit(sg_data[sel_stressor], sg_data["ccr_pct"], 1)
        x_line = np.linspace(sg_data[sel_stressor].min(), sg_data[sel_stressor].max(), 50)
        fig_sc.add_trace(go.Scatter(
            x=x_line, y=np.polyval(z, x_line),
            mode="lines", line=dict(color=SUBGROUP_COLORS[sg], width=3),
            showlegend=False,
        ))

    fig_sc.update_layout(
        title=f"{stressors[sel_stressor]} vs CCR by Subgroup",
        xaxis_title=stressors[sel_stressor],
        yaxis_title="CCR (%)",
        height=500, plot_bgcolor="white",
    )
    st.plotly_chart(fig_sc, width='stretch')

    if corr_rows:
        st.markdown("#### Correlation Summary")
        st.dataframe(pd.DataFrame(corr_rows).set_index("Subgroup"), width='stretch')

    # full correlation matrix
    with st.expander("📋 Full Stressor × Subgroup Correlation Table"):
        rows = []
        for col, label in stressors.items():
            row = {"Stressor": label}
            for sg in ["Asian", "Black", "Hispanic", "White"]:
                sg_data = filtered[(filtered["Subgroup"] == sg) & filtered[col].notna()]
                if len(sg_data) >= 10:
                    r, p = pearsonr(sg_data[col], sg_data["ccr_pct"])
                    sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
                    row[sg] = f"{r:+.2f} {sig}"
                else:
                    row[sg] = "N/A"
            rows.append(row)
        st.dataframe(pd.DataFrame(rows).set_index("Stressor"), width='stretch')

# =====================================================================
# TAB 3 — Within-School Gaps
# =====================================================================
with tab3:
    st.markdown("### Within-School CCR Gaps")
    st.markdown(
        "When students of different backgrounds attend the **same school**, "
        "do they achieve the same CCR?  The *intra-school gap* is each "
        "subgroup's CCR minus the school-wide CCR."
    )

    if filtered_multi.empty:
        st.info("Not enough multi-subgroup schools match the current filter.")
        st.stop()

    c1, c2 = st.columns(2)

    with c1:
        fig_gap_box = go.Figure()
        for sg in sel_subgroups:
            data = filtered_multi[filtered_multi["Subgroup"] == sg]["intra_school_gap"]
            if len(data) < 3:
                continue
            fig_gap_box.add_trace(go.Box(
                y=data, name=sg,
                marker_color=SUBGROUP_COLORS[sg],
                boxmean=True,
            ))
        fig_gap_box.add_hline(y=0, line_dash="dash", line_color="black")
        fig_gap_box.update_layout(
            title="Intra-School Gap Distribution",
            yaxis_title="Gap (pts from school mean)",
            height=450, plot_bgcolor="white",
        )
        st.plotly_chart(fig_gap_box, width='stretch')

    with c2:
        # gap vs ENI
        fig_gap_eni = go.Figure()
        for sg in sel_subgroups:
            sg_data = filtered_multi[
                (filtered_multi["Subgroup"] == sg)
                & filtered_multi["economic_need_index"].notna()
            ]
            if len(sg_data) < 10:
                continue
            r, p = pearsonr(sg_data["economic_need_index"], sg_data["intra_school_gap"])
            sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
            fig_gap_eni.add_trace(go.Scatter(
                x=sg_data["economic_need_index"],
                y=sg_data["intra_school_gap"],
                mode="markers",
                marker=dict(color=SUBGROUP_COLORS[sg], size=5, opacity=0.4),
                name=f"{sg} (r={r:.2f}{sig})",
            ))
            z = np.polyfit(sg_data["economic_need_index"], sg_data["intra_school_gap"], 1)
            x_line = np.linspace(sg_data["economic_need_index"].min(),
                                 sg_data["economic_need_index"].max(), 50)
            fig_gap_eni.add_trace(go.Scatter(
                x=x_line, y=np.polyval(z, x_line),
                mode="lines", line=dict(color=SUBGROUP_COLORS[sg], width=3),
                showlegend=False,
            ))

        fig_gap_eni.add_hline(y=0, line_dash="dash", line_color="black")
        fig_gap_eni.update_layout(
            title="Does ENI Widen Within-School Disparities?",
            xaxis_title="Economic Need Index",
            yaxis_title="Intra-School Gap (pts)",
            height=450, plot_bgcolor="white",
        )
        st.plotly_chart(fig_gap_eni, width='stretch')

    # gap summary table
    st.markdown("#### Gap Summary")
    gap_tbl = (
        filtered_multi.groupby("Subgroup")["intra_school_gap"]
        .agg(["mean", "median", "std", "count"])
        .round(1)
        .rename(columns={"mean": "Mean Gap", "median": "Median Gap",
                         "std": "Std", "count": "N"})
        .sort_values("Mean Gap", ascending=False)
    )
    st.dataframe(gap_tbl, width='stretch')

    st.markdown(
        """
        > **Positive gap** → subgroup outperforms the school average  
        > **Negative gap** → subgroup underperforms the school average

        A widening gap at higher ENI values indicates that economic
        stress **amplifies** existing disparities rather than affecting
        all groups equally.
        """
    )
