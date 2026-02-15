"""
H12: Capacity Retention Degrades Below 80% After 500 Cycles

Hypothesis: Battery capacity retention falls below 80% after 500 cycles.

NOTE: This hypothesis is NOT VERIFIABLE with the current dataset (no capacity data).
"""

import os
import sys
import json
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

HYPOTHESIS_ID = "H12"
HYPOTHESIS_NAME = "Capacity_Retention"
HYPOTHESIS_TEXT = """
Capacity retention degrades below 80% after 500 charge-discharge cycles.

This is a standard battery degradation metric where the battery is considered
to have reached end-of-life when capacity drops below 80% of initial capacity.

NOTE: This hypothesis requires capacity measurements (mAh or Ah) across 500+ cycles,
which is not available in the current dataset. The dataset contains only Raman
spectroscopy data without direct capacity measurements.
"""


class BatteryDataLoader:
    """Custom data loader for battery experiment data."""

    def __init__(self, data_folder: str):
        self.data_path = data_folder
        self.table_dict = {}
        self._load_battery_data()
        self.data_desc = self._generate_data_description()

    def _load_battery_data(self):
        raman_path = os.path.join(self.data_path, "raman_peaks_decomposed.csv")
        self.table_dict["df_raman_peaks"] = pd.read_csv(raman_path)
        voltage_path = os.path.join(self.data_path, "voltage_profile_detailed.csv")
        if os.path.exists(voltage_path):
            self.table_dict["df_voltage_profile"] = pd.read_csv(voltage_path)

    def _generate_data_description(self) -> str:
        return """
Battery Operando Raman Spectroscopy Data:
- Material: Li1.13Ni0.3Mn0.57O2 (Li-rich layered oxide)
- 900 spatial pixels (30x30 grid), 114 time steps
- Voltage range: 3.05V to 4.68V (single charge cycle)
- Key columns: Raman peak parameters only (no capacity data)
- NOTE: No capacity measurements (mAh/Ah), no current data, no multi-cycle data
"""


def run_hypothesis_test():
    """Run VOLTA hypothesis test for H12 using GPT-4o."""

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set!")
        print("Set it with: export OPENAI_API_KEY='your-key'")
        return None

    from volta.agent import SequentialFalsificationTest

    script_dir = os.path.dirname(os.path.abspath(__file__))
    volta_dir = os.path.dirname(script_dir)
    data_path = os.path.join(volta_dir, "Battery_Data")
    output_dir = os.path.join(script_dir, "results", HYPOTHESIS_ID)
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print(f"Testing {HYPOTHESIS_ID}: {HYPOTHESIS_NAME} with GPT-4o")
    print("=" * 60)

    data_loader = BatteryDataLoader(data_path)

    agent = SequentialFalsificationTest(
        llm="gpt-4o",
        api_key=api_key
    )

    agent.configure(
        data=data_loader,
        alpha=0.1,
        aggregate_test='E-value',
        max_num_of_tests=5,
        max_retry=3,
        time_limit=5,
        relevance_checker=True,
        use_react_agent=True
    )

    start_time = time.time()
    log, last_message, parsed_result = agent.go(HYPOTHESIS_TEXT)
    elapsed_time = time.time() - start_time

    result = {
        "hypothesis_id": HYPOTHESIS_ID,
        "hypothesis_name": HYPOTHESIS_NAME,
        "hypothesis_text": HYPOTHESIS_TEXT,
        "model": "gpt-4o",
        "log": log,
        "last_message": last_message,
        "parsed_result": parsed_result,
        "elapsed_time_seconds": elapsed_time,
        "timestamp": datetime.now().isoformat()
    }

    log_file = os.path.join(output_dir, "log.json")
    with open(log_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)

    summary_file = os.path.join(output_dir, "summary.md")
    with open(summary_file, 'w') as f:
        f.write(f"# {HYPOTHESIS_ID}: {HYPOTHESIS_NAME}\n\n")
        f.write(f"**Model**: GPT-4o\n\n")
        f.write(f"## Hypothesis\n{HYPOTHESIS_TEXT}\n\n")
        f.write(f"## Result\n")
        f.write(f"- **Conclusion**: {parsed_result.get('conclusion', 'N/A')}\n")
        f.write(f"- **Elapsed Time**: {elapsed_time:.1f} seconds\n\n")
        f.write(f"## Rationale\n{parsed_result.get('rationale', 'N/A')}\n")

    print(f"\nConclusion: {parsed_result.get('conclusion', 'N/A')}")
    print(f"Elapsed time: {elapsed_time:.1f} seconds")
    print(f"Results saved to: {output_dir}")

    return result


if __name__ == "__main__":
    run_hypothesis_test()
