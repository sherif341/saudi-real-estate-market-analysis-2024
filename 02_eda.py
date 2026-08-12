"""
Real Estate Project - Stage 3: EDA (Exploratory Data Analysis)
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 120

DATA = "/home/claude/real_estate_project/data/cleaned/real_estate_2024_clean.csv"
OUT = "/home/claude/real_estate_project/eda"

df = pd.read_csv(DATA, parse_dates=["date_gregorian"])

# ---------------------------------------------------------------
# Q1/Q6: Price per m² by region (median, more robust than mean)
# ---------------------------------------------------------------
region_price = (
    df[df["classification"] == "Residential"]
    .groupby("region")["price_per_sqm"]
    .median()
    .sort_values(ascending=False)
)
plt.figure(figsize=(9, 6))
sns.barplot(x=region_price.values, y=region_price.index, hue=region_price.index,
            palette="viridis", legend=False)
plt.title("Median Residential Price per m² by Region (2024)")
plt.xlabel("SAR / m²")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{OUT}/01_price_per_sqm_by_region.png")
plt.close()
region_price.to_csv(f"{OUT}/table_region_price.csv")

# ---------------------------------------------------------------
# Q2: Correlation between area and price (log-log, with outlier-safe sample)
# ---------------------------------------------------------------
sample = df[df["classification"] == "Residential"].sample(15000, random_state=1)
plt.figure(figsize=(8, 6))
plt.scatter(sample["area_sqm"], sample["price"], alpha=0.15, s=8, color="teal")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Area (m², log scale)")
plt.ylabel("Price (SAR, log scale)")
plt.title("Price vs Area - Residential Transactions (log-log)")
plt.tight_layout()
plt.savefig(f"{OUT}/02_price_area_scatter.png")
plt.close()

corr_overall = df[df["classification"] == "Residential"][["area_sqm", "price"]].corr().iloc[0, 1]
corr_by_region = (
    df[df["classification"] == "Residential"]
    .groupby("region")[["area_sqm", "price"]]
    .corr()
    .iloc[0::2, 1]
    .droplevel(1)
    .sort_values(ascending=False)
)
corr_by_region.to_csv(f"{OUT}/table_corr_by_region.csv")
print("Overall area-price correlation (Residential):", round(corr_overall, 3))
print(corr_by_region)

# ---------------------------------------------------------------
# Q3: Classification mix by region (stacked %)
# ---------------------------------------------------------------
mix = pd.crosstab(df["region"], df["classification"], normalize="index") * 100
mix = mix.loc[df["region"].value_counts().index]  # order by activity
mix.plot(kind="barh", stacked=True, figsize=(9, 6), colormap="Set2")
plt.title("Property Classification Mix by Region (%)")
plt.xlabel("% of transactions")
plt.ylabel("")
plt.legend(title="Classification", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig(f"{OUT}/03_classification_mix_by_region.png")
plt.close()
mix.to_csv(f"{OUT}/table_classification_mix.csv")

# ---------------------------------------------------------------
# Q4: Seasonality - transaction volume by month
# ---------------------------------------------------------------
monthly = df.groupby("month").size()
plt.figure(figsize=(9, 5))
sns.barplot(x=monthly.index, y=monthly.values, hue=monthly.index, palette="crest", legend=False)
plt.title("Monthly Transaction Volume (2024)")
plt.xlabel("Month")
plt.ylabel("Number of Transactions")
# Ramadan 2024 was approx March 11 - April 9
plt.axvspan(2.5, 4.1, color="orange", alpha=0.15, label="Ramadan period")
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUT}/04_monthly_volume.png")
plt.close()
monthly.to_csv(f"{OUT}/table_monthly_volume.csv")

# ---------------------------------------------------------------
# Q5: Top 10 cities by transaction count and by total value
# ---------------------------------------------------------------
top_cities_count = df["city_ar"].value_counts().head(10)
top_cities_value = df.groupby("city_ar")["price"].sum().sort_values(ascending=False).head(10)
top_cities_count.to_csv(f"{OUT}/table_top_cities_count.csv")
top_cities_value.to_csv(f"{OUT}/table_top_cities_value.csv")

fig, axes = plt.subplots(1, 2, figsize=(13, 6))
sns.barplot(x=top_cities_count.values, y=top_cities_count.index, ax=axes[0],
            hue=top_cities_count.index, palette="mako", legend=False)
axes[0].set_title("Top 10 Cities - Transaction Count")
sns.barplot(x=(top_cities_value.values/1e9), y=top_cities_value.index, ax=axes[1],
            hue=top_cities_value.index, palette="mako", legend=False)
axes[1].set_title("Top 10 Cities - Total Value (Billion SAR)")
plt.tight_layout()
plt.savefig(f"{OUT}/05_top_cities.png")
plt.close()

# ---------------------------------------------------------------
# Q7: QoQ Momentum - price change by region across quarters
# ---------------------------------------------------------------
quarterly_region = (
    df[df["classification"] == "Residential"]
    .groupby(["region", "quarter_num"])["price_per_sqm"]
    .median()
    .unstack()
)
quarterly_region["QoQ_change_%"] = (
    (quarterly_region[4] - quarterly_region[1]) / quarterly_region[1] * 100
).round(1)
quarterly_region_sorted = quarterly_region.sort_values("QoQ_change_%", ascending=False)
quarterly_region_sorted.to_csv(f"{OUT}/table_qoq_momentum.csv")

plt.figure(figsize=(9, 6))
colors = ["seagreen" if v > 0 else "indianred" for v in quarterly_region_sorted["QoQ_change_%"]]
sns.barplot(x=quarterly_region_sorted["QoQ_change_%"], y=quarterly_region_sorted.index,
            hue=quarterly_region_sorted.index, palette=colors, legend=False)
plt.title("Price per m² Momentum: Q1 -> Q4 2024 (%)")
plt.xlabel("% change")
plt.ylabel("")
plt.axvline(0, color="black", linewidth=0.8)
plt.tight_layout()
plt.savefig(f"{OUT}/06_qoq_momentum.png")
plt.close()

# ---------------------------------------------------------------
# Q8: Liquidity - quarterly transaction count by region (heatmap)
# ---------------------------------------------------------------
liquidity = pd.crosstab(df["region"], df["quarter_num"])
liquidity = liquidity.loc[liquidity.sum(axis=1).sort_values(ascending=False).index]
liquidity.to_csv(f"{OUT}/table_liquidity.csv")

plt.figure(figsize=(7, 7))
sns.heatmap(liquidity, annot=True, fmt="d", cmap="YlGnBu", cbar_kws={"label": "Transactions"})
plt.title("Transaction Liquidity by Region x Quarter (2024)")
plt.xlabel("Quarter")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{OUT}/07_liquidity_heatmap.png")
plt.close()

# ---------------------------------------------------------------
# Q10: Value segments (Residential price distribution)
# ---------------------------------------------------------------
res = df[df["classification"] == "Residential"].copy()
bins = [0, 300000, 700000, 1500000, res["price"].max()]
labels = ["Economy (<300K)", "Mid (300K-700K)", "Upper-Mid (700K-1.5M)", "Luxury (>1.5M)"]
res["segment"] = pd.cut(res["price"], bins=bins, labels=labels)
segment_region = pd.crosstab(res["region"], res["segment"], normalize="index") * 100
segment_region.to_csv(f"{OUT}/table_value_segments.csv")

segment_region.plot(kind="barh", stacked=True, figsize=(9, 6), colormap="plasma")
plt.title("Residential Price Segment Mix by Region (%)")
plt.xlabel("% of transactions")
plt.legend(title="Segment", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig(f"{OUT}/08_value_segments.png")
plt.close()

print("\nAll EDA charts and tables saved to", OUT)
