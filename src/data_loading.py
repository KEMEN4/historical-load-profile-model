from pathlib import Path
import pandas as pd

# Path to weather data
WEATHER_CSV = Path("data/raw/dataexport_20260228T140237.csv")

def load_weather_data():
    """
    Load weather data from CSV file
    """

    df = pd.read_csv(WEATHER_CSV)

    # Convert timestamp column if needed
    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"])

    return df


if __name__ == "__main__":
    weather = load_weather_data()
    print(weather.head())
