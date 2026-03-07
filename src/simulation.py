"""
Dynamic building simulation for the simplified energy balance model.

This module performs the hourly simulation of indoor temperature,
heating load, and cooling load using the same logic as the original
notebook implementation.

Inputs:
- outdoor temperature
- solar gains
- internal gains
- thermal properties

Outputs:
- indoor temperature
- HVAC load
- heating demand
- cooling demand
"""

import numpy as np

from src.building_parameters import T_heat_set
from src.model_assumptions import T_cool_set


def run_simulation(Tout, Q_solar, Q_int, thermal_props, dt=3600.0):
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
        Dictionary containing thermal properties:
        - H_total
        - C
    dt : float, optional
        Time step in seconds. Default is 3600 s (1 hour).

    Returns
    -------
    dict
        Dictionary containing:
        - Tin
        - Q_hvac
        - Q_heat
        - Q_cool
    """

    Tout = np.asarray(Tout, dtype=float)
    Q_solar = np.asarray(Q_solar, dtype=float)
    Q_int = np.asarray(Q_int, dtype=float)

    # ============================================================
    # Optional uncertainty on outdoor temperature
    # ============================================================
    #
    # Supervisor remark:
    # "If you want you can start with adding uncertainty to the code,
    # for example on the outside temperature. This then will affect
    # your results for the demand and COP."
    #
    # The baseline version below keeps the simulation identical to the
    # original notebook.
    #
    # To test the effect of uncertainty on outdoor temperature,
    # uncomment the following two lines:
    #
    # sigma_T = 1.0  # standard deviation of temperature uncertainty [°C]
    # Tout = Tout + np.random.normal(0, sigma_T, size=len(Tout))
    #
    # This can later be used to compare:
    # - baseline demand vs uncertain demand
    # - baseline COP vs uncertain COP
    #

    N = len(Tout)

    H_total = thermal_props["H_total"]
    C = thermal_props["C"]

    Tin = np.zeros(N)
    Q_hvac = np.zeros(N)
    Q_heat = np.zeros(N)
    Q_cool = np.zeros(N)

    # Initial indoor temperature
    Tin[0] = T_heat_set

    for k in range(N - 1):

        # Free-floating indoor temperature without HVAC
        Tin_free = Tin[k] + (dt / C) * (
            H_total * (Tout[k] - Tin[k]) + Q_solar[k] + Q_int[k]
        )

        # Heating mode
        if Tin_free < T_heat_set:
            Q_needed = ((T_heat_set - Tin[k]) * C / dt) - (
                H_total * (Tout[k] - Tin[k]) + Q_solar[k] + Q_int[k]
            )
            Q_hvac[k] = max(Q_needed, 0.0)

        # Cooling mode
        elif Tin_free > T_cool_set:
            Q_needed = ((T_cool_set - Tin[k]) * C / dt) - (
                H_total * (Tout[k] - Tin[k]) + Q_solar[k] + Q_int[k]
            )
            Q_hvac[k] = min(Q_needed, 0.0)

        # No HVAC needed
        else:
            Q_hvac[k] = 0.0

        # Separate heating and cooling loads
        Q_heat[k] = max(Q_hvac[k], 0.0)
        Q_cool[k] = max(-Q_hvac[k], 0.0)

        # Update indoor temperature with HVAC
        Tin[k + 1] = Tin[k] + (dt / C) * (
            H_total * (Tout[k] - Tin[k]) + Q_solar[k] + Q_int[k] + Q_hvac[k]
        )

    # Copy last values for convenience
    Q_heat[-1] = Q_heat[-2]
    Q_cool[-1] = Q_cool[-2]
    Q_hvac[-1] = Q_hvac[-2]

    return {
        "Tin": Tin,
        "Q_hvac": Q_hvac,
        "Q_heat": Q_heat,
        "Q_cool": Q_cool,
    }
