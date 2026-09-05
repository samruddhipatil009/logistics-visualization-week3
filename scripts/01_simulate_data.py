"""
01_simulate_data.py
--------------------
Simulates a hypothetical logistics operations dataset for a mid-size
parcel/freight delivery network over one calendar year.

Key variables:
    shipment_id          - unique identifier
    ship_date            - date shipment left origin hub
    origin_hub           - originating distribution center
    destination_region   - delivery region
    transport_mode       - Road / Air / Rail / Sea
    carrier              - carrier company handling the shipment
    shipment_volume_m3   - volume of the shipment (cubic meters)
    weight_kg            - shipment weight (kg)
    distance_km          - travel distance
    planned_delivery_days- SLA promised transit time (days)
    actual_delivery_days - actual transit time (days)
    delivery_delay_days  - actual - planned (negative = early)
    transportation_cost  - total cost to move the shipment (USD)
    fuel_surcharge_pct   - fuel surcharge applied (%)
    on_time_flag         - 1 if delivered on/before planned date
    damaged_flag         - 1 if shipment arrived damaged
    customer_rating      - post-delivery satisfaction score (1-5)
"""

import numpy as np
import pandas as pd

np.random.seed(42)

N = 5000  # number of shipments

origin_hubs = ["Chicago", "Dallas", "Atlanta", "Newark", "Los Angeles", "Seattle"]
destination_regions = ["Northeast", "Southeast", "Midwest", "Southwest", "West", "International"]
transport_modes = ["Road", "Air", "Rail", "Sea"]
carriers = ["Carrier A", "Carrier B", "Carrier C", "Carrier D"]

# Mode-specific base characteristics (speed, cost/km, variability)
mode_profile = {
    "Road": {"speed_kmpd": 700, "cost_per_km": 1.10, "delay_std": 0.9, "damage_rate": 0.02},
    "Air":  {"speed_kmpd": 4000, "cost_per_km": 3.40, "delay_std": 0.5, "damage_rate": 0.015},
    "Rail": {"speed_kmpd": 500, "cost_per_km": 0.55, "delay_std": 1.4, "damage_rate": 0.03},
    "Sea":  {"speed_kmpd": 350, "cost_per_km": 0.25, "delay_std": 2.5, "damage_rate": 0.045},
}

dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")

rows = []
for i in range(1, N + 1):
    ship_date = np.random.choice(dates)
    origin = np.random.choice(origin_hubs)
    dest = np.random.choice(destination_regions, p=[0.22, 0.20, 0.18, 0.15, 0.15, 0.10])
    mode = np.random.choice(transport_modes, p=[0.55, 0.18, 0.15, 0.12])
    carrier = np.random.choice(carriers, p=[0.35, 0.30, 0.20, 0.15])

    profile = mode_profile[mode]

    # distance depends loosely on destination type
    base_distance = {
        "Northeast": 800, "Southeast": 900, "Midwest": 500,
        "Southwest": 1000, "West": 1400, "International": 6000
    }[dest]
    distance_km = max(50, np.random.normal(base_distance, base_distance * 0.25))
    if dest == "International" and mode == "Road":
        mode = "Sea"  # correct implausible combos
        profile = mode_profile[mode]

    shipment_volume_m3 = max(0.1, np.random.gamma(2.0, 1.8))
    weight_kg = shipment_volume_m3 * np.random.uniform(80, 220)

    planned_days = max(1, round(distance_km / profile["speed_kmpd"] + np.random.uniform(0.5, 1.5)))

    # Seasonal peak (Nov-Dec) increases delay & cost due to holiday volume
    month = pd.Timestamp(ship_date).month
    peak_season = month in (11, 12)
    seasonal_delay_boost = 1.0 if peak_season else 0.0
    seasonal_cost_boost = 1.12 if peak_season else 1.0

    delay_noise = np.random.normal(seasonal_delay_boost, profile["delay_std"])
    actual_days = max(1, round(planned_days + delay_noise))
    delivery_delay = actual_days - planned_days
    on_time_flag = 1 if delivery_delay <= 0 else 0

    fuel_surcharge_pct = np.round(np.random.uniform(3, 18), 1)
    base_cost = distance_km * profile["cost_per_km"] + shipment_volume_m3 * 15 + weight_kg * 0.05
    transportation_cost = round(base_cost * (1 + fuel_surcharge_pct / 100) * seasonal_cost_boost, 2)

    damaged_flag = 1 if np.random.rand() < profile["damage_rate"] * (1.5 if peak_season else 1.0) else 0

    # customer rating: penalized by delay and damage
    rating = 5 - min(3, max(0, delivery_delay) * 0.4) - (1.5 if damaged_flag else 0)
    rating = np.clip(rating + np.random.normal(0, 0.4), 1, 5)

    rows.append([
        i, pd.Timestamp(ship_date).date(), origin, dest, mode, carrier,
        round(shipment_volume_m3, 2), round(weight_kg, 1), round(distance_km, 1),
        planned_days, actual_days, delivery_delay, transportation_cost,
        fuel_surcharge_pct, on_time_flag, damaged_flag, round(rating, 2)
    ])

columns = [
    "shipment_id", "ship_date", "origin_hub", "destination_region", "transport_mode",
    "carrier", "shipment_volume_m3", "weight_kg", "distance_km", "planned_delivery_days",
    "actual_delivery_days", "delivery_delay_days", "transportation_cost", "fuel_surcharge_pct",
    "on_time_flag", "damaged_flag", "customer_rating"
]

df = pd.DataFrame(rows, columns=columns)
df.to_csv("/home/claude/logistics_analysis/data/logistics_dataset.csv", index=False)
print(df.shape)
print(df.head())
