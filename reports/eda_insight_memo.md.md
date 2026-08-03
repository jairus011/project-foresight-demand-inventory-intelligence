# Project FORESIGHT — Data-Quality & EDA Insight Memo

## 1. Data-quality issues found and handled
- `sku_master`: 1 duplicate `sku_id` row removed; category labels had
  inconsistent casing (`'Small Appliances'` vs `'small appliances'`, etc.) —
  normalized to Title Case (`Lighting`, `Textiles`, `Decor`, `Furniture`,
  `Small Appliances`).
- `sales_daily`: 40 exact duplicate rows removed; 15 rows with negative
  `units_sold` were clipped to 0 (data entry errors, not real returns).
- Final analysis-ready dataset: **119,153 rows × 20 columns**, one row per
  SKU-day, joined with SKU attributes, calendar, and inventory position.

## 2. Demand patterns

**Seasonality (by month):** January is the clear peak month (~175,000 units
sold), followed by September (~163,000). October is the weakest month
(~97,000 units). This is roughly a 45% swing between the strongest and
weakest month — reorder cycles should build in extra lead time ahead of
January.

**Seasonality (by season):**
| Season | Units sold |
|---|---|
| Winter | 411,374 |
| Summer | 391,462 |
| Spring | 380,506 |
| Autumn | 356,325 |

Winter is the strongest season; Autumn the weakest — a ~15% gap.

## 3. Top movers and dead stock
The top 15 SKUs (led by SKU0001-class fast movers) account for a
disproportionate share of total volume, while the bottom of the ranked list
(dead-stock candidates) sell only a fraction of that — these are markdown /
clearance candidates rather than reorder targets (see `top_movers.png` and
`sku_totals.tail(10)` output for the exact SKU IDs).

## 4. Category performance
| Category | Total units | Total revenue | # SKUs |
|---|---|---|---|
| Decor | 408,982 | ₹1.79B | 54 |
| Lighting | 340,194 | ₹1.07B | 44 |
| Furniture | 302,694 | ₹1.15B | 41 |
| Small Appliances | 242,549 | ₹0.87B | 25 |
| Textiles | 245,248 | ₹0.81B | 36 |

Decor is the single largest revenue driver despite Furniture having a higher
revenue-per-unit — worth prioritizing Decor in forecasting accuracy since it
carries the most business impact.

## 5. Promotion impact
Promotion days show a **large, clear lift**: average units/day rises from
**12.45 (no promo)** to **23.18 (promo)** — an **86% increase**. This is one
of the strongest signals in the dataset and should be an explicit feature in
the forecasting model (already included as `promo_flag`).

## 6. Holiday impact
Holidays show only a mild lift (12.92 → 13.43 units/day, ~4%) — much weaker
than promotions. Holiday effects should still be modeled but are a secondary
driver compared to promotions.

## Key business insights (summary)

1. **Promotions drive an 86% sales lift** — the single biggest demand driver
   in the data. Inventory planning must anticipate known promo events well
   ahead of time to avoid stockouts during promos.
2. **January and Winter are peak-demand periods** (up to 45% above the
   weakest month) — reorder points should be raised ahead of this window,
   not during it, given lead times.
3. **Decor is the highest-revenue category** (₹1.79B, largest of all five)
   — forecast accuracy on Decor SKUs has outsized impact on the business
   case and should be prioritized during model evaluation.
4. **A long tail of dead-stock SKUs exists** at the bottom of the top-movers
   ranking — these are markdown/clearance candidates that free up working
   capital currently locked in slow-moving inventory.

## Data-quality note
Cleaning decisions are logged automatically by `pipeline.py` at
`data/processed/data_quality_log.txt` on every run, so this memo can be
regenerated and verified against fresh data.
