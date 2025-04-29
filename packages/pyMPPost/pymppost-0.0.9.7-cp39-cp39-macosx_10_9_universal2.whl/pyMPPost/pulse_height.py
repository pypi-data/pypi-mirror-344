# -*- coding: utf-8 -*-
"""
file: pulse_height.py
description: 
    This module calculates pulse height by applying light production, pulse creation, 
    and resolution effects (time and energy) for particle events.
"""

import logging
import numpy as np
from .cython_functs import calc_pulses

# Import the pre-configured logger from the main logging configuration
logger = logging.getLogger(__name__)

def pulse_height(plm_ddf, client, mats, threshold, time_res=False, energy_res=False, seed=0, tol=1e-6):
    """Calculates pulse height for particle events based on light production and pulse creation.

    Args:
        plm_ddf (Dask DataFrame): Particle event data.
        client (Dask Client): Dask client for distributed computation.
        mats (list of dict): Materials' calibration and resolution data.
        threshold (tuple): Lower and upper bounds for light filtering.
        time_res (bool): Apply time resolution if True.
        energy_res (bool): Apply energy resolution if True.
        tol (float): Tolerance for pulse creation.

    Returns:
        PH_df (pd.DataFrame): Pulse height data.
        total_count (int): Total number of entries.
        neutron_count (int): Number of neutron entries.
    """
    logger.info("Starting pulse height calculation.")
    
    # Logging input parameters
    logger.debug(f"Threshold: {threshold}, Time Resolution: {time_res}, Energy Resolution: {energy_res}, Seed: {seed}, Tolerance: {tol}")
    
    # Calculate Light
    meta = plm_ddf._meta.assign(light=[])
    logger.debug("Calculating light for each event...")
    plm_ddf = plm_ddf.map_partitions(lambda df: df.assign(light=_light_helper(df, mats)), meta=meta)

    # Generate Pulses
    pgt_arr = np.array([mat["pulse_creation"]["pgt"] / 10.0 for mat in mats])
    dt_arr = np.array([mat["pulse_creation"]["dt"] / 10.0 for mat in mats])

    meta = meta.assign(pulse=[])
    logger.debug("Generating pulses...")
    pulses_q = plm_ddf.map_partitions(lambda df: df.assign(pulse=_pulse_helper(df, pgt_arr, dt_arr, tol)), meta=meta)

    # Sum Light by Pulse
    pulses_q = pulses_q.groupby(by=["history", "cell", "pulse"]).agg({
        'particle_type': 'first', 'mat_num': 'first', 'time': 'first', 'light': 'sum'
    })

    # Log details about pulse aggregation
    logger.debug("Aggregating pulses by history, cell, and pulse.")

    # Check and apply resolution sub-modules
    pulse_meta = pulses_q._meta
    gen = np.random.default_rng() if seed == 0 else np.random.default_rng(seed)
    
    if time_res:
        logger.debug("Applying time resolution...")
        pulses_q = pulses_q.map_partitions(lambda df: df.assign(time=_time_res(df, mats, gen)), meta=pulse_meta)
    
    if energy_res:
        logger.debug("Applying energy resolution...")
        pulses_q = pulses_q.map_partitions(lambda df: df.assign(light=_energy_res(df, mats, gen)), meta=pulse_meta)

    logger.info("Starting pulse height computation...")
    PH_df = client.compute(pulses_q).result().reset_index(["cell", "pulse"])
    
    # Filter pulse heights based on threshold
    PH_df = PH_df[PH_df["pulse"] >= 0]
    PH_df = PH_df[(PH_df["light"] >= threshold[0]) & (PH_df["light"] <= threshold[1])]

    logger.debug(f"Filtered pulse height data: {len(PH_df)} entries after applying threshold.")
    
    logger.info("Pulse height computation complete.")
    
    # Log final counts
    total_count = len(PH_df)
    neutron_count = len(PH_df[PH_df["particle_type"] == 1])
    logger.info(f"Total number of entries: {total_count}")
    logger.info(f"Number of neutron entries: {neutron_count}")

    return PH_df, (total_count, neutron_count)


