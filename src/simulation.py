"""
Dynamic building simulation for the simplified energy balance model.

This version follows a physics-based logic:
- free-floating indoor temperature is first computed
- heating is applied only if indoor temperature drops below heating setpoint
- cooling is applied only if indoor temperature exceeds cooling setpoint
- natural ventilation is used as a passive summer comfort mechanism
  when indoor air is warm and outdoor air is cooler


"""

import numpy as np
import pandas as pd
from pandas.io.formats.format import return_docstring

from src.building_parameters import T_heat_set
from src.model_assumptions import T_cool_set


def heating_setpoint(ts):
    """
    Simplified heating setpoint schedule.

    Based on the benchmark article:
    - living areas around 21°C
    - lower temperatures at night / reduced activity periods

    This is a simplified whole-building representation.
    """
    h = ts.hour

    # Lower night setpoint
    if 0 <= h < 6:
        return 17.0
    elif 6 <=h <9:
        return 20.0
    elif 9 <=h < 17:
        return 19.0
    else:
        return 21.0





def run_simulation(Tout, Q_solar, Q_int, thermal_props, weather_index, dt=3600.0):
    """
    Run the hourly simplified building energy simulation.

    Parameters
    ----------
    Tout : array-like
        Outdoor air temperature [°C]
    Q_solar : array-like
        Solar gains [W]
    Q_int : array-like
        Internal gains [W]
    thermal_props : dict
        Dictionary containing:
        - H_total
        - C
    weather_index : pandas.DatetimeIndex
        Time index of the simulation
    dt : float, optional
        Time step in seconds

    Returns
    -------
    dict
        Dictionary with:
        - Tin
        - Q_hvac
        - Q_heat
        - Q_cool
    """

    Tout = np.asarray(Tout, dtype=float)
    Q_solar = np.asarray(Q_solar, dtype=float)
    Q_int = np.asarray(Q_int, dtype=float)
    weather_index = pd.DatetimeIndex(weather_index)

    N = len(Tout)

    H_total = thermal_props["H_total"]
    C = thermal_props["C"]

    Tin = np.zeros(N)
    Q_hvac = np.zeros(N)
    Q_heat = np.zeros(N)
    Q_cool = np.zeros(N)

    Tin[0] = T_heat_set

    # Deadband to avoid unrealistic switching
    deadband = 0.5  # °C

    for k in range(N - 1):
        ts = weather_index[k]
        T_heat_set_k = heating_setpoint(ts)

        # Heating allowed depending on outdoor temperature
        #if Tout[k]> 18:
          #  heating_allowed = False
        #else:
         #   heating_allowed = True
        heating_allowed = Tout[k] <= 16.0

        # ------------------------------------------------------------
        # Natural ventilation / window opening
        # ------------------------------------------------------------
        # Inspired by the Brussels benchmark article:
        # occupants frequently open windows in summer to reduce overheating.
        # We do not force it by month; we activate it only when physically useful.
        #
        # Conditions:
        # - indoor temperature above cooling comfort threshold
        # - outdoor air cooler than indoor air
        # - mostly useful during daytime/evening warm periods
       # if Tin[k] > T_cool_set and Tout[k] < Tin[k]:
           # Q_natvent = -500.0  # W, simplified passive cooling assumption
        #else:
         #   Q_natvent = 0.0
        if Tin[k] > T_cool_set and Tout[k] < Tin[k] and 8 <= ts.hour <= 22:
            Q_natvent = -300.0 * (Tin[k] - Tout[k])
        else:
            Q_natvent = 0.0

        # ------------------------------------------------------------
        # Free-floating indoor temperature without active HVAC
        # ------------------------------------------------------------
        Tin_free = Tin[k] + (dt / C) * (
            H_total * (Tout[k] - Tin[k]) + Q_solar[k] + Q_int[k] + Q_natvent
        )

        # ------------------------------------------------------------
        # Heating
        # ------------------------------------------------------------
        if Tin_free < (T_heat_set_k - deadband) and heating_allowed:
            Q_needed = ((T_heat_set_k - Tin[k]) * C / dt) - (
                H_total * (Tout[k] - Tin[k]) + Q_solar[k] + Q_int[k] + Q_natvent
            )
            Q_hvac[k] = max(Q_needed, 0.0)

        # ------------------------------------------------------------
        # Cooling
        # ------------------------------------------------------------
        elif Tin_free > (T_cool_set + deadband):
            Q_needed = ((T_cool_set - Tin[k]) * C / dt) - (
                H_total * (Tout[k] - Tin[k]) + Q_solar[k] + Q_int[k] + Q_natvent
            )
            Q_hvac[k] = min(Q_needed, 0.0)

        # ------------------------------------------------------------
        # No HVAC
        # ------------------------------------------------------------
        else:
            Q_hvac[k] = 0.0

        # Split loads
        Q_heat[k] = max(Q_hvac[k], 0.0)
        Q_cool[k] = max(-Q_hvac[k], 0.0)

        # Update indoor temperature with actual HVAC
        Tin[k + 1] = Tin[k] + (dt / C) * (
            H_total * (Tout[k] - Tin[k]) + Q_solar[k] + Q_int[k] + Q_natvent + Q_hvac[k]
        )

    # Copy last values
    Q_heat[-1] = Q_heat[-2]
    Q_cool[-1] = Q_cool[-2]
    Q_hvac[-1] = Q_hvac[-2]

    return {
        "Tin": Tin,
        "Q_hvac": Q_hvac,
        "Q_heat": Q_heat,
        "Q_cool": Q_cool,
    }
