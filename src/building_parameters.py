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

A_total = 259.0            # [m²] total floor area
A_cond = 173.0             # [m²] conditioned area
A_uncond = 86.0            # [m²] unconditioned (approx.)

V_build = 873.0            # [m³] building volume

A_wall_ext = 122.0         # [m²] external wall area
A_roof = 91.0              # [m²] roof area
A_floor = 259.0            # [m²] total floor area
A_window = 41.0            # [m²] window area

# ------------------------------------------------------------
# Occupancy
# ------------------------------------------------------------
n_occ = 4
occupancy_density = 43.0   # [m²/person]

# ------------------------------------------------------------
# Window / solar properties
# ------------------------------------------------------------
WWR = 0.19                 # [-] window-to-wall ratio
U_window = 1.2             # [W/m²K]
g_window = 0.6             # [-]
SHGC = 0.6                 # [-]
wall_absorptance = 0.9     # [-]

# ------------------------------------------------------------
# Envelope thermal properties
# ------------------------------------------------------------
U_wall = 0.4               # [W/m²K]
U_roof = 0.3               # [W/m²K]
U_ground = 0.3             # [W/m²K]
U_attic_floor = 0.8        # [W/m²K]

# ------------------------------------------------------------
# Airtightness / infiltration
# ------------------------------------------------------------
ACH_50Pa = 1.58            # [1/h] air change rate at 50 Pa
q50 = 3.6                  # [m³/h·m²] infiltration rate (approx.)

# ------------------------------------------------------------
# Ventilation
# ------------------------------------------------------------
vent_living_supply = 25.0      # [m³/h]
vent_living_extract = 30.0     # [m³/h]

vent_bedroom_supply = 25.0     # [m³/h]
vent_bathroom_extract = 25.0   # [m³/h]

mvhr_efficiency = 0.92         # [-] heat recovery efficiency

# ------------------------------------------------------------
# Heating / operation
# ------------------------------------------------------------
T_heat_set= 21.0       # [°C]
T_heat_set_bedroom = 18.0      # [°C]
T_heat_set_bathroom = 16.0     # [°C]
T_heat_setback = 12.0          # [°C]

# System type
heating_system = "gas condensing boiler"
heating_fuel = "natural gas"

# Approximate system efficiency
system_efficiency = 0.88       # [-] (from table / COP equivalent)

# ------------------------------------------------------------
# Internal gains
# ------------------------------------------------------------

# Lighting
LPD_living = 12.0              # [W/m²]
LPD_bedroom = 8.0              # [W/m²]

# Plug loads
plug_load_density = EPD = 8.0        # [W/m²]

# ------------------------------------------------------------
# Domestic hot water / usage
# ------------------------------------------------------------
DHW_per_person = 30.0          # [L/person/day]
water_use_total = 62.0         # [L/person/day]

cooking_time = 40.0            # [min/day] (approx. 40–60)

# ------------------------------------------------------------
# Renewable energy
# ------------------------------------------------------------
PV_production = 3000.0         # [kWh/year]
electricity_demand = 3600.0    # [kWh/year]

# ------------------------------------------------------------
# Climate (from article context)
# ------------------------------------------------------------
HDD = 2391                    # heating degree days
CDD = 36                      # cooling degree days

# ------------------------------------------------------------
# Benchmark annual energy use
# ------------------------------------------------------------
heating_EUI = 16.7            # [kWh/m²/year]
electricity_EUI = 12.0        # [kWh/m²/year]

average_consumption = 28.7    # [kWh/m²/year] ≈ 29
