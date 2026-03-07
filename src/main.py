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

    weather_csv = Path("data/raw/dataexport_20260228T140237.csv")
    output_csv = Path("results/tables/load_profiles_energy_balance.csv")

    # ============================================================
    # Load weather data
    # ============================================================

    weather = load_weather_data(weather_csv)

    Tout = weather["Tout_C"].values
    G = weather["G_Wm2"].values

    # ============================================================
    # Derived model components
    # ============================================================

    geometry = compute_geometry()
    thermal_props = compute_thermal_properties()

    internal = compute_internal_gains(weather.index)
    Q_int = internal["Q_int"]
    P_base_elec = internal["P_base_elec"]

    Q_solar = compute_solar_gains(G)

    # ============================================================
    # Dynamic simulation
    # ============================================================

    sim = run_simulation(
        Tout=Tout,
        Q_solar=Q_solar,
        Q_int=Q_int,
        thermal_props=thermal_props,
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
        Tout=Tout,
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

    print(f"Results saved to: {output_csv}")


if __name__ == "__main__":
    main()
