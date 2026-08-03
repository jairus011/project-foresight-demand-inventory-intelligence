"""
Project FORESIGHT — Synthetic Data Generator
Generates 4 tables matching the NorthBay Living data dictionary:
sales_daily, sku_master, calendar, inventory_snapshots

Run: python generate_data.py
Output: CSVs written to ../data/
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)  # fixed seed -> reproducible

# ---------- CONFIG ----------
N_SKUS = 60                     # keep smaller than 200 for a manageable first pass
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2026, 6, 30)
CATEGORIES = {
    "Furnishings": ["Sofas", "Chairs", "Tables"],
    "Decor": ["Wall Art", "Vases", "Candles"],
    "Small Appliances": ["Blenders", "Lamps", "Fans"],
}

OUT_DIR = "../data"

# ---------- 1. sku_master ----------
skus = []
for i in range(1, N_SKUS + 1):
    sku_id = f"SKU{i:04d}"
    category = np.random.choice(list(CATEGORIES.keys()))
    subcategory = np.random.choice(CATEGORIES[category])
    launch_date = START_DATE + timedelta(days=int(np.random.uniform(0, 400)))
    unit_cost = round(np.random.uniform(200, 4000), 2)
    list_price = round(unit_cost * np.random.uniform(1.4, 2.5), 2)
    skus.append([sku_id, category, subcategory, launch_date.date(), unit_cost, list_price])

sku_master = pd.DataFrame(
    skus, columns=["sku_id", "category", "subcategory", "launch_date", "unit_cost", "list_price"]
)

# introduce a little messiness: some category label casing issues, a duplicate row
sku_master.loc[sku_master.sample(3, random_state=1).index, "category"] = \
    sku_master.loc[sku_master.sample(3, random_state=1).index, "category"].str.lower()
sku_master = pd.concat([sku_master, sku_master.iloc[[0]]], ignore_index=True)  # duplicate

# ---------- 2. calendar ----------
dates = pd.date_range(START_DATE, END_DATE, freq="D")
calendar = pd.DataFrame({"date": dates})
calendar["week"] = calendar["date"].dt.isocalendar().week
calendar["month"] = calendar["date"].dt.month
calendar["season"] = calendar["month"].map(lambda m: (
    "Winter" if m in [12, 1, 2] else
    "Spring" if m in [3, 4, 5] else
    "Summer" if m in [6, 7, 8] else "Autumn"
))
holidays = pd.to_datetime(["2024-01-26", "2024-08-15", "2024-10-31", "2024-12-25",
                           "2025-01-26", "2025-08-15", "2025-10-20", "2025-12-25",
                           "2026-01-26", "2026-06-15"])
calendar["is_holiday"] = calendar["date"].isin(holidays).astype(int)

promo_events = {}
for yr in [2024, 2025, 2026]:
    promo_events[datetime(yr, 6, 15)] = "Summer Sale"
    promo_events[datetime(yr, 11, 25)] = "Festive Sale"
calendar["promo_event"] = calendar["date"].map(promo_events)

# ---------- 3. sales_daily ----------
records = []
for _, row in sku_master.drop_duplicates("sku_id").iterrows():
    sku_id = row["sku_id"]
    launch = pd.Timestamp(row["launch_date"])
    base_price = row["list_price"]
    base_demand = np.random.uniform(2, 25)  # avg units/day
    trend = np.random.uniform(-0.0005, 0.001)
    phase = np.random.uniform(0, 2 * np.pi)

    for d in dates:
        if d < launch:
            continue
        days_since = (d - launch).days
        seasonal = 1 + 0.35 * np.sin(2 * np.pi * d.dayofyear / 365 + phase)
        trend_factor = max(0.3, 1 + trend * days_since)
        promo = 1.6 if d in promo_events else 1.0
        noise = np.random.poisson(max(base_demand * seasonal * trend_factor * promo, 0.1))
        units_sold = max(0, int(noise))
        price = base_price * (0.85 if d in promo_events else 1.0)
        revenue = round(units_sold * price, 2)
        records.append([d.date(), sku_id, units_sold, revenue, round(price, 2),
                         1 if d in promo_events else 0])

sales_daily = pd.DataFrame(
    records, columns=["date", "sku_id", "units_sold", "revenue", "unit_price", "promo_flag"]
)

# introduce messiness: a few missing values, a few duplicate rows
missing_idx = sales_daily.sample(frac=0.01, random_state=2).index
sales_daily.loc[missing_idx, "revenue"] = np.nan
sales_daily = pd.concat([sales_daily, sales_daily.sample(50, random_state=3)], ignore_index=True)

# ---------- 4. inventory_snapshots (weekly snapshots) ----------
snap_dates = pd.date_range(START_DATE, END_DATE, freq="W-MON")
inv_records = []
for _, row in sku_master.drop_duplicates("sku_id").iterrows():
    sku_id = row["sku_id"]
    on_hand = np.random.randint(50, 400)
    lead_time = int(np.random.choice([7, 14, 21, 30]))
    reorder_point = int(np.random.uniform(20, 80))
    for d in snap_dates:
        # simulate depletion/replenishment
        recent_sales = sales_daily[(sales_daily.sku_id == sku_id) &
                                    (pd.to_datetime(sales_daily.date) < d) &
                                    (pd.to_datetime(sales_daily.date) >= d - timedelta(days=7))]["units_sold"].sum()
        on_hand = max(0, on_hand - int(recent_sales * np.random.uniform(0.8, 1.1)))
        on_order = np.random.choice([0, 0, 0, int(np.random.uniform(20, 150))])
        if on_hand < reorder_point:
            on_hand += int(np.random.uniform(100, 300))  # replenishment arrives
        inv_records.append([d.date(), sku_id, on_hand, on_order, lead_time, reorder_point])

inventory_snapshots = pd.DataFrame(
    inv_records, columns=["date", "sku_id", "on_hand_units", "on_order_units",
                           "lead_time_days", "reorder_point"]
)

# ---------- SAVE ----------
import os
os.makedirs(OUT_DIR, exist_ok=True)
sku_master.to_csv(f"{OUT_DIR}/sku_master.csv", index=False)
calendar.to_csv(f"{OUT_DIR}/calendar.csv", index=False)
sales_daily.to_csv(f"{OUT_DIR}/sales_daily.csv", index=False)
inventory_snapshots.to_csv(f"{OUT_DIR}/inventory_snapshots.csv", index=False)

print("Generated:")
print(f"  sku_master: {sku_master.shape}")
print(f"  calendar: {calendar.shape}")
print(f"  sales_daily: {sales_daily.shape}")
print(f"  inventory_snapshots: {inventory_snapshots.shape}")
print(f"\nSaved to {OUT_DIR}/")
