"""
H12: Capacity Retention Degrades Below 80% After 500 Cycles (NON-VERIFIABLE)

Hypothesis: The battery exhibits capacity retention below 80% of initial capacity after 500 cycles.
Why NOT Verifiable: Dataset contains only ONE partial charge cycle. No capacity or long-term data.
"""

import os
import sys
import json
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd


HYPOTHESIS_ID = "H12"
HYPOTHESIS_NAME = "Capacity_Retention_500_Cycles"
HYPOTHESIS_TEXT = """
The battery exhibits capacity retention below 80% of initial capacity after 500 electrochemical
cycles, indicating significant degradation of the Li-rich layered oxide cathode.

Note: This hypothesis may NOT be verifiable with the current dataset which contains only ONE
partial charge cycle. No capacity measurements, no discharge data, and no long-term cycling data
are available.
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
- Voltage range: 3.05V to 4.68V (single charge cycle ONLY)
- Key columns: Voltage, Time_Min, X, Y
- NOTE: No capacity measurements, no discharge data, only single charge cycle
"""





def run_hypothesis_test():
    """Run POPPER hypothesis test for H12 using Gemini 2.0 Flash."""

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not set!")
        print("Set it with: export GOOGLE_API_KEY='your-key'")
        return None

    
    from popper.agent import SequentialFalsificationTest

    script_dir = os.path.dirname(os.path.abspath(__file__))
    popper_dir = os.path.dirname(script_dir)
    data_path = os.path.join(popper_dir, "Battery_Data")
    output_dir = os.path.join(script_dir, "results", HYPOTHESIS_ID)
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print(f"Testing {HYPOTHESIS_ID}: {HYPOTHESIS_NAME} with Gemini 2.0 Flash")
    print("=" * 60)

    data_loader = BatteryDataLoader(data_path)

    agent = SequentialFalsificationTest(
        llm="gemini-2.0-flash",
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
    try:
        log, last_message, parsed_result = agent.go(HYPOTHESIS_TEXT)
    except Exception as e:
        elapsed_time = time.time() - start_time
        error_result = {
            "hypothesis_id": HYPOTHESIS_ID,
            "hypothesis_name": HYPOTHESIS_NAME,
            "error": str(e),
            "elapsed_time_seconds": elapsed_time,
            "timestamp": datetime.now().isoformat()
        }
        error_file = os.path.join(output_dir, "error.txt")
        with open(error_file, 'w') as f:
            f.write(f"Error: {str(e)}\n")
        print(f"ERROR: {e}")
        return error_result

    elapsed_time = time.time() - start_time

    result = {
        "hypothesis_id": HYPOTHESIS_ID,
        "hypothesis_name": HYPOTHESIS_NAME,
        "hypothesis_text": HYPOTHESIS_TEXT,
        "model": "gemini-2.0-flash",
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
        f.write(f"**Model**: Gemini 2.0 Flash\n\n")
        f.write(f"## Hypothesis\n{HYPOTHESIS_TEXT}\n\n")
        f.write(f"## Result\n")
        if isinstance(parsed_result, dict):
            f.write(f"- **Conclusion**: {parsed_result.get('conclusion', 'N/A')}\n")
        else:
            f.write(f"- **Conclusion**: {getattr(parsed_result, 'conclusion', 'N/A')}\n")
        f.write(f"- **Elapsed Time**: {elapsed_time:.1f} seconds\n\n")
        if isinstance(parsed_result, dict):
            f.write(f"## Rationale\n{parsed_result.get('rationale', 'N/A')}\n")
        else:
            f.write(f"## Rationale\n{getattr(parsed_result, 'rationale', 'N/A')}\n")

    if isinstance(parsed_result, dict):
        print(f"\nConclusion: {parsed_result.get('conclusion', 'N/A')}")
    else:
        print(f"\nConclusion: {getattr(parsed_result, 'conclusion', 'N/A')}")
    print(f"Elapsed time: {elapsed_time:.1f} seconds")
    print(f"Results saved to: {output_dir}")

    return result


if __name__ == "__main__":
    run_hypothesis_test()
