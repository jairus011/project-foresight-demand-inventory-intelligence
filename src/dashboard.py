from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Project FORESIGHT",
    page_icon="📦",
    layout="wide",
)

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "processed"


@st.cache_data
def load_data():
    risk_path = DATA_DIR / "risk_scoring.csv"
    forecast_path = DATA_DIR / "forecast_forward.csv"

    if not risk_path.exists() or not forecast_path.exists():
        raise FileNotFoundError(
            "Processed project outputs are missing. Run the project pipeline/notebooks "
            "to regenerate data/processed/risk_scoring.csv and forecast_forward.csv."
        )

    risk = pd.read_csv(risk_path)
    forecast = pd.read_csv(forecast_path, parse_dates=["date"])
    return risk, forecast


st.title("📦 Project FORESIGHT")
st.caption("Demand forecasting & inventory risk intelligence — portfolio prototype")

st.info(
    "This dashboard uses the project's synthetic retail dataset. It is a decision-support "
    "prototype, not a live inventory system."
)

try:
    risk, forecast = load_data()
except Exception as exc:
    st.error(str(exc))
    st.stop()

st.subheader("Model snapshot")
m1, m2, m3 = st.columns(3)
m1.metric("Baseline WAPE", "0.239")
m2.metric("Model WAPE", "0.231")
m3.metric("Relative improvement", "3.2%")

st.divider()

st.subheader("Inventory risk summary")
required_col = "recommended_action"
if required_col not in risk.columns:
    st.error(f"Expected column '{required_col}' was not found in risk_scoring.csv.")
    st.stop()

actions = risk[required_col].fillna("Unknown")
r1, r2, r3 = st.columns(3)
r1.metric("Reorder now", int((actions == "Reorder now").sum()))
r2.metric("Markdown / clear", int((actions == "Markdown / clear").sum()))
r3.metric("Healthy", int((actions == "Healthy").sum()))

st.divider()

left, right = st.columns([1.1, 0.9])

with left:
    st.subheader("SKU risk table")
    options = ["All"] + sorted(actions.dropna().unique().tolist())
    action_filter = st.selectbox("Recommended action", options)

    if action_filter == "All":
        filtered = risk.copy()
    else:
        filtered = risk[actions == action_filter].copy()

    st.dataframe(filtered, use_container_width=True, hide_index=True)

    st.download_button(
        "Download filtered risk table",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="foresight_risk_view.csv",
        mime="text/csv",
    )

with right:
    st.subheader("Forward demand forecast")

    if not {"sku_id", "date", "forecast"}.issubset(forecast.columns):
        st.error("Forecast output is missing one of: sku_id, date, forecast.")
    else:
        sku_choice = st.selectbox(
            "SKU",
            sorted(forecast["sku_id"].dropna().unique().tolist()),
        )
        sku_forecast = (
            forecast.loc[forecast["sku_id"] == sku_choice, ["date", "forecast"]]
            .sort_values("date")
            .set_index("date")
        )
        st.line_chart(sku_forecast)

st.divider()
st.caption(
    "Project FORESIGHT demonstrates a reproducible forecasting and inventory-risk workflow. "
    "The current dashboard reads committed processed outputs and does not call an external API."
)
