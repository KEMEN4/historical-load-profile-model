# historical-load-profile-model
Python project for generating historical electricity, cooling, and heating load profiles using physical modeling.


This Python project generates hourly load profiles for:

- heating
- cooling
- electricity consumption

from meteorological data and a simplified thermal model of the building.

---

## Project Structure

data/ → Weather data used as input

results/ → Load profiles generated

notebooks/ → Notebooks used during development

src/ → Python scripts for the model:

- `building_parameters.py`: Building parameters from the articles
- `data_loading.py`: Loading of weather data
- `geometry.py`: Simplified reconstruction of the building geometry
- `model_assumptions.py`: Model assumptions
- `internal_gains.py`: Internal gains (occupants, lighting, equipment)
- `solar_gains.py`: Solar gains
- `simulation.py`: Dynamic thermal simulation of the building
- `cop_model.py`: Calculation of the COP and EER depending on the outside temperature
- `main.py`: Main script that generates the profiles Energy

---

## Weather Data

The weather data comes from **Meteoblue**. 
Brussels weather data (January 1, 2025 - December 31, 2025)

The variables used are:

- outdoor temperature
- global solar radiation

The data is provided as hourly time series in a CSV file.

---

## Building Data

The building parameters come from the following articles:

Attia et al. (2022) – Applied Energy
Rahif et al. (2022) – Building and Environment

These articles use a **reference nZEB (terraced house) building** located in Brussels.

The parameters used include:

- building surface area
- volume
- number of occupants
- window-to-wall ratio
- U-values ​​of the building envelope
- window properties
- infiltration rate

---
Some equations for heat balance and heat transfer
are taken from the **HVAC (Heating, Ventilation and Air Conditioning)** course MA1
---

## Principle of the thermal model

The model is based on a simplified energy balance:

C dTin/dt = H (Tout − Tin) + Qsolar + Qininternal + QHVAC

where:

- Tin: indoor temperature
- Tout: outdoor temperature
- Qsolar: solar gains
- Qininternal: internal gains
- QHVAC: heating or cooling capacity

---

## COP and EER Model

The electrical consumption of the HVAC system is calculated from the **COP (Coefficient of Performance)** and the **EER (Energy Efficiency Ratio)**.

The expressions for COP and EER as a function of outdoor temperature are taken from the article:

Energies (2018) – Heat pump performance curves.

These equations allow us to estimate:

- the electrical power required for heating
- the electrical power required for cooling

---

## Model Execution

To start the simulation:
- run the main script from the root directory of the project:

python src/main.py

This script performs the following steps:
- loads the weather data
- computes geometry and thermal properties
- calculates internal and solar gains
- runs the dynamic thermal simulation
- converts heating and cooling loads into electrical demand

The generated load profiles are saved as a CSV file in:

results/tables/load_profiles_energy_balance.csv

## Weather data

The original model was developed using Meteoblue weather data for Basel.
For this thesis, the weather input has been updated to use hourly data for Brussels (2025) from the NASA POWER database(power access climate data).

The dataset includes:
- Outdoor temperature (T2M)
- Wind speed (WS10M)
- Global solar irradiance (ALLSKY_SFC_SW_DWN)
