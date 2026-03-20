"""
Internal gains model for the simplified building energy balance.

This module computes:
- occupancy profile
- occupant heat gains
- lighting gains
- equipment gains
- total internal gains
- base electric load (non-HVAC)

Refinement inspired by the reference article:
- living areas: 12 W/m²
- bedrooms: 8 W/m²
- lighting schedule varies by hour and season
"""

import numpy as np

from src.building_parameters import A_cond, n_occ
from src.model_assumptions import EPD

# Article-based lighting power densities
LPD_LIVING = 12.0   # [W/m²]
LPD_BEDROOM = 8.0   # [W/m²]

# Simplified whole-building weighted average
# Assumption: 60% living area, 40% bedroom area
LPD = 0.6 * LPD_LIVING + 0.4 * LPD_BEDROOM   # = 10.4 W/m²


def occupancy_fraction(ts):
    """
    Simplified residential occupancy schedule.
    """
    h = ts.hour
    dow = ts.dayofweek

    if dow < 5:  # weekdays
        if 6 <= h <= 9 or 17 <= h <= 23:
            return 1.0
        else:
            return 0.1
    else:  # weekends
        if 8 <= h <= 23:
            return 1.0
        else:
            return 0.1


def lighting_fraction(ts):
    """
    Simplified lighting schedule.

    Inspired by the article:
    - more lighting in the morning and evening
    - winter extension of lighting use
    """
    h = ts.hour
    month = ts.month

    # Base hourly profile
    if 6 <= h <= 8 or 18 <= h <= 23:
        frac = 1.0
    elif 9 <= h <= 16:
        frac = 0.3
    else:
        frac = 0.1

    # Winter extension:
    # article mentions extending living area lighting
    # 2 h after 08:00 and 1 h before 17:00
    if month in [11, 12, 1, 2]:
        if 8 <= h <= 10 or 16 <= h <= 17:
            frac = max(frac, 0.6)

    return frac


def compute_internal_gains(weather_index, G_Wm2=None):
    """
    Compute internal heat gains and base electricity load.

    Parameters
    ----------
    weather_index : pandas.DatetimeIndex
        Time index of the weather data
    G_Wm2 : array-like, optional
        Global solar radiation [W/m²].
        Used to reduce lighting gains when daylight is available.

    Returns
    -------
    dict
        Dictionary containing occupancy, internal gains, and base electric load
    """

    occ = weather_index.to_series().apply(occupancy_fraction).values
    light_sched = weather_index.to_series().apply(lighting_fraction).values

    # Occupant sensible heat gains
    Q_people_full = 75.0 * n_occ  # [W]

    # Lighting factor = occupancy × lighting schedule
    light_factor = occ * light_sched

    # Daylight correction for lighting
    if G_Wm2 is not None:
        G_Wm2 = np.asarray(G_Wm2)
        light_factor = light_factor.copy()
        light_factor[G_Wm2 > 200] *= 0.5
        light_factor[G_Wm2 > 400] *= 0.7

    # Lighting and equipment gains
    Q_lights = LPD * A_cond * light_factor
    Q_equip = EPD * A_cond * (0.65+ 0.35*occ)

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
