#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file: pulse_height.py
description: 
    This script processes MCNP-Polimi simulation results by running modules 
    such as pulse height, cross-correlation, and multiplicity, and 
    generating a summary of the results.
"""

import argparse
import datetime
import logging
import os
import time

import dask.dataframe as dd
import numpy as np
import toml
from dask.distributed import LocalCluster

from .pulse_height import pulse_height
from .cross_correlation import cross_correlation
from .multiplicity import multiplicity

def main():
    """Reads input file, configures logging, and starts Dask cluster for processing."""
    parser = argparse.ArgumentParser(
        prog='pyMPPost',
        description='Process MCNP-Polimi simulation results.',
        epilog='See the documentation for more details.'
    )
    
    # Add argument for input file
    parser.add_argument('input_file', help='Path to the input TOML configuration file.')
    args = parser.parse_args()
    
    # Load configuration from TOML file
    with open(args.input_file) as toml_file:
        input_toml = toml.load(toml_file)
    input_toml["input_file"] = args.input_file

    # Set up logging for the application
    logging.basicConfig(
        filename=f"{input_toml['i/o']['output_root']}.log", 
        filemode='w+', 
        format='%(asctime)s %(message)s', 
        datefmt='%m/%d/%Y %I:%M:%S %p', 
        level=logging.DEBUG
    )

    # Start Dask cluster to distribute the computation
    dask_cluster = LocalCluster(silence_logs=logging.ERROR)
    
    # Start the processing pipeline
    _mppost_start(input_toml, dask_cluster.get_client())

def _mppost_start(info, client):
    """Reads detector data and runs the specified processing modules."""
    run_start_time = time.time()  # Record start time for processing
    logging.info("Beginning pyMPPost run...")

    # Process detector data and material mappings
    detect_map, cell_to_mats = _detector_data(info)
    
    # Read Polimi data into a Dask DataFrame
    plm_ddf = _read_polimi(info, detect_map, cell_to_mats, client)
    
    # Dictionary to store results
    results = {}

    # Run Pulse Height Module if enabled
    if info["pulse_height"]["module_on"]:
        PH_df, results["pulse_height"] = pulse_height(plm_ddf, 
                                                      client,
                                                      info["mats"],
                                                      (info["pulse_height"]["threshold"]["lower"],
                                                       info["pulse_height"]["threshold"]["upper"]),
                                                      info["pulse_height"]["time_res_on"],
                                                      info["pulse_height"]["energy_res_on"],
                                                      info["seed"],
                                                      info["pulse_height"]["pulse_tol"]
                                                    )
        
        # Pulse Height Module Outputs
        # All Pulses File
        if info["pulse_height"]["all_pulses"] == "tsv":
            PH_df.to_csv(f"{info['i/o']['output_root']}_All_Pulses", header=info['i/o']['output_headers'], sep="\t")
        elif info["pulse_height"]["all_pulses"] == "parquet":
            PH_df.to_parquet(f"{info['i/o']['output_root']}_All_Pulses")
        
        # Pulse Height Histogram 
        total, edges = np.histogram(a=PH_df["light"], bins=info["pulse_height"]["hist_bins"])
        neutrons, __ = np.histogram(a=PH_df[PH_df.particle_type == 1]["light"], bins=edges)
        photons, __ = np.histogram(a=PH_df[PH_df.particle_type == 2]["light"], bins=edges)
        np.savetxt(fname=f"{info['i/o']['output_root']}_Pulse_Hist", X=np.column_stack((edges[:-1],total,neutrons,photons)))
        
    # Run Cross Correlation Module if enabled
    if info["cross_correlation"]["module_on"]:
        cc_results = cross_correlation(PH_df, 
                                       info["cross_correlation"]["start_detectors"]
                                    )
        # Cross Correlation Outputs
        for start_detector in cc_results:
            (time_diff, labels) = cc_results[start_detector]
            
            # All Cross Correlation Files
            if info["cross correlation"]["all_cc"] == "tsv":
                header = "time_diff\tlabel"
                np.savetxt(fname=f"{info['i/o']['output_root']}_detector_{start_detector}_All_CC", X=np.column_stack((time_diff,labels)), delimiter="\t", header=header)
            
            
            # Cross Correlation Histograms
            total, edges = np.histogram(a=time_diff, bins=info["cross correlation"]["hist_bins"])
            nn, __ = np.histogram(a=time_diff[labels == "nn"], bins=edges)
            gn, __ = np.histogram(a=time_diff[labels == "gn"], bins=edges)
            ng, __ = np.histogram(a=time_diff[labels == "nn"], bins=edges)
            gg, __ = np.histogram(a=time_diff[labels == "gg"], bins=edges)
            header = "time_diff\ttotal\tnn\tgn\tng\tgg"
            np.savetxt(fname=f"{info['i/o']['output_root']}_detector_{start_detector}_CC_Hist", X=np.column_stack((edges[:-1],total, nn, gn, ng, gg)), delimiter="\t", header=header)
        
    
    # Run Multiplicity Module if enabled
    if info["multiplicity"]["module_on"]:
        results["multiplicity"] = multiplicity(PH_df, 
                                               info["multiplicity"]["window_width"],
                                               info["multiplicity"]["mult_tol"]
                                            )
    
    # Generate a summary of the results
    _gen_summary(plm_ddf, info, client, results, run_start_time)

def _detector_data(info):
    """Processes the detector data and material calibration information."""
    cells_to_mats = {}
    detect_map = {}

    # Map cells to their corresponding materials
    for material, cells in zip(info["detectors"]["detector_mats"], info["detectors"]["detector_cells"]):
        cells_to_mats[cells[0]] = material
        if len(cells) > 1:
            for cell in cells[1:]:
                detect_map[cell] = cells[0]
                
    mats = []
    # Load material calibration data from files
    for mat_path in info["detectors"]["material_list"]:
        with open(mat_path) as mat_toml_file:
            mat = toml.load(mat_toml_file)
        mats.append(mat)
    info["mats"] = mats
    
    # Process Birks calibration for materials with type 1
    for mat in mats:
        if mat["mat_type"] == 1:
            _process_birks_calibration(mat)

    # Map detectors to materials
    detectors = {cell: mats[cells_to_mats[cell]] for cell in cells_to_mats}
    print(cells_to_mats)
    return detect_map, cells_to_mats

def _process_birks_calibration(mat):
    """Process Birks calibration for a given material."""
    mat_birks = mat["calibration"].pop("birks")
    with open(mat_birks["stopping_power"]) as dEdx_file:
        lines = dEdx_file.readlines()
    
    energy = np.zeros(len(lines))
    dEdx = np.zeros(len(lines))
    
    # Parse stopping power data
    for i, line in enumerate(lines):
        line = line.split()
        energy[i] = float(line[0])
        dEdx[i] = float(line[2] if os.path.basename(mat_birks["stopping_power"]) == "stilbene_dEdx.txt" else line[1])
    
    # Insert initial values
    energy = np.insert(energy, 0, 0.0)
    dEdx = np.insert(dEdx, 0, 0.0)
    
    # Calculate light output using Birks' law
    intergrand = mat_birks["S"] / (1 + mat_birks["kB"] * dEdx)
    birks_light = np.cumsum(intergrand * np.diff(energy, append=0))
    
    mat["calibration"]["birks_energy"] = energy
    mat["calibration"]["birks_light"] = birks_light

def _read_polimi(info, detect_map, cells_to_mats, client):
    """Reads Polimi data into a Dask DataFrame."""
    logging.info(f"Reading in MCNP-Polimi file: {info['i/o']['polimi_det_in']}")
    
    # Define the data types for each column in the Polimi file
    polimi_collision_file_dtypes = {
        "history": np.int64,
        "particle_num": np.int64,
        "particle_type": np.int64,
        "interaction_type": np.int64,
        "target_nucleus": np.int64,
        "cell": np.int64,
        "energy_deposited": np.float64,
        "time": np.float64,
        "x-pos": np.float64,
        "y-pos": np.float64,
        "z-pos": np.float64,
        "weight": np.float64,
        "generation_num": np.int64,
        "num_scatters": np.int64,
        "code": np.int64,
        "prior_energy": np.float64
    }
    
    # Read the CSV file into a Dask DataFrame
    plm_ddf = dd.read_csv(f"{info['i/o']['polimi_det_in']}", header=None, skipinitialspace=True, sep="\s+",
                          names=["history", "particle_num", "particle_type", "interaction_type", "target_nucleus", "cell", 
                                 "energy_deposited", "time", "x-pos", "y-pos", "z-pos", "weight", "generation_num",
                                 "num_scatters", "code", "prior_energy"], dtype=polimi_collision_file_dtypes)
    plm_ddf = plm_ddf.set_index("history", sorted=True)
    
    # Map cells to detector materials
    if detect_map:
        plm_ddf["cell"] = plm_ddf["cell"].replace(detect_map)
    plm_ddf["mat_num"] = plm_ddf["cell"].replace(cells_to_mats)
    print(plm_ddf["mat_num"])
    
    # Sort data by history, cell, and time
    plm_ddf = plm_ddf.map_partitions(lambda df: df.sort_values(by=["history", "cell", "time"]), meta=plm_ddf._meta)
    
    # Persist the DataFrame in Dask cluster memory for optimized access
    return client.persist(plm_ddf)

def _gen_summary(plm_ddf, info, client, results, start_time):
    """Generates a summary of the processing results."""
    # Open the output summary file
    with open(f"{info['i/o']['output_root']}.txt", mode="w") as sum_of:
        sum_of.write("Post Processor Output File Summary\n")
        date_and_time = datetime.datetime.now()
        
        # Write basic information to summary file
        sum_of.write(f"Title: {info['title']}\n")
        sum_of.write(f"Input File: {info['input_file']}\n")
        sum_of.write(f"User: {info['username']}\n")
        sum_of.write(f"Processed: {date_and_time}\n\n")
        
        # MCNP-PoliMi File Characteristics
        sum_of.write("MCNP-PoliMi File Characteristics\n")
        sum_of.write("--------------------------------\n")
        sum_of.write(f"Number of lines: {len(plm_ddf)}\n")
        sum_of.write(f"Number of histories: {client.compute(plm_ddf.index.nunique()).result()}\n\n")
        
        # Pulse Height Module Results
        if info["pulse_height"]["module_on"]:
            total_num_pulses, neutron_num_pulses = results["pulse_height"]
            sum_of.write(f"Pulse Height Analysis\n")
            sum_of.write(f"---------------------\n")
            sum_of.write(f"Total number of pulses above threshold: {total_num_pulses}\n")
            sum_of.write(f"Total number of neutron pulses above threshold: {neutron_num_pulses}\n")
            sum_of.write(f"Total number of photon pulses above threshold: {total_num_pulses - neutron_num_pulses}\n\n")
            
        # Cross Correlation Module Results
        # if info["cross_correlation"]["module_on"]:
        #     counts, total_counts = results["multiplicity"]
        #     sum_of.write(f"Multiplicity Counts\n")
        #     sum_of.write(f"-------------------\n")
        #     sum_of.write(f"Total number of windows: {total_counts}\n")
        #     sum_of.write(f"{counts.to_string(header=False)}\n\n")
        
        # Multiplicity Module Results
        if info["multiplicity"]["module_on"]:
            counts, total_counts = results["multiplicity"]
            sum_of.write(f"Multiplicity Counts\n")
            sum_of.write(f"-------------------\n")
            sum_of.write(f"Total number of windows: {total_counts}\n")
            sum_of.write(f"{counts.to_string(header=False)}\n\n")
        
        # Runtime Information
        sum_of.write(f"Runtime\n")    
        sum_of.write(f"-------\n")  
        sum_of.write(f"This run took {time.time() - start_time} seconds")

if __name__ == "__main__":
    main()
