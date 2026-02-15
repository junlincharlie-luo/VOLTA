"""
H8: G-band Position Shows Voltage-Dependent Redshift During Charging

Hypothesis: The G-band center position shifts to lower wavenumbers (redshifts) with
increasing voltage, reflecting charge transfer with delithiating cathode.
Expected: Strong negative correlation (r ~ -0.74), ~3.5 cm^-1 per volt.
"""

import os
import sys
import json
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pandas as pd

HYPOTHESIS_ID = "H08"
HYPOTHESIS_NAME = "Gband_Redshift"
HYPOTHESIS_TEXT = """
The G-band center position shifts to lower wavenumbers (redshifts) with increasing voltage,
reflecting charge transfer interactions between the carbon conductive network and the
delithiating cathode particles, or electrochemical doping effects on the carbon.

Expected Result: Strong negative correlation (r ~ -0.74), with G-band shifting ~3.5 cm^-1 per volt.

To test: Calculate G_Center shift range and correlation with voltage.
"""


class BatteryDataLoader:
    def __init__(self, data_folder: str):
        self.data_path = data_folder
        self.table_dict = {}
        self._load_battery_data()
        self.data_desc = "Battery Raman: G_Center (~1585 cm^-1 graphitic carbon) available"

    def _load_battery_data(self):
        self.table_dict["df_raman_peaks"] = pd.read_csv(
            os.path.join(self.data_path, "raman_peaks_decomposed.csv"))
        voltage_path = os.path.join(self.data_path, "voltage_profile_detailed.csv")
        if os.path.exists(voltage_path):
            self.table_dict["df_voltage_profile"] = pd.read_csv(voltage_path)


def run_hypothesis_test():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set!")
        return None

    from popper.agent import SequentialFalsificationTest

    script_dir = os.path.dirname(os.path.abspath(__file__))
    popper_dir = os.path.dirname(os.path.dirname(script_dir))
    data_path = os.path.join(popper_dir, "Battery_Data")
    output_dir = os.path.join(script_dir, "results")
    os.makedirs(output_dir, exist_ok=True)

    print(f"Testing {HYPOTHESIS_ID}: {HYPOTHESIS_NAME}")

    data_loader = BatteryDataLoader(data_path)
    agent = SequentialFalsificationTest(llm="claude-sonnet-4-20250514", api_key=api_key)
    agent.configure(data=data_loader, alpha=0.1, aggregate_test='E-value',
                   max_num_of_tests=5, max_retry=3, time_limit=5,
                   relevance_checker=True, use_react_agent=True)

    start_time = time.time()
    log, last_message, parsed_result = agent.go(HYPOTHESIS_TEXT)
    elapsed_time = time.time() - start_time

    result = {
        "hypothesis_id": HYPOTHESIS_ID, "hypothesis_name": HYPOTHESIS_NAME,
        "hypothesis_text": HYPOTHESIS_TEXT, "log": log, "last_message": last_message,
        "parsed_result": parsed_result, "elapsed_time_seconds": elapsed_time,
        "timestamp": datetime.now().isoformat()
    }

    with open(os.path.join(output_dir, "log.json"), 'w') as f:
        json.dump(result, f, indent=2, default=str)

    with open(os.path.join(output_dir, "summary.md"), 'w') as f:
        f.write(f"# {HYPOTHESIS_ID}: {HYPOTHESIS_NAME}\n\n")
        f.write(f"## Hypothesis\n{HYPOTHESIS_TEXT}\n\n")
        f.write(f"## Result\n- **Conclusion**: {parsed_result.get('conclusion', 'N/A')}\n")
        f.write(f"- **Elapsed Time**: {elapsed_time:.1f}s\n\n")
        f.write(f"## Rationale\n{parsed_result.get('rationale', 'N/A')}\n")

    print(f"Conclusion: {parsed_result.get('conclusion', 'N/A')}")
    return result


if __name__ == "__main__":
    run_hypothesis_test()
