import streamlit as st
import pandas as pd

st.set_page_config(page_title="FORESIGHT Dashboard", layout="wide")

st.title(" FORESIGHT — Demand Forecasting & Risk Dashboard")

# Load data
risk = pd.read_csv("../data/processed/risk_scoring.csv")
forecast = pd.read_csv("../data/processed/forecast_forward.csv")

# --- Top metrics ---
st.subheader("Model Performance")
col1, col2, col3 = st.columns(3)
col1.metric("Baseline WAPE", "0.239")
col2.metric("Model WAPE", "0.231")
col3.metric("Improvement", "3.2%")

st.divider()

# --- Risk summary ---
st.subheader("Risk Summary")
col1, col2, col3 = st.columns(3)
col1.metric("SKUs — Reorder Now", int((risk["recommended_action"] == "Reorder now").sum()))
col2.metric("SKUs — Markdown/Clear", int((risk["recommended_action"] == "Markdown / clear").sum()))
col3.metric("SKUs — Healthy", int((risk["recommended_action"] == "Healthy").sum()))

st.divider()

# --- Filter and table ---
st.subheader("SKU Risk Table")
action_filter = st.selectbox(
    "Filter by recommended action",
    ["All"] + risk["recommended_action"].unique().tolist()
)

if action_filter != "All":
    filtered = risk[risk["recommended_action"] == action_filter]
else:
    filtered = risk

st.dataframe(filtered, use_container_width=True)

st.divider()

# --- Forward forecast ---
st.subheader("Forward Forecast (Next Horizon)")
sku_choice = st.selectbox("Choose SKU", forecast["sku_id"].unique())
st.line_chart(
    forecast[forecast["sku_id"] == sku_choice].set_index("date")["forecast"]
)