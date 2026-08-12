"""
Real Estate Project - Stage 2: Data Cleaning
Source: Saudi Ministry of Justice (MOJ) - Real Estate Sales Transactions 2024
"""
import pandas as pd
import numpy as np

RAW_DIR = "/home/claude/real_estate_project/data"
OUT_DIR = "/home/claude/real_estate_project/data/cleaned"

# ---- 1. Load & concatenate all quarters ----
frames = []
for q in ["Q1", "Q2", "Q3", "Q4"]:
    df_q = pd.read_csv(f"{RAW_DIR}/MOJ-Sales-2024-{q}.csv")
    df_q["quarter"] = q
    frames.append(df_q)
df = pd.concat(frames, ignore_index=True)

print("=" * 60)
print("RAW SHAPE:", df.shape)
print("=" * 60)

# Rename columns to English (canonical) for easier handling
df = df.rename(columns={
    "المنطقة": "region_ar",
    "المدينة": "city_ar",
    "المدينة / الحي": "district_ar",
    "الرقم المرجعي للصفقة": "ref_number",
    "تاريخ الصفقة ميلادي": "date_gregorian",
    "تاريخ الصفقة هجري": "date_hijri",
    "تصنيف العقار": "classification_ar",
    "عدد العقارات": "num_properties",
    "السعر": "price_raw",
    "المساحة": "area_raw",
})

# ---- 2. Drop fully-empty / corrupt rows ----
before = len(df)
df = df.dropna(subset=["price_raw", "area_raw", "region_ar"])
print(f"Dropped {before - len(df)} rows with missing core fields")

# ---- 3. Clean numeric fields (remove thousands-separator commas) ----
df["price"] = df["price_raw"].astype(str).str.replace(",", "", regex=False).astype(float)
df["area_sqm"] = df["area_raw"].astype(str).str.replace(",", "", regex=False).astype(float)

# ---- 4. Parse date & derive month/quarter ----
df["date_gregorian"] = pd.to_datetime(df["date_gregorian"], format="%Y/%m/%d", errors="coerce")
df["month"] = df["date_gregorian"].dt.month
df["quarter_num"] = df["date_gregorian"].dt.quarter

# ---- 5. Clean text fields (strip whitespace inconsistencies) ----
for col in ["region_ar", "city_ar", "district_ar", "classification_ar"]:
    df[col] = df[col].astype(str).str.strip()

# Map region names to clean English labels for the CV project (translate the 13 regions)
region_map = {
    "منطقة الرياض": "Riyadh",
    "منطقة مكة المكرمه": "Makkah",
    "منطقة الشرقية": "Eastern Province",
    "منطقة القصيم": "Qassim",
    "منطقة المدينة المنوره": "Madinah",
    "منطقة عسير": "Asir",
    "منطقة حائل": "Hail",
    "منطقة جازان": "Jazan",
    "منطقة تبوك": "Tabuk",
    "منطقة الجوف": "Al Jouf",
    "منطقة نجران": "Najran",
    "منطقة الحدود الشمالية": "Northern Borders",
    "منطقة الباحة": "Al Baha",
}
df["region"] = df["region_ar"].map(region_map)

classification_map = {"سكني": "Residential", "تجاري": "Commercial", "زراعي": "Agricultural"}
df["classification"] = df["classification_ar"].map(classification_map)

# ---- 6. Remove duplicate transactions (same ref_number) ----
before = len(df)
df = df.drop_duplicates(subset=["ref_number"])
print(f"Dropped {before - len(df)} duplicate transactions (same ref_number)")

# ---- 7. Outlier handling on price & area ----
# Domain-sensible floor: a valid sale must have positive price and area
before = len(df)
df = df[(df["price"] > 0) & (df["area_sqm"] > 0)]
print(f"Dropped {before - len(df)} rows with zero/negative price or area")

# Derived metric central to the whole project: price per square meter
df["price_per_sqm"] = df["price"] / df["area_sqm"]

# Statistical outlier trim using IQR on price_per_sqm (per classification, since
# residential/commercial/agricultural have very different price scales)
def iqr_flag(group, col, k=3):
    q1, q3 = group[col].quantile([0.25, 0.75])
    iqr = q3 - q1
    lower, upper = q1 - k * iqr, q3 + k * iqr
    return (group[col] >= lower) & (group[col] <= upper)

before = len(df)
mask = df.groupby("classification", group_keys=False).apply(
    lambda g: iqr_flag(g, "price_per_sqm")
)
df = df[mask]
print(f"Dropped {before - len(df)} statistical outliers (IQR x3 on price/sqm, by classification)")

# ---- 8. Final missing-value check ----
print("\nRemaining nulls per key column:")
print(df[["region", "classification", "price", "area_sqm", "date_gregorian"]].isna().sum())

df = df.dropna(subset=["region", "classification", "date_gregorian"])

# ---- 9. Final column selection ----
final_cols = [
    "ref_number", "region", "city_ar", "district_ar", "classification",
    "num_properties", "price", "area_sqm", "price_per_sqm",
    "date_gregorian", "month", "quarter_num",
]
df_clean = df[final_cols].copy()

print("\n" + "=" * 60)
print("CLEAN SHAPE:", df_clean.shape)
print("=" * 60)
print(df_clean.describe())

df_clean.to_csv(f"{OUT_DIR}/real_estate_2024_clean.csv", index=False)
print(f"\nSaved cleaned dataset to {OUT_DIR}/real_estate_2024_clean.csv")
