# Key Insights — Saudi Real Estate Market Analysis (2024)
**Data source:** Saudi Ministry of Justice (MOJ) — 243,871 cleaned transactions, Jan–Dec 2024

---

## 1. Market Overview

**Price levels are heavily concentrated in 4 regions.** Makkah (1,668 SAR/m²), Riyadh
(1,450 SAR/m²), Eastern Province (1,190 SAR/m²) and Madinah (952 SAR/m²) form a clear
top tier — 3–30x more expensive per m² than the bottom tier (Northern Borders at just
55 SAR/m², Najran at 128 SAR/m²). This isn't a smooth gradient; there's a visible price
cliff between the top 4 regions and the remaining 9.

**Area and price are correlated, but not uniformly.** Overall correlation for
residential property is 0.62 — meaningful but far from perfect, meaning area alone
does not explain price; location effects are doing a lot of the work. This is confirmed
regionally: in Tabuk (0.92) and Makkah (0.84) area is a strong price driver, but in
Najran (0.08) and Madinah (0.19) it barely matters — price there is set almost entirely
by other factors (location within the city, land use, market sentiment) rather than
raw square meterage.

**Residential dominates everywhere, but commercial share is a regional signal.**
Tabuk stands out with 19.9% commercial transactions — more than double the national
norm (~9%) — suggesting a market with a distinct commercial/investment character
rather than a purely residential one. Hail has the highest agricultural share (8%).

**Ramadan produces a real, measurable dip.** Transaction volume drops from ~18,600 in
March to ~12,700 in April (-32%), recovering immediately in May. This is a demand-timing
effect, not a data quality issue — it repeats the same pattern every region shows in the
liquidity heatmap. Volume also trends upward through the second half of the year,
peaking in October (~25,700 transactions).

**Riyadh and Jeddah dominate both by count and by value.** Riyadh alone accounts for
69,354 transactions (28% of the national total) and 103.2B SAR in transaction value —
roughly 2.7x Jeddah, the second-largest market. Notably, Hiraimla and Al Diriyah
(satellite areas of Riyadh) appear in the top-10-by-value list despite not appearing in
top-10-by-count — a sign of large, high-value individual land parcels rather than high
transaction frequency.

---

## 2. Investment Angle

**Entry price vs. liquidity is a real trade-off, not just a hunch.** Riyadh and Makkah
combine high prices *and* high liquidity (low risk of being unable to exit a position).
Regions like Hail and Al Jouf sit at the opposite corner: cheap entry, but liquidity is
roughly 10x lower than Riyadh's — an investor there is betting on price appreciation
more than trading flexibility.

**The biggest 2024 price movements happened outside the "big 4."** Hail (+53.7%),
Al Jouf (+39.6%), Tabuk (+32.9%) and Northern Borders (+31.5%) all saw sharp median
price/m² increases from Q1 to Q4 — while Qassim (-16.1%) and Makkah (-8.3%) actually
*declined* over the same period. This is the single most actionable investment signal
in the dataset: momentum and absolute price level are not correlated — some of the
cheapest regions are also the fastest-moving.

**Liquidity is extremely concentrated.** Riyadh's Q3 volume alone (27,053 transactions)
exceeds the *entire annual* volume of 9 of the 13 regions combined. For an investor
prioritizing the ability to resell quickly, only Riyadh, Makkah, and Eastern Province
offer consistently high transaction counts across all four quarters.

**Value segments reveal who each market serves.** Riyadh, Makkah, and Eastern Province
are the only regions with a meaningful "Luxury" segment (>1.5M SAR) — everywhere else,
90%+ of transactions fall in Economy/Mid tiers. This means the "luxury real estate"
narrative only genuinely applies to 3 of the 13 regions; elsewhere the market is
fundamentally a mass, affordability-driven market.

---

## 3. Data Quality Notes (for transparency)

- 5,460 rows (2.2%) were removed during cleaning: duplicates, missing core fields, and
  statistical outliers (IQR × 3 on price/m², computed separately per property
  classification to avoid distorting agricultural vs. residential scales).
- Correlation and price figures use **medians**, not means, to reduce the influence of
  a small number of very large land parcels skewing regional averages.
- MOJ data captures notarized *sale* transactions only — it does not include rental
  yield, which would be needed for a full ROI calculation. This analysis is therefore
  a price/liquidity/momentum view, not a cap-rate or yield-based investment model.
