"""

This module converts heating and cooling loads into electrical loads
using temperature-dependent COP and EER curves.

Important note:
The reference benchmark building uses a gas-fired boiler in the source articles.
However, this simplified Python model uses heat pump performance curves
to estimate electrical consumption associated with heating and cooling loads.

COP and EER are computed as functions of outdoor temperature
based on polynomial regressions reported in:

Baglivo et al. (2018)
"Performance Analysis of Air Cooled Heat Pump"


"""

import numpy as np


def cop_35(T):
    """
    Heating COP for water supply temperature Tw = 35°C.

    This function follows the original notebook implementation:
    - one polynomial for T <= 3°C
    - another polynomial for T > 3°C
    - output clipped to a reasonable interval

    Parameters
    ----------
    T : array-like or float
        Outdoor air temperature [°C]

    Returns
    -------
    array-like or float
        COP values [-]
    """

    T = np.asarray(T, dtype=float)

    COP_A = (
        5e-10 * T**6
        + 7e-6 * T**5
        + 2e-5 * T**4
        - 0.0017 * T**3
        + 0.0097 * T**2
        + 0.0787 * T
        + 2.5019
    )

    COP_B = (
        -2e-7 * T**6
        + 2e-5 * T**5
        - 0.0004 * T**4
        + 0.0066 * T**3
        - 0.0606 * T**2
        + 0.4206 * T
        + 2.0482
    )

    COP = np.where(T <= 3.0, COP_A, COP_B)

    return np.clip(COP, 1.0, 6.5)


def eer_6(T):
    """
    Cooling EER for chilled water temperature Tw = 6°C.

    This function follows the original notebook implementation.

    Parameters
    ----------
    T : array-like or float
        Outdoor air temperature [°C]

    Returns
    -------
    array-like or float
        EER values [-]
    """

    T = np.asarray(T, dtype=float)

    EER = (
        -4e-5 * T**3
        + 0.005 * T**2
        - 0.2806 * T
        + 7.7483
    )

    return np.clip(EER, 1.0, 8.0)


def compute_hvac_electricity(Q_heat, Q_cool, Tout):
    """
    Convert heating and cooling loads into HVAC electrical demand.

    Parameters
    ----------
    Q_heat : array-like
        Heating load [W]
    Q_cool : array-like
        Cooling load [W]
    Tout : array-like
        Outdoor air temperature [°C]

    Returns
    -------
    dict
        Dictionary containing:
        - COP_t
        - EER_t
        - P_hvac_elec
    """

    Q_heat = np.asarray(Q_heat, dtype=float)
    Q_cool = np.asarray(Q_cool, dtype=float)
    Tout = np.asarray(Tout, dtype=float)

    COP_t = cop_35(Tout)
    EER_t = eer_6(Tout)

    P_hvac_elec = (Q_heat / COP_t) + (Q_cool / EER_t)

    return {
        "COP_t": COP_t,
        "EER_t": EER_t,
        "P_hvac_elec": P_hvac_elec,
    }
