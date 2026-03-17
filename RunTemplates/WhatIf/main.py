#!/usr/bin/env python3
# Copyright (c) Cosmo Tech corporation.
# This document and all information contained herein is the exclusive property -
# including all intellectual property rights pertaining thereto - of Cosmo Tech.
# Any use, reproduction, translation, broadcasting, transmission, distribution,
# etc., to any person is prohibited unless it has been previously and
# specifically authorized by written means by Cosmo Tech.
"""
Sample Run Template - Calculator

This script performs a simple calculation based on input parameters:
- a_value: First operand (integer, 0-100)
- b_value: Second operand (integer, 0-100)
- operator: Operation to perform (+, -, *, /)

The result is sent directly to Azure Data Explorer (ADX) for storage and analysis.

Author: endrit.ahmeti.ext@cosmotech.com
Version: 0.0.1
"""

import csv
import glob
import logging
import os
import shutil
import sys
import tempfile
import time
import zipfile
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

def perform_calculation(a_value, b_value, operator):
    """
    Perform the calculation based on the operator.

    Args:
        a_value (int): First operand
        b_value (int): Second operand
        operator (str): Operation to perform (+, -, *, /)

    Returns:
        float: Result of the calculation

    Raises:
        ValueError: If operator is invalid or division by zero
    """

    if operator == "+":
        result = a_value + b_value
    elif operator == "-":
        result = a_value - b_value
    elif operator == "*":
        result = a_value * b_value
    elif operator == "/":
        if b_value == 0:
            raise ValueError("Division by zero is not allowed")
        result = a_value / b_value
    else:
        raise ValueError(f"Invalid operator: {operator}")

    return result


def main():
    """
    Main execution function for the Sample Run Template.
    """

    try:
        # Get environment variables
        simulation_id = os.environ.get("CSM_RUNNER_ID")
        parameters_path = os.environ.get("CSM_PARAMETERS_ABSOLUTE_PATH", "/mnt/parameters")
        output_path = os.environ.get("CSM_OUTPUT_ABSOLUTE_PATH")
        dataset_path = os.environ.get("CSM_DATASET_ABSOLUTE_PATH", "/mnt/scenariorun-data")


        # Navigate into the single subdirectory inside dataset_path, find the zip, extract CSVs to output_path
        sub_dir = os.path.join(dataset_path, os.listdir(dataset_path)[0])
        zip_path = os.path.join(sub_dir, os.listdir(sub_dir)[0])
        logging.info(f"Found zip file: {zip_path}")

        if output_path is None:
            raise ValueError("CSM_OUTPUT_ABSOLUTE_PATH environment variable not set")

        with tempfile.TemporaryDirectory() as tmp_dir:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(tmp_dir)
            for csv_file in glob.glob(os.path.join(tmp_dir, '**', '*.csv'), recursive=True):
                dest = os.path.join(output_path, os.path.basename(csv_file))
                shutil.move(csv_file, dest)
                logging.info(f"Moved {os.path.basename(csv_file)} -> {dest}")

        # if not simulation_id:
        #     raise ValueError("CSM_SIMULATION_ID environment variable not set")


        # # Read parameters
        # parameters = read_parameters_from_csv(parameters_path)

        # Extract calculator parameters
        a_value_str = '45'
        b_value_str = '15'
        operator = '+'

        if not a_value_str:
            raise ValueError("Parameter 'a_value' not found")
        if not b_value_str:
            raise ValueError("Parameter 'b_value' not found")
        if not operator:
            raise ValueError("Parameter 'operator' not found")

        # Convert to appropriate types
        a_value = int(a_value_str)
        b_value = int(b_value_str)


        # Perform calculation
        result = perform_calculation(a_value, b_value, operator)
        logging.info(f"Calculation result: {result}")
        pd.DataFrame({"simulation_id": [simulation_id], "a_value": [a_value], "b_value": [b_value], "operator": [operator], "result": [result]}).to_csv(os.path.join(output_path, "results.csv"), index=False)

        # display output path content for debugging
        logging.info(f"Output path content: {os.listdir(output_path)}")

        return 0

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return 1

if __name__ == "__main__":
    start_time = time.time()
    exit_code = main()
    execution_time = time.time() - start_time
    logging.info(f"Execution time: {execution_time:.2f} seconds")
    sys.exit(exit_code)