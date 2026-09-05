"""
02_eda.py
---------
Exploratory Data Analysis on the simulated logistics dataset:
 - Central tendency & spread for key numeric variables
 - Frequency breakdowns for categorical variables
 - On-time performance and damage rates by mode/carrier
 - Correlation matrix among numeric variables
Outputs a text summary (eda_summary.txt) used to write the report narrative.
"""

import pandas as pd
import numpy as np

pd.set_option("display.width", 120)

df = pd.read_csv("/home/claude/logistics_analysis/data/logistics_dataset.csv", parse_dates=["ship_date"])

out = []
def log(msg=""):
    print(msg)
    out.append(str(msg))

log("=== DATASET OVERVIEW ===")
log(f"Rows: {len(df)}, Columns: {len(df.columns)}")
log(df.dtypes.to_string())

log("\n=== CENTRAL TENDENCY & SPREAD (numeric variables) ===")
numeric_cols = ["shipment_volume_m3", "weight_kg", "distance_km", "planned_delivery_days",
                 "actual_delivery_days", "delivery_delay_days", "transportation_cost",
                 "fuel_surcharge_pct", "customer_rating"]
desc = df[numeric_cols].describe().T
desc["skew"] = df[numeric_cols].skew()
log(desc.round(2).to_string())

log("\n=== OVERALL KPIs ===")
on_time_rate = df["on_time_flag"].mean() * 100
damage_rate = df["damaged_flag"].mean() * 100
avg_cost = df["transportation_cost"].mean()
avg_delay = df["delivery_delay_days"].mean()
avg_rating = df["customer_rating"].mean()
log(f"On-time delivery rate: {on_time_rate:.1f}%")
log(f"Damage rate: {damage_rate:.2f}%")
log(f"Average transportation cost per shipment: ${avg_cost:,.2f}")
log(f"Average delivery delay: {avg_delay:.2f} days")
log(f"Average customer rating: {avg_rating:.2f} / 5")

log("\n=== ON-TIME RATE & COST BY TRANSPORT MODE ===")
mode_summary = df.groupby("transport_mode").agg(
    shipments=("shipment_id", "count"),
    on_time_rate_pct=("on_time_flag", lambda x: round(x.mean() * 100, 1)),
    avg_delay_days=("delivery_delay_days", "mean"),
    avg_cost=("transportation_cost", "mean"),
    damage_rate_pct=("damaged_flag", lambda x: round(x.mean() * 100, 2)),
    avg_rating=("customer_rating", "mean"),
).round(2).sort_values("shipments", ascending=False)
log(mode_summary.to_string())

log("\n=== ON-TIME RATE & COST BY CARRIER ===")
carrier_summary = df.groupby("carrier").agg(
    shipments=("shipment_id", "count"),
    on_time_rate_pct=("on_time_flag", lambda x: round(x.mean() * 100, 1)),
    avg_cost=("transportation_cost", "mean"),
    damage_rate_pct=("damaged_flag", lambda x: round(x.mean() * 100, 2)),
    avg_rating=("customer_rating", "mean"),
).round(2).sort_values("on_time_rate_pct", ascending=False)
log(carrier_summary.to_string())

log("\n=== PERFORMANCE BY DESTINATION REGION ===")
region_summary = df.groupby("destination_region").agg(
    shipments=("shipment_id", "count"),
    avg_distance_km=("distance_km", "mean"),
    on_time_rate_pct=("on_time_flag", lambda x: round(x.mean() * 100, 1)),
    avg_cost=("transportation_cost", "mean"),
).round(1).sort_values("shipments", ascending=False)
log(region_summary.to_string())

log("\n=== MONTHLY TRENDS (seasonality) ===")
df["month"] = df["ship_date"].dt.month
monthly = df.groupby("month").agg(
    shipments=("shipment_id", "count"),
    avg_cost=("transportation_cost", "mean"),
    on_time_rate_pct=("on_time_flag", lambda x: round(x.mean() * 100, 1)),
    avg_delay_days=("delivery_delay_days", "mean"),
).round(2)
log(monthly.to_string())

log("\n=== CORRELATION MATRIX (numeric variables) ===")
corr = df[numeric_cols].corr(numeric_only=True)
log(corr.round(2).to_string())

log("\n=== KEY CORRELATIONS OF INTEREST ===")
log(f"distance_km vs transportation_cost: {df['distance_km'].corr(df['transportation_cost']):.2f}")
log(f"delivery_delay_days vs customer_rating: {df['delivery_delay_days'].corr(df['customer_rating']):.2f}")
log(f"damaged_flag vs customer_rating: {df['damaged_flag'].corr(df['customer_rating']):.2f}")
log(f"shipment_volume_m3 vs transportation_cost: {df['shipment_volume_m3'].corr(df['transportation_cost']):.2f}")
log(f"fuel_surcharge_pct vs transportation_cost: {df['fuel_surcharge_pct'].corr(df['transportation_cost']):.2f}")

with open("/home/claude/logistics_analysis/data/eda_summary.txt", "w") as f:
    f.write("\n".join(out))

# Save summary tables as CSVs for reference in report
mode_summary.to_csv("/home/claude/logistics_analysis/data/mode_summary.csv")
carrier_summary.to_csv("/home/claude/logistics_analysis/data/carrier_summary.csv")
region_summary.to_csv("/home/claude/logistics_analysis/data/region_summary.csv")
monthly.to_csv("/home/claude/logistics_analysis/data/monthly_summary.csv")
corr.to_csv("/home/claude/logistics_analysis/data/correlation_matrix.csv")
