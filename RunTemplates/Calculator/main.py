import operator as op
from pathlib import Path
import pandas as pd

from cosmotech.coal.utils.configuration import Configuration
from cosmotech.coal.utils.logger import get_logger
from cosmotech.coal.utils.input_collector import ENVIRONMENT_INPUT_COLLECTOR as InputCollector

OPERATORS = {
    "+": op.add,
    "-": op.sub,
    "*": op.mul,
    "/": op.truediv,
}

LOGGER = get_logger("CALCULATOR")
CSM_CONFIG = Configuration()

RUNNER_ID = CSM_CONFIG.cosmotech.runner_id
OUTPUT_PATH = CSM_CONFIG.cosmotech.output_absolute_path

OUTPUT_FILENAME = "calculator_results.csv"



def main():
    path_output = Path(OUTPUT_PATH) / OUTPUT_FILENAME

    raw_a = InputCollector.fetch("a_value")
    raw_b = InputCollector.fetch("b_value")
    if not raw_a or not raw_a.strip():
        raise ValueError("Parameter 'a_value' is missing or empty")
    if not raw_b or not raw_b.strip():
        raise ValueError("Parameter 'b_value' is missing or empty")
    a_value = float(raw_a)
    b_value = float(raw_b)
    operator_str = InputCollector.fetch("operator")
    if operator_str not in OPERATORS:
        raise ValueError(f"Unsupported operator: {operator_str}. Supported: {list(OPERATORS.keys())}")
    result = OPERATORS[operator_str](a_value, b_value)
    results_df = pd.DataFrame([[a_value, b_value, operator_str, result]], columns=["a_values", "b_values", "operator", "result"])
    results_df.to_csv(path_output, index=False)
    # Save results to output file
    LOGGER.info(f"Calculator run completed successfully with {len(results_df)} rows.")
    LOGGER.info(f"Output file path: {path_output}")

if __name__ == "__main__":
    main()