def _light_helper(df, mats):
    """Helper function to calculate the light value from the respective material's Birk's table.

    Args:
        df (pd.DataFrame): DataFrame with particle event data.
        mats (list of dict): List of materials and their calibration information.

    Returns:
        np.ndarray: Array of calculated light values for each particle.
    """
    logger.debug("Calculating light for particle events...")
    conditions = []
    choices = []

    for i, mat in enumerate(mats):
        cal = mat["calibration"]
        mat_type = mat["mat_type"]

        if mat_type == 1:
            # Neutron and gamma calculations for material type 1
            conditions.append((df["mat_num"] == i) & (df["particle_type"] != 1))
            choices.append(df["energy_deposited"] * cal["photon"][0] + cal["photon"][1])
            
            # Neutron calculations for specific target nuclei
            conditions.append((df["mat_num"] == i) & (df["particle_type"] == 1) & 
                              ((df["target_nucleus"] == 6000) | (df["target_nucleus"] == 6012) | 
                               (df["target_nucleus"] == 6013)))
            choices.append(df["energy_deposited"] * cal["carbon"])
            
            # Neutron calculation for target nucleus 1001
            conditions.append((df["mat_num"] == i) & (df["particle_type"] == 1) & (df["target_nucleus"] == 1001))
            choices.append(np.interp(df["energy_deposited"], cal["birks_energy"], cal["birks_light"]))
        else:
            # Photon calculations for other material types
            conditions.append((df["mat_num"] == i))
            choices.append(df["energy_deposited"] * cal["photon"][0] + cal["photon"][1])
    logger.debug("Light calculation completed.")
    print(df["mat_num"])
    return np.select(conditions, choices)


def _pulse_helper(df, pgt_arr, dt_arr, tol):
    """Helper function to calculate pulse information using a Cython function.

    Args:
        df (pd.DataFrame): DataFrame containing particle event data.
        pgt_arr (np.ndarray): Array of pulse generation thresholds.
        dt_arr (np.ndarray): Array of time window thresholds.
        tol (float): Tolerance for pulse creation.

    Returns:
        np.ndarray: Array of calculated pulse information.
    """
    logger.debug("Calculating pulse information...")
    return calc_pulses(df.index.values, df.cell.values, df.time.values, df.mat_num.values, pgt_arr, dt_arr, tol)


def _time_res(df, mats, gen):
    """Computes random time broadening (resolution) for particle events.

    Args:
        df (pd.DataFrame): DataFrame with particle event data.
        mats (list of dict): List of materials with time resolution data.
        gen (np.random.Generator): Random number generator.

    Returns:
        np.ndarray: Time-resolved particle times.
    """
    logger.debug("Applying time resolution...")
    conditions = [(df["mat_num"] == i) for i in range(len(mats))]
    choices = [mat["resolution"]["time"] / 10.0 for mat in mats]

    time_res = np.select(conditions, choices)
    return gen.normal(loc=df["time"], scale=time_res)


def _energy_res(df, mats, gen):
    """Computes random energy broadening (resolution) for particle events.

    Args:
        df (pd.DataFrame): DataFrame with particle event data.
        mats (list of dict): List of materials with energy resolution data.
        gen (np.random.Generator): Random number generator.

    Returns:
        np.ndarray: Energy-resolved particle light values.
    """
    logger.debug("Applying energy resolution...")
    conditions = []
    choices = []

    for i, mat in enumerate(mats):
        mat_type = mat["mat_type"]
        en_res_p = mat["resolution"]["energy"]["photon"]

        if mat_type == 1:
            en_res_n = mat["resolution"]["energy"]["neutron"]

            # Non-neutron (photon) energy resolution
            conditions.append((df["mat_num"] == i) & (df["particle_type"] != 1))
            choices.append(df["light"] * np.sqrt((en_res_p[0]**2) + ((en_res_p[1]**2) / df["light"]) +
                                                 ((en_res_p[2]**2) / (df["light"]**2))))

            # Neutron energy resolution
            conditions.append((df["mat_num"] == i) & (df["particle_type"] == 1))
            choices.append(df["light"] * np.sqrt((en_res_n[0]**2) + ((en_res_n[1]**2) / df["light"]) +
                                                 ((en_res_n[2]**2) / (df["light"]**2))))
        else:
            # Photon energy resolution for other material types
            conditions.append((df["mat_num"] == i))
            choices.append(df["light"] * np.sqrt((en_res_p[0]**2) + ((en_res_p[1]**2) / df["light"]) +
                                                 ((en_res_p[2]**2) / (df["light"]**2))))

    logger.debug("Energy resolution applied.")
    en_half_max = np.select(conditions, choices)
    en_sd = en_half_max / (2 * np.sqrt(2.0 * np.log(2)))
    return gen.normal(loc=df["light"], scale=en_sd)
