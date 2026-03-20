"""

The coefficient of performance (COP) and energy efficiency ratio (EER) are computed using a modified Carnot approach.


"""
import numpy as np

T_indoor_heat = 20.0
T_indoor_cool = 24.0

dT_hex_heating = 6.0
dT_hex_cooling = import numpy as np

T_indoor_heat = 20.0
T_indoor_cool = 24.0

dT_hex_heating = 6.0
dT_hex_cooling = -6.0

deltaT_min = 10.0

eta_heating = 0.40
eta_cooling = 0.25

heat_cutoff_temp = 15.0
cool_cutoff_temp = 23.0

COP_min = 1.0
COP_max = 7.0
EER_min = 1.0
EER_max = 8.0


def to_kelvin(T_c):
    return np.asarray(T_c, dtype=float) + 273.15


def cop_carnot_heating(Tout_C, Tindoor_C=T_indoor_heat):
    Tout_C = np.asarray(Tout_C, dtype=float)

    T_cond_K = to_kelvin(Tindoor_C + dT_hex_heating)
    T_evap_K = to_kelvin(Tout_C - dT_hex_heating)

    delta_T = np.maximum(T_cond_K - T_evap_K, deltaT_min)
    cop_real = eta_heating * (T_cond_K / delta_T)

    return np.clip(cop_real, COP_min, COP_max)


def eer_carnot_cooling(Tout_C, Tindoor_C=T_indoor_cool):
    Tout_C = np.asarray(Tout_C, dtype=float)

    T_cond_K = to_kelvin(Tout_C + dT_hex_cooling)
    T_evap_K = to_kelvin(Tindoor_C - dT_hex_cooling)

    delta_T = np.maximum(T_cond_K - T_evap_K, deltaT_min)
    eer_real = eta_cooling * (T_evap_K / delta_T)
    delta_T = np.clip(delta_T, deltaT_min, 35)

    return np.clip(eer_real, EER_min, EER_max)


def heating_active_mask(Q_heat, Tout_C, cutoff=heat_cutoff_temp):
    Q_heat = np.asarray(Q_heat, dtype=float)
    Tout_C = np.asarray(Tout_C, dtype=float)
    return (Q_heat > 0.0) & (Tout_C <= cutoff)


def cooling_active_mask(Q_cool, Tout_C, cutoff=cool_cutoff_temp):
    Q_cool = np.asarray(Q_cool, dtype=float)
    Tout_C = np.asarray(Tout_C, dtype=float)
    return (Q_cool > 0.0) & (Tout_C >= cutoff)


def compute_heat_pump_electricity(
    Q_heat,
    Q_cool,
    Tout,
    Tindoor_heat_C=T_indoor_heat,
    Tindoor_cool_C=T_indoor_cool,
):
    """
    Parameters
    ----------
    Q_heat : array-like
        Heating thermal demand [kW] or [kWh/timestep]
    Q_cool : array-like
        Cooling thermal demand [kW] or [kWh/timestep]
    Tout : array-like
        Outdoor air temperature [°C]

    Returns
    -------
    dict
        Heat pump performance and electricity use.
    """
    Q_heat = np.asarray(Q_heat, dtype=float)
    Q_cool = np.asarray(Q_cool, dtype=float)
    Tout = np.asarray(Tout, dtype=float)

    if not (Q_heat.shape == Q_cool.shape == Tout.shape):
        raise ValueError("Q_heat, Q_cool, and Tout must have the same shape.")

    Q_heat = np.maximum(Q_heat, 0.0)
    Q_cool = np.maximum(Q_cool, 0.0)

    COP_t_raw = cop_carnot_heating(Tout, Tindoor_C=Tindoor_heat_C)
    EER_t_raw = eer_carnot_cooling(Tout, Tindoor_C=Tindoor_cool_C)

    heating_on = heating_active_mask(Q_heat, Tout)
    cooling_on = cooling_active_mask(Q_cool, Tout) & (~heating_on)

    Q_heat_served = np.where(heating_on, Q_heat, 0.0)
    Q_cool_served = np.where(cooling_on, Q_cool, 0.0)

    P_heat_elec = np.where(heating_on, Q_heat_served / COP_t_raw, 0.0)
    P_cool_elec = np.where(cooling_on, Q_cool_served / EER_t_raw, 0.0)

    return {
        "COP_t": np.where(heating_on, COP_t_raw, np.nan),
        "EER_t": np.where(cooling_on, EER_t_raw, np.nan),
        "Q_heat_served": Q_heat_served,
        "Q_cool_served": Q_cool_served,
        "P_heat_elec": P_heat_elec,
        "P_cool_elec": P_cool_elec,
        "P_hvac_elec": P_heat_elec + P_cool_elec,
        "heating_on": heating_on,
        "cooling_on": cooling_on,
    }
# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

# Keep old function name for compatibility with main.py
compute_hvac_electricity = compute_heat_pump_electricity-6.0

deltaT_min = 10.0

eta_heating = 0.40
eta_cooling = 0.25

heat_cutoff_temp = 15.0
cool_cutoff_temp = 23.0

COP_min = 1.0
COP_max = 7.0
EER_min = 1.0
EER_max = 8.0


def to_kelvin(T_c):
    return np.asarray(T_c, dtype=float) + 273.15


def cop_carnot_heating(Tout_C, Tindoor_C=T_indoor_heat):
    Tout_C = np.asarray(Tout_C, dtype=float)

    T_cond_K = to_kelvin(Tindoor_C + dT_hex_heating)
    T_evap_K = to_kelvin(Tout_C - dT_hex_heating)

    delta_T = np.maximum(T_cond_K - T_evap_K, deltaT_min)
    cop_real = eta_heating * (T_cond_K / delta_T)

    return np.clip(cop_real, COP_min, COP_max)


def eer_carnot_cooling(Tout_C, Tindoor_C=T_indoor_cool):
    Tout_C = np.asarray(Tout_C, dtype=float)

    T_cond_K = to_kelvin(Tout_C + dT_hex_cooling)
    T_evap_K = to_kelvin(Tindoor_C - dT_hex_cooling)

    delta_T = np.maximum(T_cond_K - T_evap_K, deltaT_min)
    eer_real = eta_cooling * (T_evap_K / delta_T)
    delta_T = np.clip(delta_T, deltaT_min, 35)

    return np.clip(eer_real, EER_min, EER_max)


def heating_active_mask(Q_heat, Tout_C, cutoff=heat_cutoff_temp):
    Q_heat = np.asarray(Q_heat, dtype=float)
    Tout_C = np.asarray(Tout_C, dtype=float)
    return (Q_heat > 0.0) & (Tout_C <= cutoff)


def cooling_active_mask(Q_cool, Tout_C, cutoff=cool_cutoff_temp):
    Q_cool = np.asarray(Q_cool, dtype=float)
    Tout_C = np.asarray(Tout_C, dtype=float)
    return (Q_cool > 0.0) & (Tout_C >= cutoff)


def compute_heat_pump_electricity(
    Q_heat,
    Q_cool,
    Tout,
    Tindoor_heat_C=T_indoor_heat,
    Tindoor_cool_C=T_indoor_cool,
):
    """
    Parameters
    ----------
    Q_heat : array-like
        Heating thermal demand [kW] or [kWh/timestep]
    Q_cool : array-like
        Cooling thermal demand [kW] or [kWh/timestep]
    Tout : array-like
        Outdoor air temperature [°C]

    Returns
    -------
    dict
        Heat pump performance and electricity use.
    """
    Q_heat = np.asarray(Q_heat, dtype=float)
    Q_cool = np.asarray(Q_cool, dtype=float)
    Tout = np.asarray(Tout, dtype=float)

    if not (Q_heat.shape == Q_cool.shape == Tout.shape):
        raise ValueError("Q_heat, Q_cool, and Tout must have the same shape.")

    Q_heat = np.maximum(Q_heat, 0.0)
    Q_cool = np.maximum(Q_cool, 0.0)

    COP_t_raw = cop_carnot_heating(Tout, Tindoor_C=Tindoor_heat_C)
    EER_t_raw = eer_carnot_cooling(Tout, Tindoor_C=Tindoor_cool_C)

    heating_on = heating_active_mask(Q_heat, Tout)
    cooling_on = cooling_active_mask(Q_cool, Tout) & (~heating_on)

    Q_heat_served = np.where(heating_on, Q_heat, 0.0)
    Q_cool_served = np.where(cooling_on, Q_cool, 0.0)

    P_heat_elec = np.where(heating_on, Q_heat_served / COP_t_raw, 0.0)
    P_cool_elec = np.where(cooling_on, Q_cool_served / EER_t_raw, 0.0)

    return {
        "COP_t": np.where(heating_on, COP_t_raw, np.nan),
        "EER_t": np.where(cooling_on, EER_t_raw, np.nan),
        "Q_heat_served": Q_heat_served,
        "Q_cool_served": Q_cool_served,
        "P_heat_elec": P_heat_elec,
        "P_cool_elec": P_cool_elec,
        "P_hvac_elec": P_heat_elec + P_cool_elec,
        "heating_on": heating_on,
        "cooling_on": cooling_on,
    }
# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

# Keep old function name for compatibility with main.py
compute_hvac_electricity = compute_heat_pump_electricity


    
