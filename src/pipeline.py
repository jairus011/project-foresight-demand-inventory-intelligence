"""
Project FORESIGHT — Data Pipeline (D1)
Ingests the 4 raw extracts, cleans them, and produces one
analysis-ready dataset: data/processed/analysis_ready.csv

Run: python pipeline.py
"""

import pandas as pd
import numpy as np
import os

RAW_DIR = "../data"
OUT_DIR = "../data/processed"
os.makedirs(OUT_DIR, exist_ok=True)

log = []  # keeps a record of every cleaning decision -> goes into the data-quality report


def note(msg):
    print(msg)
    log.append(msg)


# ---------- 1. INGEST ----------
sales = pd.read_csv(f"{RAW_DIR}/sales_daily.csv", parse_dates=["date"])
sku_master = pd.read_csv(f"{RAW_DIR}/sku_master.csv", parse_dates=["launch_date"])
calendar = pd.read_csv(f"{RAW_DIR}/calendar.csv", parse_dates=["date"])
inventory = pd.read_csv(f"{RAW_DIR}/inventory_snapshots.csv", parse_dates=["date"])

note(f"Raw shapes -> sales:{sales.shape} sku_master:{sku_master.shape} "
     f"calendar:{calendar.shape} inventory:{inventory.shape}")

# ---------- 2. CLEAN: sku_master ----------
dupes = sku_master.duplicated(subset="sku_id").sum()
if dupes:
    note(f"sku_master: removed {dupes} duplicate sku_id rows")
    sku_master = sku_master.drop_duplicates(subset="sku_id", keep="first")

# normalize category casing inconsistencies
before = sku_master["category"].unique().tolist()
sku_master["category"] = sku_master["category"].str.strip().str.title()
after = sku_master["category"].unique().tolist()
note(f"sku_master: normalized category labels {before} -> {after}")

# ---------- 3. CLEAN: sales_daily ----------
dupes = sales.duplicated().sum()
if dupes:
    note(f"sales_daily: removed {dupes} exact duplicate rows")
    sales = sales.drop_duplicates()

missing_rev = sales["revenue"].isna().sum()
if missing_rev:
    # reconstruct revenue from units_sold * unit_price rather than dropping rows
    mask = sales["revenue"].isna()
    sales.loc[mask, "revenue"] = sales.loc[mask, "units_sold"] * sales.loc[mask, "unit_price"]
    note(f"sales_daily: {missing_rev} missing 'revenue' values reconstructed "
         f"from units_sold * unit_price")

neg = (sales["units_sold"] < 0).sum()
if neg:
    note(f"sales_daily: {neg} negative units_sold rows clipped to 0")
    sales["units_sold"] = sales["units_sold"].clip(lower=0)

# ---------- 4. CLEAN: inventory_snapshots ----------
neg_stock = (inventory["on_hand_units"] < 0).sum()
if neg_stock:
    inventory["on_hand_units"] = inventory["on_hand_units"].clip(lower=0)
    note(f"inventory_snapshots: {neg_stock} negative on_hand_units clipped to 0")

# ---------- 5. MERGE into analysis-ready dataset ----------
# grain: one row per sku_id per date (daily), joined with sku attributes and calendar
df = sales.merge(sku_master, on="sku_id", how="left")
df = df.merge(calendar, on="date", how="left", suffixes=("", "_cal"))

# attach nearest prior inventory snapshot per SKU (inventory is weekly, sales is daily)
inventory_sorted = inventory.sort_values("date")
df_sorted = df.sort_values("date")
merged = pd.merge_asof(
    df_sorted, inventory_sorted,
    on="date", by="sku_id", direction="backward"
)

# ---------- 6. FEATURE-READY FLAGS ----------
merged["is_holiday"] = merged["is_holiday"].fillna(0).astype(int)
merged["promo_flag"] = merged["promo_flag"].fillna(0).astype(int)

note(f"Final analysis-ready shape: {merged.shape}")

# ---------- 7. SAVE ----------
merged.to_csv(f"{OUT_DIR}/analysis_ready.csv", index=False)
with open(f"{OUT_DIR}/data_quality_log.txt", "w") as f:
    f.write("\n".join(log))

note(f"\nSaved analysis-ready dataset -> {OUT_DIR}/analysis_ready.csv")
note(f"Saved cleaning log -> {OUT_DIR}/data_quality_log.txt")
