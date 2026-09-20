# Project FORESIGHT — Demand & Inventory Intelligence

**Forecasting, inventory risk scoring, and decision support for a synthetic retail operation.**

Project FORESIGHT is a collaborative data-science project that turns daily sales, product, calendar, and inventory data into two business outputs:

1. forward demand forecasts, and
2. SKU-level inventory actions such as **Reorder now**, **Markdown / clear**, or **Healthy**.

A Streamlit dashboard makes those outputs explorable without requiring a notebook.

## Why this project exists

Retail teams need to answer practical questions such as:

- Which SKUs are likely to run short?
- Which products are tying up working capital?
- How much demand should we expect over the next horizon?
- How do promotions and seasonality change expected sales?
- Which inventory actions should be prioritized first?

FORESIGHT is a portfolio prototype for that workflow.

> **Data note:** the repository uses synthetic retail data generated for the project. Results are not claims about a real retailer.

## What is working

- reproducible synthetic data generation
- cleaning and analysis-ready data pipeline
- exploratory analysis and business insight memo
- forecasting workflow
- inventory risk/action scoring
- committed forward-forecast and risk outputs
- Streamlit decision dashboard
- deployment-ready configuration for Render

## Model snapshot

The project records:

| Metric | Value |
|---|---:|
| Baseline WAPE | 0.239 |
| Forecast model WAPE | 0.231 |
| Relative improvement | 3.2% |

These values describe this synthetic project dataset only.

## Key data findings

The analysis found strong promotion and seasonality effects in the generated data. The accompanying EDA memo documents cleaning decisions, demand patterns, category performance, and inventory implications.

See: [reports/eda_insight_memo.md.md](reports/eda_insight_memo.md.md)

## Repository structure

```text
project-foresight-demand-inventory-intelligence/
├── data/
│   ├── processed/
│   │   ├── analysis_ready.csv
│   │   ├── forecast_forward.csv
│   │   └── risk_scoring.csv
│   ├── calendar.csv
│   ├── inventory_snapshots.csv
│   ├── sales_daily.csv
│   └── sku_master.csv
├── notebooks/
│   ├── 01_eda.ipynb
│   └── 02_forecast_and_risk.ipynb
├── reports/
├── src/
│   ├── dashboard.py
│   ├── generate_data .py
│   └── pipeline.py
├── PROJECT_STATUS.md
├── render.yaml
├── requirements.txt
└── README.md
```

## Run the dashboard locally

Use Python 3.12.

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run src/dashboard.py
```

On Linux/macOS:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run src/dashboard.py
```

## Deployment

The repository is configured for a Render web service.

**Build command**

```bash
pip install -r requirements.txt
```

**Start command**

```bash
streamlit run src/dashboard.py --server.address 0.0.0.0 --server.port $PORT
```

The live URL should only be added here after a deployment has been verified.

## API integration

There is **no external API integration** in the current version. The dashboard reads project outputs from committed CSV files.

That is intentional: this version demonstrates the forecasting and decision layer. A future production architecture could expose forecasts through FastAPI or read from a database/API instead of static project outputs.

## Skills demonstrated

Python · Pandas · Data cleaning · Feature engineering · Forecasting · Model evaluation · Inventory analytics · Streamlit · Git/GitHub · Business communication

## Limitations

- synthetic data rather than production retail data
- dashboard consumes prepared outputs rather than live data
- model performance is specific to this generated dataset
- no authentication, database, streaming, or production monitoring
- no external validation

## Next engineering steps

A serious extension would add a repeatable training CLI, automated tests, database-backed inputs, forecast versioning, and an API contract for downstream systems.
