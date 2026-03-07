"""
Building parameters taken directly from the reference-building tables used in:

1) Attia et al. (2022), Applied Energy
"Developing a benchmark model for renovated, nearly zero-energy, terraced dwellings"

2) Rahif et al. (2022), Building and Environment
"Impact of climate change on nearly zero-energy dwelling in temperate climate"

Both articles use the same benchmark terraced nZEB dwelling in Brussels.
This file intentionally contains only parameters explicitly reported in the articles.
"""

# ============================================================
# Reference building: directly reported article values
# ============================================================

# Geometry / building description
floors = 3

A_total = 259.0            # [m²] total area
A_cond = 173.0             # [m²] conditioned area
A_uncond = 86.0            # [m²] unconditioned area

V_build = 873.0            # [m³] total volume

A_wall_ext = 122.0         # [m²] external wall area
A_roof = 91.0              # [m²] roof area
A_floor = 259.0            # [m²] floor area
A_window = 41.0            # [m²] windows area

# Occupancy
n_occ = 4
occupancy_density = 43.0   # [m²/person]

# Window / solar properties
WWR = 0.19                 # [-] window-to-wall ratio
U_window = 1.2             # [W/m²K]
g_window = 0.6             # [-]
SHGC = 0.6                 # [-]
wall_absorptance = 0.9     # [-]

# Envelope thermal properties
U_wall = 0.4               # [W/m²K]
U_roof = 0.3               # [W/m²K]
U_ground = 0.3             # [W/m²K]
U_attic_floor = 0.8        # [W/m²K]

# Airtightness / ventilation
ACH_50Pa = 1.58            # [1/h]
ACH_4Pa = 0.3              # [1/h]

vent_living_supply = 25.0      # [m³/h]
vent_living_extract = 30.0     # [m³/h]
vent_bedroom_supply = 25.0     # [m³/h]
vent_bathroom_extract = 25.0   # [m³/h]

mvhr_efficiency = 0.92         # [-]

# Heating / operation
COP_heating_system = 0.88      # [-]
T_heat_set = 21.0              # [°C]
T_heat_setback = 12.0          # [°C]

# Lighting
LPD_min = 8.0                  # [W/m²]
LPD_max = 10.0                 # [W/m²]

# Systems
heating_system = "gas-fired boiler"
heating_fuel = "natural gas"

# Benchmark annual value
average_consumption = 29.0     # [kWh/m²/year]
