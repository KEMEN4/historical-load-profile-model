"""
Model assumptions used in the simplified physics-based building model.

These parameters are not explicitly reported in the benchmark-building
tables from the reference articles. They are introduced to complete the
reduced-order energy balance model implemented in Python.

The values are based on typical assumptions used in building energy
modelling and HVAC literature.
"""

# ============================================================
# Indoor comfort assumptions
# ============================================================

# Cooling setpoint
# Not provided in the benchmark tables.
# A typical residential comfort temperature is assumed.

T_cool_set = 25.0      # [°C]


# ============================================================
# Internal equipment loads
# ============================================================

# Equipment power density
# Not explicitly given in the articles.
# Typical residential plug loads range between 3–5 W/m².

EPD = 8.0              # [W/m²]


# ============================================================
# Air properties (standard HVAC values)
# ============================================================

rho_air = 1.225          # air density [kg/m³]
cp_air = 1004.0        # air specific heat capacity [J/kgK]


# ============================================================
# Building thermal inertia approximation
# ============================================================

# Effective thermal mass factor used in simplified 1-node models.
# Typical values range between 10 and 20 depending on building mass.

effective_mass_factor = 15.0


# ============================================================
# Simplified geometry reconstruction
# ============================================================

# Typical floor-to-floor height used to reconstruct the building
# geometry in the simplified box-model approach.

h_floor = 2.8          # [m]
