"""
03_visualizations.py
---------------------
Generates all charts used in the logistics performance report.
Each chart is chosen deliberately for the story it tells:

1. Histogram + KDE of delivery delay -> shows distribution/shape & outliers
2. Boxplot of transportation cost by transport mode -> compare spread/outliers across categories
3. Bar chart of on-time rate by transport mode -> categorical performance comparison
4. Line chart of monthly shipment volume & on-time rate -> trend/seasonality over time
5. Scatter plot distance vs cost (colored by mode) -> relationship between two numeric vars
6. Correlation heatmap -> relationships among all numeric variables at once
7. Grouped bar: damage rate & customer rating by transport mode -> operational quality comparison
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

sns.set_theme(style="whitegrid", context="talk")
FIG_DIR = "/home/claude/logistics_analysis/figures"

df = pd.read_csv("/home/claude/logistics_analysis/data/logistics_dataset.csv", parse_dates=["ship_date"])
df["month"] = df["ship_date"].dt.month
month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

PALETTE = {"Road": "#4C72B0", "Air": "#DD8452", "Rail": "#55A868", "Sea": "#C44E52"}

# ---------------------------------------------------------------
# 1. Distribution of delivery delay
# ---------------------------------------------------------------
plt.figure(figsize=(9, 5.5))
sns.histplot(df["delivery_delay_days"], bins=30, kde=True, color="#4C72B0")
plt.axvline(0, color="black", linestyle="--", linewidth=1.2, label="On-time threshold")
plt.title("Distribution of Delivery Delay (Actual − Planned Days)")
plt.xlabel("Delivery Delay (days)")
plt.ylabel("Number of Shipments")
plt.legend()
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/01_delay_distribution.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# 2. Boxplot: transportation cost by transport mode
# ---------------------------------------------------------------
plt.figure(figsize=(9, 5.5))
order = df.groupby("transport_mode")["transportation_cost"].median().sort_values(ascending=False).index
sns.boxplot(data=df, x="transport_mode", y="transportation_cost", order=order, palette=PALETTE, showfliers=True)
plt.title("Transportation Cost Distribution by Transport Mode")
plt.xlabel("Transport Mode")
plt.ylabel("Transportation Cost (USD)")
plt.gca().yaxis.set_major_formatter(mticker.StrMethodFormatter('${x:,.0f}'))
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/02_cost_by_mode_boxplot.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# 3. Bar chart: on-time rate by transport mode
# ---------------------------------------------------------------
mode_ontime = df.groupby("transport_mode")["on_time_flag"].mean().mul(100).sort_values(ascending=False)
plt.figure(figsize=(9, 5.5))
bars = plt.bar(mode_ontime.index, mode_ontime.values, color=[PALETTE[m] for m in mode_ontime.index])
plt.axhline(mode_ontime.mean(), color="black", linestyle="--", linewidth=1, label="Average across modes")
for b in bars:
    plt.text(b.get_x() + b.get_width()/2, b.get_height() + 0.5, f"{b.get_height():.1f}%",
              ha="center", va="bottom", fontsize=12)
plt.title("On-Time Delivery Rate by Transport Mode")
plt.xlabel("Transport Mode")
plt.ylabel("On-Time Rate (%)")
plt.ylim(0, 85)
plt.legend()
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/03_ontime_rate_by_mode.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# 4. Line chart: monthly shipment volume & on-time rate (dual axis)
# ---------------------------------------------------------------
monthly = df.groupby("month").agg(shipments=("shipment_id", "count"),
                                   on_time_rate=("on_time_flag", "mean")).reindex(range(1, 13))
fig, ax1 = plt.subplots(figsize=(10, 5.8))
ax1.plot(month_names, monthly["shipments"], color="#4C72B0", marker="o", linewidth=2.2, label="Shipment Volume")
ax1.set_ylabel("Number of Shipments", color="#4C72B0")
ax1.tick_params(axis="y", labelcolor="#4C72B0")
ax1.set_xlabel("Month (2025)")

ax2 = ax1.twinx()
ax2.plot(month_names, monthly["on_time_rate"] * 100, color="#C44E52", marker="s", linewidth=2.2, label="On-Time Rate (%)")
ax2.set_ylabel("On-Time Rate (%)", color="#C44E52")
ax2.tick_params(axis="y", labelcolor="#C44E52")
ax2.set_ylim(0, 100)

plt.title("Monthly Shipment Volume vs. On-Time Delivery Rate (Seasonality)")
fig.legend(loc="lower center", bbox_to_anchor=(0.5, -0.05), ncol=2, frameon=False)
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/04_monthly_seasonality.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------
# 5. Scatter: distance vs cost, colored by mode
# ---------------------------------------------------------------
plt.figure(figsize=(9.5, 6))
sample = df.sample(1500, random_state=1)  # sample for readability
sns.scatterplot(data=sample, x="distance_km", y="transportation_cost", hue="transport_mode",
                 palette=PALETTE, alpha=0.6, s=45)
plt.title("Transportation Cost vs. Distance by Transport Mode")
plt.xlabel("Distance (km)")
plt.ylabel("Transportation Cost (USD)")
plt.gca().yaxis.set_major_formatter(mticker.StrMethodFormatter('${x:,.0f}'))
plt.legend(title="Transport Mode")
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/05_distance_vs_cost_scatter.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# 6. Correlation heatmap
# ---------------------------------------------------------------
numeric_cols = ["shipment_volume_m3", "weight_kg", "distance_km", "planned_delivery_days",
                 "actual_delivery_days", "delivery_delay_days", "transportation_cost",
                 "fuel_surcharge_pct", "customer_rating"]
corr = df[numeric_cols].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, square=True,
            cbar_kws={"label": "Correlation coefficient"})
plt.title("Correlation Matrix of Key Logistics Variables")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/06_correlation_heatmap.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# 7. Grouped bar: damage rate & rating by mode
# ---------------------------------------------------------------
mode_quality = df.groupby("transport_mode").agg(
    damage_rate=("damaged_flag", "mean"),
    avg_rating=("customer_rating", "mean")
).reindex(mode_ontime.index)

fig, ax1 = plt.subplots(figsize=(9.5, 5.8))
x = np.arange(len(mode_quality))
width = 0.38
b1 = ax1.bar(x - width/2, mode_quality["damage_rate"] * 100, width, label="Damage Rate (%)", color="#C44E52")
ax1.set_ylabel("Damage Rate (%)", color="#C44E52")
ax1.tick_params(axis="y", labelcolor="#C44E52")
ax1.set_xticks(x)
ax1.set_xticklabels(mode_quality.index)

ax2 = ax1.twinx()
b2 = ax2.bar(x + width/2, mode_quality["avg_rating"], width, label="Avg. Customer Rating (1-5)", color="#4C72B0")
ax2.set_ylabel("Average Customer Rating (1-5)", color="#4C72B0")
ax2.tick_params(axis="y", labelcolor="#4C72B0")
ax2.set_ylim(0, 5.5)

plt.title("Damage Rate & Customer Satisfaction by Transport Mode")
fig.legend(handles=[b1, b2], loc="lower center", bbox_to_anchor=(0.5, -0.08), ncol=2, frameon=False)
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/07_damage_rating_by_mode.png", dpi=150, bbox_inches="tight")
plt.close()

print("All 7 figures generated in:", FIG_DIR)
