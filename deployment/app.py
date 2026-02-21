"""
NYC College & Career Readiness Dashboard — Landing Page
Run:  streamlit run deployment/app.py   (from project root)
"""

import sys
from pathlib import Path

# make 'utils' importable from pages/
sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st

st.set_page_config(
    page_title="NYC CCR Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── sidebar branding ────────────────────────────────────────────────
st.sidebar.title("🎓 CCR Dashboard")
st.sidebar.caption("Data Slayer Corps · CID 2025")

# ── hero section ─────────────────────────────────────────────────────
st.title("🎓 NYC College & Career Readiness Dashboard")
st.markdown(
    "Predict school-level **4-Year College & Career Readiness (CCR)** "
    "rates across NYC high schools using a **Beta Regression** model, and "
    "explore subgroup equity gaps across race/ethnicity."
)
st.markdown("---")

# ── key metrics row ──────────────────────────────────────────────────
from utils.data_loader import fit_beta_model  # noqa: E402

art = fit_beta_model()
tm, tsm = art["train_metrics"], art["test_metrics"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Schools Analyzed", f"{tm['N'] + tsm['N']}")
c2.metric("Model r² (Test)", f"{tsm['r2']:.2f}")
c3.metric("Test MAE", f"{tsm['MAE']:.1f} pts")
c4.metric("Precision φ", f"{art['precision']:.1f}")

st.markdown("---")

# ── page guide ───────────────────────────────────────────────────────
st.markdown("### Navigate the Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        #### 📊 Model Overview
        Explore which features drive CCR predictions — coefficient
        directions, magnitudes, and significance levels displayed as
        an interactive horizontal bar chart.

        #### 🔮 Predictive Tool
        Adjust school-level sliders (ENI, attendance, teaching
        environment, etc.) and instantly predict a school's CCR.
        See which factors push the prediction up or down.
        """
    )

with col2:
    st.markdown(
        """
        #### ⚖️ Equity Analysis
        Examine how stressors impact CCR **differently** across
        Asian, Black, Hispanic, and White subgroups. Filter by
        borough and ethnicity to reveal within-school gaps.

        #### ⚠️ Bias & Limitations
        Understand data suppression (n < 15), missingness patterns,
        and the tradeoffs between precision and representation
        in subgroup-level reporting.
        """
    )

st.markdown("---")

# ── about section ────────────────────────────────────────────────────
with st.expander("ℹ️  About this project"):
    st.markdown(
        """
        **What is CCR?**
        The 4-Year College & Career Readiness rate measures the share of
        a graduating cohort that meets NYC DOE benchmarks for
        postsecondary readiness.

        **Why Beta Regression?**
        CCR is a bounded proportion (0 – 100 %).  Unlike OLS, Beta
        Regression respects these bounds, models heteroscedasticity
        naturally, and uses a logit link to handle the non-linear
        relationship between predictors and the outcome.

        **Data Sources:**
        NYC DOE School Quality Reports, NYC InfoHub, and publicly
        available demographic/environmental data for 500+ NYC high
        schools.
        """
    )
