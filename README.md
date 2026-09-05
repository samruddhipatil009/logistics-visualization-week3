# logistics-visualization-week3

# Advanced Data Analysis and Visualization in Logistics

**Week 3 Task — Advanced Data Analysis and Visualization in Logistics**

This repository contains the Python scripts, simulated dataset, and full Word report
for Week 3 of the logistics data analytics series. It builds on the strategic planning
(Week 1) and data cleaning (Week 2) phases by moving into deeper exploratory analysis
and visualization of operational logistics data.

## Scenario

Continuing with **MeridianMart** — a hypothetical mid-size regional e-commerce and FMCG
distributor — this week's task simulates a full year of shipment-level data across
multiple transport modes, carriers, and destination regions, and analyzes it to surface
operational bottlenecks, cost drivers, and service-quality issues.

## Dataset

A synthetic dataset of **5,000 shipments** over calendar year 2025 was generated in
Python (NumPy/pandas), encoding realistic relationships between transport mode, distance,
cost, delivery delay, damage, and customer satisfaction — including a modeled
November-December holiday peak-season capacity strain.

| Variable | Description |
|---|---|
| `shipment_id`, `ship_date` | Shipment identifier and ship date |
| `origin_hub`, `destination_region` | Origin distribution center and delivery region |
| `transport_mode`, `carrier` | Road / Air / Rail / Sea, and carrier company |
| `shipment_volume_m3`, `weight_kg` | Shipment size |
| `distance_km` | Travel distance |
| `planned_delivery_days`, `actual_delivery_days`, `delivery_delay_days` | SLA vs. actual transit time |
| `transportation_cost`, `fuel_surcharge_pct` | Cost variables |
| `on_time_flag`, `damaged_flag`, `customer_rating` | Performance and satisfaction outcomes |

## Data Science Approach

| Stage | Technique | Script |
|---|---|---|
| Data simulation | Synthetic shipment-level data generation | `scripts/01_simulate_data.py` |
| Exploratory Data Analysis | Descriptive statistics, group comparisons, correlation analysis | `scripts/02_eda.py` |
| Visualization | Distribution, comparison, trend, relationship & correlation charts (matplotlib/seaborn) | `scripts/03_visualizations.py` |
| Reporting | Full written analysis with embedded charts and code | `Logistics_Data_Analysis_Report.docx` |

## Key Insights

- Overall on-time delivery rate is 64.5%, but this hides a sharp seasonal collapse:
  on-time performance drops from a stable ~70-75% for most of the year to just
  26-29% in November-December.
- Transportation cost correlates more strongly with distance (r = 0.46) and transport
  mode than with shipment size (r ≈ 0.00).
- Air freight has the best on-time rate (71.0%) and lowest damage rate (1.4%) but
  costs 4-6x more per shipment than Road, Rail, or Sea.
- Sea freight is the weakest link: lowest on-time rate (59.7%) and highest damage
  rate (5.5%).
- Delivery delay and damage are the two strongest negative drivers of customer
  satisfaction (r = -0.54 and -0.51), stronger than the effect of cost.

## Repository Structure

```
logistics-visualization-week3/
├── README.md
├── requirements.txt
├── Logistics_Data_Analysis_Report.docx
├── data/
│   └── logistics_dataset.csv
├── scripts/
│   ├── 01_simulate_data.py
│   ├── 02_eda.py
│   └── 03_visualizations.py
└── figures/
    ├── 01_delay_distribution.png
    ├── 02_cost_by_mode_boxplot.png
    ├── 03_ontime_rate_by_mode.png
    ├── 04_monthly_seasonality.png
    ├── 05_distance_vs_cost_scatter.png
    ├── 06_correlation_heatmap.png
    └── 07_damage_rating_by_mode.png
```

## Setup

```
pip install -r requirements.txt
```

Run the scripts in order:

```
python scripts/01_simulate_data.py
python scripts/02_eda.py
python scripts/03_visualizations.py
```

## Report

The full analysis — methodology, EDA, all 7 visualizations with code and
interpretation, and prioritized recommendations — is documented in
[`Logistics_Data_Analysis_Report.docx`](./Logistics_Data_Analysis_Report.docx).

## Author

Samruddhi — Logistics Data Analyst Intern, YuvaIntern
