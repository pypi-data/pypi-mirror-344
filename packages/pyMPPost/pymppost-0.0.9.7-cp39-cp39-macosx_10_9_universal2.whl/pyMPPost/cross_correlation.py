import numpy as np
import pandas as pd
import logging

# Initialize logger
logger = logging.getLogger(__name__)

def cross_correlation(ph_df, start_detectors):
    """
    Calculates the cross-correlation between different detectors.
    
    Args:
        ph_df (pd.DataFrame): Dataframe containing particle history data, including 
                              'cell', 'history', 'particle_type', and 'time'.
        start_detectors (list): List of start detectors for cross-correlation calculation.
    
    Returns:
        dict: A dictionary where each key is a start detector, and the value is a tuple
              of (time_diff_array, labels_array) for that detector.
    """
    
    # Mapping particle types to labels
    ph_df["particle_label"] = ph_df.particle_type.map({1: "n", 2: "g", 3: "g"})

    # Initialize a dictionary to store results for each start detector
    cc_results = {}

    # Loop through each start detector to calculate cross-correlation
    for start_detect in start_detectors:
        logger.info(f"Processing cross-correlation for start detector: {start_detect}")

        # Filter the dataframe to only include relevant events
        # Filter rows where both start and other detectors exist in the same history
        filtered_df = ph_df[
            (ph_df["cell"] == start_detect) | ph_df.groupby("history")["cell"].transform(lambda x: start_detect in x.values)
        ]

        # Ensure there are enough data points for cross-correlation
        if filtered_df.empty:
            logger.warning(f"No data found for start detector: {start_detect}")
            continue

        # Separate the dataframe into start and other detectors' data
        start_df = filtered_df[filtered_df["cell"] == start_detect]
        oth_df = filtered_df[filtered_df["cell"] != start_detect]

        # Split the data based on history for cross-correlation
        computed1 = np.split(start_df[["time", "particle_label"]].values,
                             np.unique(start_df.index.values, return_index=True)[1][1:])
        computed2 = np.split(oth_df[["time", "particle_label"]].values,
                             np.unique(oth_df.index.values, return_index=True)[1][1:])

        # Compute time differences and particle label combinations for cross-correlation
        time_data = [
            np.subtract.outer(oth[:, 0], start[:, 0]).flatten()
            for start, oth in zip(computed1, computed2)
        ]
        label_data = [
            np.add.outer(start[:, 1], oth[:, 1]).flatten()
            for start, oth in zip(computed1, computed2)
        ]

        # Convert time differences and labels into NumPy arrays
        time_diff_array = np.concatenate(time_data)
        labels_array = np.concatenate(label_data)

        # Store the result in the dictionary with the start detector as the key
        cc_results[start_detect] = (time_diff_array, labels_array)

        logger.info(f"Completed cross-correlation for start detector: {start_detect}")

    return cc_results
