# -*- coding: utf-8 -*-
"""
file: multiplicity.py
description:
    This script calculates the multiplicity count of particle events based on the provided 
    history data and multiplicity window configuration.
"""

import logging
import numpy as np
import pandas as pd
from .cython_functs import shift_register_counting

# Import the pre-configured logger
logger = logging.getLogger(__name__)

def multiplicity(ph_df, window_width, tol=1e-6):
    """Calculates the multiplicity count for particle events.

    Args:
        ph_df (pd.DataFrame): Dataframe containing particle history data, including 'particle_type' and 'time'.
        window_width (int or float): The width of the multiplicity window to use for counting.
        tol (float, optional): Tolerance for shift register counting (default is 1e-6).

    Returns:
        counts (pd.Series): The count of windows grouped by particle label.
        total_counts (int): Total number of windows in the data.
    """
    
    logger.info("Starting multiplicity count calculation.")

    # Map particle types to labels ('n' for neutron, 'g' for gamma)
    ph_df["particle_label"] = ph_df.particle_type.map({1: "n", 2: "g", 3: "g"})
    
    logger.debug(f"Particle labels assigned: {ph_df['particle_label'].unique()}")
    
    # Calculate the multiplicity window for each event using shift register counting
    logger.debug(f"Performing shift register counting with window width: {window_width} and tolerance: {tol}")
    ph_df["window"] = shift_register_counting(
        ph_df.index.values, 
        ph_df.time.values, 
        window_width, 
        tol
    )
    
    # Sort the dataframe by window and particle label for consistent grouping
    logger.debug("Sorting the DataFrame by window and particle label.")
    ph_df.sort_values(["window", "particle_label"], inplace=True)

    # Group by window and aggregate particle labels (summing the labels)
    window_df = ph_df.groupby("window").agg({"particle_label": "sum"}).reset_index()
    
    logger.debug(f"Grouped data by window: {window_df.head()}")
    
    # Calculate total window counts and counts per particle label
    total_counts = window_df["particle_label"].count()
    counts = window_df.groupby("particle_label")["window"].count()

    logger.info(f"Multiplicity count calculation complete. Total windows: {total_counts}")
    logger.debug(f"Counts per particle label: {counts}")
    
    return counts, total_counts
