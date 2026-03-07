"""
Internal gains model for the simplified building energy balance.

This module computes:
- occupancy profile
- occupant heat gains
- lighting gains
- equipment gains
- total internal gains
- base electric load (non-HVAC)



from src.building_parameters import A_cond, n_occ
from src.model_assumptions import EPD


# Lighting power density:
# the articles report a range of 8–10 W/m².
# I'am uses the midpoint value 9 W/m².
LPD = 9.0  # [W/m²]


def occupancy_fraction(ts):
    """
    Simplified occupancy schedule from the notebook.

    Parameters
    ----------
    ts : pandas.Timestamp
        Current timestamp

    Returns
    -------
    float
        Occupancy fraction
    """

    h = ts.hour
    dow = ts.dayofweek

    if dow < 5:  # weekdays
        return 1.0 if (6 <= h <= 9 or 17 <= h <= 23) else 0.2
    else:        # weekends
        return 1.0 if (8 <= h <= 23) else 0.3


def compute_internal_gains(weather_index):
    """
    Compute internal heat gains and base electricity load.

    Parameters
    ----------
    weather_index : pandas.DatetimeIndex
        Time index of the weather data

    Returns
    -------
    dict
        Dictionary containing occupancy, internal gains, and base electric load
    """

    occ = weather_index.to_series().apply(occupancy_fraction).values

    # Occupant sensible heat gains
    Q_people_full = 75.0 * n_occ  # [W]

    # Lighting and equipment gains
    Q_lights = LPD * A_cond * occ
    Q_equip = EPD * A_cond * occ

    # Total internal gains
    Q_int = Q_people_full * occ + Q_lights + Q_equip

    # Base electric demand excluding HVAC
    P_base_elec = Q_lights + Q_equip

    return {
        "occ": occ,
        "Q_people_full": Q_people_full,
        "Q_lights": Q_lights,
        "Q_equip": Q_equip,
        "Q_int": Q_int,
        "P_base_elec": P_base_elec,
    }
