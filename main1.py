"""
Main script for generating hourly historical load profiles.

This script assembles the simplified physics-based model by:
- loading weather data
- computing geometry and thermal properties
- computing internal and solar gains
- running the dynamic building simulation
- converting heating/cooling loads into electrical demand
- saving the final results
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from src.data_loading import load_weather_data
from src.geometry import compute_geometry
from src.thermal_model import compute_thermal_properties
from src.internal_gains import compute_internal_gains
from src.solar_gains import compute_solar_gains
from src.simulation import run_simulation
from src.cop_model import compute_hvac_electricity


def main():
    # ============================================================
    # Input / output paths
    # ============================================================
    BASE_DIR = Path(__file__).resolve().parent

    weather_csv = BASE_DIR / "data" / "raw" / "POWER_Point_Hourly_20250101_20251231_050d85N_004d35E_UTC.csv"
    output_csv = BASE_DIR / "results" / "tables" / "load_profiles_brussels_2025.csv"
    figures_dir = BASE_DIR / "results" / "figures" / "brussels_2025"

    # ============================================================
    # Load weather data
    # ============================================================
    weather = load_weather_data(weather_csv)

    print(weather.head())
    print(weather.columns)
    print("Nombre de lignes météo :", len(weather))

    Tout = weather["Tout_C"].values
    G = weather["G_Wm2"].values

    # ============================================================
    # Derived model components
    # ============================================================
    geometry = compute_geometry()
    thermal_props = compute_thermal_properties()

    internal = compute_internal_gains(weather.index,G)
    Q_int = internal["Q_int"]
    P_base_elec = internal["P_base_elec"]

    Q_solar = compute_solar_gains(G, weather.index)

    # ============================================================
    # Dynamic simulation
    # ============================================================
    sim = run_simulation(
        Tout=Tout,
        Q_solar=Q_solar,
        Q_int=Q_int,
        thermal_props=thermal_props,
        weather_index=weather.index,
    )

    Tin = sim["Tin"]
    Q_hvac = sim["Q_hvac"]
    Q_heat = sim["Q_heat"]
    Q_cool = sim["Q_cool"]

    # ============================================================
    # HVAC electricity
    # ============================================================
    hvac_elec = compute_hvac_electricity(
        Q_heat=Q_heat,
        Q_cool=Q_cool,
        Tout=weather["Tout_C"].values,
    )

    COP_t = hvac_elec["COP_t"]
    EER_t = hvac_elec["EER_t"]
    P_hvac_elec = hvac_elec["P_hvac_elec"]



    # ============================================================
    # Total electricity
    # ============================================================
    P_total_elec = P_base_elec + P_hvac_elec

    # ============================================================
    # Save results
    # ============================================================
    out = pd.DataFrame(index=weather.index)

    out["Tout_C"] = Tout
    out["Tin_C"] = Tin
    out["SolarGain_W"] = Q_solar
    out["InternalGain_W"] = Q_int

    out["HeatingLoad_W"] = Q_heat
    out["CoolingLoad_W"] = Q_cool
    out["HVACLoad_W"] = Q_hvac

    out["BaseElectric_W"] = P_base_elec
    out["HVACElectric_W"] = P_hvac_elec
    out["TotalElectric_W"] = P_total_elec

    out["COP"] = COP_t
    out["EER"] = EER_t

    # Convenient kW columns
    for c in [
        "HeatingLoad_W",
        "CoolingLoad_W",
        "HVACLoad_W",
        "BaseElectric_W",
        "HVACElectric_W",
        "TotalElectric_W",
    ]:
        out[c.replace("_W", "_kW")] = out[c] / 1000.0

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_csv, index_label="timestamp")

    figures_dir.mkdir(parents=True, exist_ok=True)

    print(f"Results saved to: {output_csv}")
    print(f"Figures saved to: {figures_dir}")

    plot_profiles(out, figures_dir)


def plot_profiles(out, figures_dir):
    # Heating and Cooling
    plt.figure(figsize=(14, 4))
    plt.plot(out.index, out["HeatingLoad_kW"], label="Heating load (kW)")
    plt.plot(out.index, out["CoolingLoad_kW"], label="Cooling load (kW)")
    plt.xlabel("Time")
    plt.ylabel("kW")
    plt.title("Heating and Cooling Load Profiles")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figures_dir / "heating_cooling.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Electricity
    plt.figure(figsize=(14, 4))
    plt.plot(out.index, out["BaseElectric_kW"], label="Base electricity (kW)")
    plt.plot(out.index, out["HVACElectric_kW"], label="HVAC electricity (kW)")
    plt.plot(out.index, out["TotalElectric_kW"], label="Total electricity (kW)")
    plt.xlabel("Time")
    plt.ylabel("kW")
    plt.title("Electric Load Profiles")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figures_dir / "electricity.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Electricity - daily average for better readability over one year
    out_daily = out.resample("D").mean()

    plt.figure(figsize=(14, 4))
    plt.plot(out_daily.index, out_daily["BaseElectric_kW"], label="Base electricity (daily avg)")
    plt.plot(out_daily.index, out_daily["HVACElectric_kW"], label="HVAC electricity (daily avg)")
    plt.plot(out_daily.index, out_daily["TotalElectric_kW"], label="Total electricity (daily avg)")

    plt.xlabel("Time")
    plt.ylabel("kW")
    plt.title("Electric Load Profiles (Daily Average)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figures_dir / "electricity_daily.png", dpi=300, bbox_inches="tight")
    plt.close()

    # COP / EER
    plt.figure(figsize=(14, 4))
    plt.plot(out.index, out["COP"], label="COP")
    plt.plot(out.index, out["EER"], label="EER")
    plt.xlabel("Time")
    plt.ylabel("[-]")
    plt.title("Heat Pump Performance")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figures_dir / "cop_eer.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Outdoor temperature
    plt.figure(figsize=(14, 4))
    plt.plot(out.index, out["Tout_C"], label="Outdoor temperature")
    plt.xlabel("Time")
    plt.ylabel("°C")
    plt.title("Outdoor Temperature Profile")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figures_dir / "outdoor_temperature.png", dpi=300, bbox_inches="tight")
    plt.close()



if __name__ == "__main__":
    main()
