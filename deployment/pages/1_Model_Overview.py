"""
Page 1 — Model Overview
Horizontal coefficient bar chart + model performance metrics.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from utils.data_loader import fit_beta_model, FEATURE_DISPLAY

st.set_page_config(page_title="Model Overview", page_icon="📊", layout="wide")
st.title("📊 Model Overview — Feature Importance")

art = fit_beta_model()
coef_df = art["coef_df"]
train_m = art["train_metrics"]
test_m  = art["test_metrics"]

# ── description ──────────────────────────────────────────────────────
st.markdown(
    """
    The beta regression model predicts **4-Year CCR** using school-level
    environmental stressors, climate measures, and borough.  The chart
    below shows each feature's **standardized coefficient** on the logit
    scale, with 95 % confidence intervals.

    > **Green** bars push CCR **up**; **red** bars push CCR **down**.
    """
)

# ── coefficient bar chart ────────────────────────────────────────────
plot_df = coef_df.drop("const", errors="ignore").copy()
plot_df["display"] = plot_df.index.map(
    lambda n: FEATURE_DISPLAY.get(n, n)
)
plot_df = plot_df.sort_values("Coefficient")

colors = ["#4CAF50" if c > 0 else "#EF5350" for c in plot_df["Coefficient"]]

fig = go.Figure()
fig.add_trace(go.Bar(
    y=plot_df["display"],
    x=plot_df["Coefficient"],
    orientation="h",
    marker_color=colors,
    error_x=dict(type="data", array=(1.96 * plot_df["Std Error"]).values, visible=True),
    text=[f"{c:+.3f} {s}" for c, s in zip(plot_df["Coefficient"], plot_df["sig"])],
    textposition="outside",
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Coefficient: %{x:.4f}<br>"
        "<extra></extra>"
    ),
))
fig.add_vline(x=0, line_dash="dash", line_color="black", line_width=1)
fig.update_layout(
    title="Standardized Beta Coefficients (logit scale) with 95% CI",
    xaxis_title="Coefficient",
    yaxis_title="",
    height=500,
    margin=dict(l=20, r=20, t=50, b=40),
    plot_bgcolor="white",
)
st.plotly_chart(fig, width='stretch', key='coef_chart')

# ── interpretation cards ─────────────────────────────────────────────
st.markdown("### Feature Interpretation")

# Separate significant from non-significant
sig_feats = plot_df[plot_df["sig"] != "ns"].sort_values("Coefficient", key=abs, ascending=False)
ns_feats  = plot_df[plot_df["sig"] == "ns"]

cols = st.columns(2)
with cols[0]:
    st.markdown("#### ✅ Statistically Significant")
    for idx, row in sig_feats.iterrows():
        direction = "⬆️ increases" if row["Coefficient"] > 0 else "⬇️ decreases"
        st.markdown(
            f"**{row['display']}** ({row['sig']}, p = {row['p']:.4f})  \n"
            f"A 1-SD increase {direction} predicted CCR."
        )

with cols[1]:
    st.markdown("#### ⚪ Not Significant")
    if len(ns_feats) == 0:
        st.info("All features are statistically significant.")
    for idx, row in ns_feats.iterrows():
        st.markdown(
            f"**{row['display']}** (p = {row['p']:.3f})  \n"
            f"No statistically significant effect at α = 0.05."
        )

# ── model performance ────────────────────────────────────────────────
st.markdown("---")
st.markdown("### Model Performance")

met_cols = st.columns(5)
labels = ["MAE", "RMSE", "MAPE", "r", "r2"]
nice   = ["MAE (pts)", "RMSE (pts)", "MAPE (%)", "Pearson r", "r²"]

for i, (key, lbl) in enumerate(zip(labels, nice)):
    tr = train_m[key]
    te = test_m[key]
    met_cols[i].metric(
        label=f"Test {lbl}",
        value=f"{te:.2f}" if isinstance(te, float) else str(te),
        delta=f"{te - tr:+.2f} vs train" if isinstance(te, float) else None,
        delta_color="inverse" if key in ("MAE", "RMSE", "MAPE") else "normal",
    )

# train vs test grouped bar
fig2 = go.Figure()
bar_labels = ["MAE", "RMSE", "MAPE (%)", "r²"]
bar_keys   = ["MAE", "RMSE", "MAPE", "r2"]
fig2.add_trace(go.Bar(
    name="Train",
    x=bar_labels,
    y=[train_m[k] for k in bar_keys],
    marker_color="#4682B4",
    text=[f"{train_m[k]:.2f}" for k in bar_keys],
    textposition="outside",
))
fig2.add_trace(go.Bar(
    name="Test",
    x=bar_labels,
    y=[test_m[k] for k in bar_keys],
    marker_color="#FF7F50",
    text=[f"{test_m[k]:.2f}" for k in bar_keys],
    textposition="outside",
))
fig2.update_layout(
    barmode="group",
    title="Train vs Test Metrics — Overfitting Check",
    yaxis_title="Value",
    height=400,
    plot_bgcolor="white",
)
st.plotly_chart(fig2, width='stretch', key='metrics_chart')

mae_gap = abs(train_m["MAE"] - test_m["MAE"])
r2_gap  = abs(train_m["r2"]  - test_m["r2"])
if mae_gap < 2 and r2_gap < 0.05:
    st.success("✅ Model generalizes well — small train/test gap.")
elif mae_gap < 4:
    st.warning("⚠️ Slight overfitting detected (moderate gap).")
else:
    st.error("❌ Potential overfitting — large gap between train and test.")

# ── precision parameter ──────────────────────────────────────────────
st.markdown("---")
with st.expander("🔬 Precision parameter (φ)"):
    st.markdown(
        f"""
        The estimated precision is **φ = {art['precision']:.2f}**.

        In Beta Regression, φ controls the **variance** of the predicted
        distribution — higher φ means tighter, more confident predictions
        around the conditional mean.
        """
    )
