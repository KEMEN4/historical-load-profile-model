"""
Thermal properties and heat transfer coefficients for the simplified
building energy balance model.

This module computes:

- transmission heat losses (UA)
- infiltration heat losses (H_inf)
- total heat loss coefficient (H_total)
- effective building thermal capacitance

The equations follow standard HVAC heat transfer formulations and
match the implementation used in the original notebook.
"""

from src.building_parameters import *
from src.model_assumptions import *
from src.geometry import compute_geometry


def compute_thermal_properties():

    geom = compute_geometry()

    A_wall_opaque = geom["A_wall_opaque"]
    A_window = geom["A_window"]
    A_roof = geom["A_roof"]
    A_ground = geom["A_ground"]

    # ============================================================
    # Transmission heat transfer
    # UA = Σ(U_i * A_i)
    # ============================================================

    UA = (
        U_wall * A_wall_opaque
        + U_window * A_window
        + U_roof * A_roof
        + U_ground * A_ground
    )

    # ============================================================
    # Infiltration heat transfer
    # H_inf = rho_air * cp_air * ACH * V / 3600
    # ============================================================

    H_inf = rho_air * cp_air * ACH_50Pa * V_build / 3600.0

    # ============================================================
    # Total heat transfer coefficient
    # ============================================================

    H_total = UA + H_inf

    # ============================================================
    # Thermal capacitance approximation
    # ============================================================

    C_air = rho_air * cp_air * V_build

    C = effective_mass_factor * C_air

    return {
        "UA": UA,
        "H_inf": H_inf,
        "H_total": H_total,
        "C_air": C_air,
        "C": C,
    }
