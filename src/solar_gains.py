"""
Solar gains model for the simplified building energy balance.

This module computes solar gains through the glazed area using the
same simplified formulation as in the original notebook.

Article-based inputs:
- A_window
- SHGC

Modelling assumption:
- orientation / utilisation factor (f_orient)

The purpose is to represent solar heat gains in a reduced-order
building model without reproducing the full multizone solar model
from the reference EnergyPlus implementation.
"""

from src.building_parameters import A_window, SHGC

# ============================================================
# MODELLING ASSUMPTION
# ============================================================

# Simplified orientation/utilisation factor
# This factor is used in the notebook to reduce raw incident solar
# radiation to an effective solar gain through windows.
f_orient = 0.6  # [-]


def compute_solar_gains(G):
    """
    Compute solar gains through windows.

    Parameters
    ----------
    G : array-like
        Global solar radiation [W/m²]

    Returns
    -------
    array-like
        Solar gains [W]
    """

    Q_solar = G * A_window * SHGC * f_orient

    return Q_solar
