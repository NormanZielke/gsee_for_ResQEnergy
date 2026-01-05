from pathlib import Path
import pandas as pd
import numpy as np
import gsee.pv

# --- config ---
FILEPATH = "try_mean_rcp85.p3.txt" # <- set this
YEAR = 2050

# --- read ---
df_raw = pd.read_csv(
    FILEPATH,
    sep=";",
    engine="python",           # tolerant for weird separators
    encoding="utf-8",
)

# force numeric int for time columns (no data changes outside these columns)
for c in ["month", "day", "hour"]:
    df_raw[c] = pd.to_numeric(df_raw[c], errors="raise").astype(int)

year_series = pd.Series([YEAR] * len(df_raw), index=df_raw.index, dtype="int64")

dt = pd.to_datetime(
    {
        "year": year_series,
        "month": df_raw["month"],
        "day": df_raw["day"],
        "hour": df_raw["hour"],
    },
    errors="raise",
)

# --- take data from 5th column onward (index 4) ---
df_data = df_raw.iloc[:, 4:].copy()
df_data.index = dt
df_data.index.name = "time"


# --- build PV input dataframe ---
df_data_pv = pd.DataFrame(
    index=df_data.index
)

# global horizontal irradiance [W/m²]
df_data_pv["global_horizontal"] = df_data["radiation_downwelling"]

# diffuse fraction (raw)
df_data_pv["diffuse_fraction"] = (
    df_data["radiation_diffuse"] / df_data["radiation_downwelling"]
)

# project to physically admissible domain
df_data_pv.loc[df_data_pv["diffuse_fraction"] < 0, "diffuse_fraction"] = 0.0

# optional: ambient temperature [°C]
df_data_pv["temperature"] = df_data["air_temperature_mean"]

# set diffuse_fraction = 0 where global_horizontal == 0
mask_zero_ghi = df_data_pv["global_horizontal"] == 0

df_data_pv.loc[mask_zero_ghi, "diffuse_fraction"] = 0.0


#cols = ["radiation_downwelling", "radiation_direct", "radiation_diffuse"]

#print(df_data[cols])

print(df_data_pv)

coords = (52.43, 13.54)  # lat, lon (Berlin)

result = gsee.pv.run_model(
    data=df_data_pv,
    coords=coords,
    tilt=30,
    azim=0,
    tracking=0,
    capacity=1000,  # W (i.e., 1 kWp)
)

print(type(result))
print(result.head())
print(result.describe())
print(result)














"""
# --- debug check ---

print(df_data.loc[:,["radiation_downwelling","radiation_direct","radiation_diffuse"]].max())
print(df_data.loc[:,["radiation_downwelling","radiation_direct","radiation_diffuse"]].min())

#print(df_data.loc[:,["radiation_downwelling","radiation_direct","radiation_diffuse"]])

print(df_data.loc[df_data["radiation_diffuse"] == -170.9])
print(df_data.loc ["2050-05-03 06:00:00":"2050-05-03 13:00:00",["radiation_downwelling","radiation_direct","radiation_diffuse"]])
print(df_data.loc["2050-05-03 11:00:00",["radiation_downwelling","radiation_direct","radiation_diffuse"]])


cols = ["radiation_downwelling", "radiation_direct", "radiation_diffuse"]

mask_neg = df_data["radiation_diffuse"] < 0

print("Number of negative radiation_diffuse values:", mask_neg.sum())

print("\nRows with negative radiation_diffuse:")
print(df_data.loc[mask_neg, cols])

"""


