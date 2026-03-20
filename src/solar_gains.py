"""
Solar gains model for the simplified building energy balance.

This module computes solar gains through the total glazed area using a
simplified window-based formulation.

The formulation follows the same physical structure as standard
building energy balance models:
    Q_solar = I * A_window * g * shading * utilisation

where:
- I is the available solar irradiance
- A_window is the total glazed area
- g is the solar heat gain coefficient (SHGC)
- shading accounts for roller shutters / solar protection
- utilisation accounts for the aggregated orientation effect

This remains a simplified whole-building approximation.
"""

import numpy as np
import pandas as pd

from src.building_parameters import A_window, SHGC

# Aggregated whole-building utilisation/orientation factor [-]
# Keeps the model simple while avoiding full facade-by-facade decomposition.
f_orient = 0.50

# Shading assumptions [-]
# Roller shutters reduce solar gains when solar radiation is high.
F_SHADING_OPEN = 1.00
F_SHADING_CLOSED = 0.40

# Radiation threshold above which shutters are assumed to be active [W/m²]
G_SHADING_THRESHOLD = 250.0


def compute_solar_gains(G, weather_index):
    """
    Compute solar gains through windows.

    Parameters
    ----------
    G : array-like
        Global solar radiation [W/m²]
    weather_index : pandas.DatetimeIndex
        Time index (currently kept for future schedule extensions)

    Returns
    -------
    np.ndarray
        Solar gains [W]
    """
    G = np.asarray(G, dtype=float)
    _ = pd.DatetimeIndex(weather_index)  # kept for possible future logic

    # No negative radiation
    G = np.maximum(G, 0.0)

    # Simplified dynamic shutter logic:
    # shutters close only when radiation is sufficiently high
    f_shading = np.where(G >= G_SHADING_THRESHOLD, F_SHADING_CLOSED, F_SHADING_OPEN)

    Q_solar = G * A_window * SHGC * f_orient * f_shading

    return Q_solar
