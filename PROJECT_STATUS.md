# Project Status

## What problem does this project solve?

Project FORESIGHT demonstrates how sales, inventory, product, and calendar data can be combined to forecast demand and turn model outputs into simple inventory actions.

## What is working now?

- synthetic data generator
- cleaning and merge pipeline
- EDA notebooks and visual reports
- forecasting/risk workflow
- committed forecast and risk-scoring outputs
- Streamlit dashboard
- local run instructions
- Render deployment configuration

## How do I run it?

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run src/dashboard.py
```

## Is it deployed?

Deployment is being prepared during the September 2026 portfolio cleanup. Add the verified production URL here only after the hosted service passes a launch check.

## Does it use an API?

No. The current dashboard reads local/committed CSV outputs. There are no API keys or external services required.

## Data/model limitations

The dataset is synthetic. The model and business findings are educational/portfolio evidence and should not be represented as validated performance for a real retailer.

## What changed in the portfolio cleanup?

- added a professional root README
- repaired dashboard paths so the app runs from the repository root and on hosting platforms
- added defensive data/column checks
- added CSV download for the filtered risk view
- added explicit synthetic-data and API disclosures
- added minimal runtime requirements
- added Python/Render deployment configuration
- added this status file

## What should be built next?

- convert data generation and modelling into clean CLI modules
- add automated tests
- remove the accidental space in `src/generate_data .py`
- rename `reports/eda_insight_memo.md.md` to a clean `.md` filename
- add experiment tracking/versioned metrics
- optionally expose forecasts via FastAPI when another client actually needs an API
