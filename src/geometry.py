"""
Simplified geometry reconstruction for the benchmark terraced dwelling.

This module derives simplified geometric quantities used in the reduced
Python energy balance model.

The reconstruction is based on:
- article-based parameters from `building_parameters.py`
- modelling assumptions from `model_assumptions.py`

The purpose is not to reproduce the full detailed building geometry from
the original EnergyPlus/DesignBuilder model, but to create a simplified
box-model representation consistent with the notebook implementation.
"""

import math

from .building_parameters import A_cond, floors, WWR
from .model_assumptions import h_floor


def compute_geometry():
    """
    Compute simplified building geometry used in the notebook model.

    Returns
    -------
    dict
        Dictionary containing reconstructed geometry values.
    """

    # Building footprint area [m²]
    A_foot = A_cond / floors

    # Assume square footprint for simplified box model
    side = math.sqrt(A_foot)

    # Perimeter of simplified square plan [m]
    perim = 4.0 * side

    # Total building height [m]
    height = floors * h_floor

    # Gross external wall area [m²]
    A_wall_gross = perim * height

    # Window area from window-to-wall ratio [m²]
    A_window = WWR * A_wall_gross

    # Opaque wall area [m²]
    A_wall_opaque = A_wall_gross - A_window

    # Simplified roof and ground areas [m²]
    A_roof = A_foot
    A_ground = A_foot

    return {
        "A_foot": A_foot,
        "side": side,
        "perim": perim,
        "height": height,
        "A_wall_gross": A_wall_gross,
        "A_window": A_window,
        "A_wall_opaque": A_wall_opaque,
        "A_roof": A_roof,
        "A_ground": A_ground,
    }
