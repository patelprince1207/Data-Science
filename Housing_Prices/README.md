# Metro City House Price Analysis

Exploratory data analysis of housing/real-estate listing data across 6 major Indian metro cities: Bangalore, Chennai, Delhi, Hyderabad, Kolkata, and Mumbai.

## Contents
- `Housing_Prices.ipynb` — main analysis notebook (data loading, cleaning, missing-value handling)
- `Bangalore.csv`, `Chennai.csv`, `Delhi.csv`, `Hyderabad.csv`, `Kolkata.csv`, `Mumbai.csv` — per-city raw datasets

## Key steps
- Combined all 6 city datasets into a single DataFrame with a `city` column
- Checked for duplicates and missing values
- **Important finding:** missing values in this dataset are encoded as `9`, not `NaN` — a naive `dropna()` causes major data loss. Replaced `9` with `NaN` before handling missing values properly (used `fillna(0)` after this correction).

## Tech stack
Python, pandas, numpy, matplotlib, seaborn

## Setup
```bash
pip install -r requirements.txt
jupyter notebook Housing_Prices.ipynb
```
