import operator as op
from pathlib import Path
import pandas as pd

from cosmotech.coal.utils.configuration import Configuration
from cosmotech.coal.utils.logger import get_logger
from cosmotech.coal.utils.input_collector import ENVIRONMENT_INPUT_COLLECTOR as InputCollector

CSM_CONFIG = Configuration()
LOGGER = get_logger("CALCULATOR")

RUNNER_ID = CSM_CONFIG.cosmotech.runner_id
OUTPUT_PATH = CSM_CONFIG.cosmotech.output_absolute_path
RESULT_OUTPUT_PATH = Path(OUTPUT_PATH) / "calculator_results.csv"

OPERATORS = {
    "+": op.add,
    "-": op.sub,
    "*": op.mul,
    "/": op.truediv,
}


def main():
    LOGGER.info(f"Starting calculator run with runner ID: {RUNNER_ID}")

    raw_a = InputCollector.fetch("a_value")
    raw_b = InputCollector.fetch("b_value")
    operator_str = InputCollector.fetch("operator")

    if not raw_a or not raw_a.strip():
        raise ValueError("Parameter 'a_value' is missing or empty")
    if not raw_b or not raw_b.strip():
        raise ValueError("Parameter 'b_value' is missing or empty")
    if not operator_str or not operator_str.strip():
        raise ValueError("Parameter 'operator' is missing or empty")
    if operator_str not in OPERATORS:
        raise ValueError(f"Unsupported operator: {operator_str}. Supported: {list(OPERATORS.keys())}")

    a_value = float(raw_a)
    b_value = float(raw_b)
    result = OPERATORS[operator_str](a_value, b_value)
    results_df = pd.DataFrame([[a_value, b_value, operator_str, result]], columns=["a_values", "b_values", "operator", "result"])
    results_df.to_csv(RESULT_OUTPUT_PATH, index=False)

    LOGGER.info("Calculator run completed successfully.")

if __name__ == "__main__":
    main()
