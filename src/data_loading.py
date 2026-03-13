from pathlib import Path
import pandas as pd


def load_weather_data(weather_csv):
    """
    Load and clean weather data from the exported CSV file.
    """
    weather_csv = Path(weather_csv)

    dfw = pd.read_csv(weather_csv)

    # Meteoblue-style export: first 9 rows are metadata
    meta_rows = 9
    raw = dfw.iloc[meta_rows:].copy()

    # Original column names
    col_temp = dfw.columns[1]
    col_wind = dfw.columns[2]
    col_wdir = dfw.columns[3]
    col_solar = dfw.columns[4]

    # Rename columns to the names expected by main.py
    raw = raw.rename(columns={
        "location": "timestamp",
        col_temp: "Tout_C",
        col_wind: "wind_kmh",
        col_wdir: "wind_dir_deg",
        col_solar: "G_Wm2",
    })

    # Convert data types
    raw["timestamp"] = pd.to_datetime(raw["timestamp"], format="%Y%m%dT%H%M")
    raw["Tout_C"] = pd.to_numeric(raw["Tout_C"], errors="coerce")
    raw["wind_kmh"] = pd.to_numeric(raw["wind_kmh"], errors="coerce")
    raw["wind_dir_deg"] = pd.to_numeric(raw["wind_dir_deg"], errors="coerce")
    raw["G_Wm2"] = pd.to_numeric(raw["G_Wm2"], errors="coerce")

    # Use timestamp as index
    weather = raw.set_index("timestamp").sort_index()

    return weather
