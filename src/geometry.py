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

from .building_parameters import A_cond, floors, A_window
from .model_assumptions import h_floor


def compute_geometry():
    """
    Compute simplified rectangular building geometry.
    """

    # Footprint area
    A_foot = A_cond / floors

    # Assume rectangular terraced house
    depth = 8.0
    width = A_foot / depth

    # Perimeter
    perim = 2.0 * (width + depth)

    # Building height
    height = floors * h_floor

    # Gross external wall area
    A_wall_gross = perim * height

    # Use article-based window area (do NOT recompute it)
    A_wall_opaque = A_wall_gross - A_window

    # Roof and ground
    A_roof = A_foot
    A_ground = A_foot

    return {
        "A_foot": A_foot,
        "width": width,
        "depth": depth,
        "perim": perim,
        "height": height,
        "A_wall_gross": A_wall_gross,
        "A_window": A_window,
        "A_wall_opaque": A_wall_opaque,
        "A_roof": A_roof,
        "A_ground": A_ground,
    }
