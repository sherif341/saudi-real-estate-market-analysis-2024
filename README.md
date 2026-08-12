# 🏠 Saudi Real Estate Market Analysis (2024)
**Descriptive Analytics Project | Python (pandas, matplotlib, seaborn)**

A full end-to-end analysis of 243,871 real estate sale transactions across all 13
regions of Saudi Arabia in 2024, framed around a market-overview + investment lens.
No predictive modeling — the focus is descriptive statistics, exploratory data
analysis, and actionable business insight.

---

## 📊 Business Question

> What are the patterns and trends in the Saudi real estate market during 2024, and
> how do prices, activity, and momentum differ by region — from both a market-overview
> and an investment perspective?

## 🗂️ Data Source

**Saudi Ministry of Justice (MOJ)** — official, open real estate transaction registry.
Source repository: [civillizard/Saudi-Real-Estate-Data](https://github.com/civillizard/Saudi-Real-Estate-Data)
(`moj/sales/MOJ-Sales-2024-Q1..Q4.csv`)

| | |
|---|---|
| Raw records | 249,331 |
| Clean records | 243,871 |
| Time period | Jan – Dec 2024 |
| Regions covered | 13 (all of Saudi Arabia) |
| Fields | region, city, district, classification, price, area, date |

## 🛠️ Tools & Workflow

| Stage | Tool | Output |
|---|---|---|
| 1. Business Question | — | Defined scope & sub-questions |
| 2. Data Cleaning | Python (pandas) | Removed duplicates, fixed formatting, IQR outlier trim |
| 3. EDA | Python (matplotlib, seaborn) | 8 charts covering price, correlation, seasonality, momentum |
| 4. Key Insights | — | Written findings tied to each chart |
| 5. Recommendations | — | 4 actionable, investment-oriented recommendations |

## 📁 Project Structure
```
real_estate_project/
├── data/
│   └── cleaned/real_estate_2024_clean.csv   # cleaned dataset (243,871 rows)
├── scripts/
│   ├── 01_data_cleaning.py
│   └── 02_eda.py
├── eda/                                # all charts + supporting tables
├── insights/
│   ├── 03_key_insights.md
│   └── 04_recommendations.md
├── Real_Estate_Analysis_2024.ipynb     # full analysis, single notebook
└── requirements.txt
```

**Note on raw data:** the raw MOJ CSVs are not committed to this repo to keep it
lightweight. They're publicly available at
[civillizard/Saudi-Real-Estate-Data](https://github.com/civillizard/Saudi-Real-Estate-Data)
(`moj/sales/MOJ-Sales-2024-Q1..Q4.csv`) and are re-downloaded/reproduced by running
`scripts/01_data_cleaning.py`.

## 🔑 Key Findings

- **Price is heavily concentrated**: Makkah and Riyadh (~1,450–1,670 SAR/m²) form a
  clear top tier, vs. Northern Borders at just 55 SAR/m² — a price cliff, not a gradient.
- **Area doesn't uniformly predict price**: correlation ranges from 0.92 (Tabuk) to
  0.08 (Najran) — location matters far more than size in most regions.
- **Ramadan produces a real ~32% dip** in national transaction volume, rebounding
  immediately the following month.
- **Price momentum is independent of price level**: Hail (+54%), Al Jouf (+40%), and
  Tabuk (+33%) led 2024 growth despite being low-priced regions.
- **Liquidity is extremely concentrated in Riyadh** — its busiest single quarter
  exceeds the full-year volume of 9 of the 13 regions combined.

Full write-up: [`insights/03_key_insights.md`](insights/03_key_insights.md)

## 💡 Business Recommendations

1. Segment investment strategy by growth regions (Hail, Al Jouf, Tabuk) vs. stability/
   liquidity regions (Riyadh, Eastern Province).
2. Treat Riyadh's liquidity dominance as a concentration risk — diversify into
   Makkah/Eastern Province.
3. Time acquisitions around the Ramadan demand dip; sell during the Q3–Q4 peak.
4. Use area-price correlation strength as a due-diligence signal, not a valuation
   shortcut — reliable in Tabuk/Makkah, unreliable in Najran/Madinah.

Full write-up: [`insights/04_recommendations.md`](insights/04_recommendations.md)

## ⚠️ Scope & Limitations

- Descriptive analytics only — no forecasting or predictive modeling.
- MOJ data captures notarized *sale* transactions only (no rental yield), so this is
  a price/liquidity/momentum view, not a cap-rate or ROI-yield investment model.
- Regional price/m² figures use medians (not means) to reduce distortion from large
  individual land parcels.

## ▶️ How to Run

```bash
pip install -r requirements.txt
jupyter notebook Real_Estate_Analysis_2024.ipynb
```
