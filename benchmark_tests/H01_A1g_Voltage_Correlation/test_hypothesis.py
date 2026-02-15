"""
H1: A1g Peak Center Correlates Negatively with Voltage

Hypothesis: The A1g peak center position (cm^-1) decreases (redshifts) with increasing
voltage during charging, reflecting delithiation-induced M-O bond weakening.
Expected: Strong negative correlation (r ~ -0.88), ~22 cm^-1 shift.
"""

import os
import sys
import json
import time
from datetime import datetime

# Add POPPER to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd

HYPOTHESIS_ID = "H01"
HYPOTHESIS_NAME = "A1g_Voltage_Correlation"
HYPOTHESIS_TEXT = """
The A1g peak center position (cm^-1) decreases (redshifts) with increasing voltage during charging,
reflecting delithiation-induced M-O bond weakening in Li-rich layered oxides due to oxygen redox
participation and structural distortion.

Expected Result: Strong negative correlation (r ~ -0.88), with A1g peak shifting ~22 cm^-1 lower
during charging from 3.05V to 4.68V.
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
- Key columns: A1g_Center (peak position), Voltage, Time_Min, X, Y
- A1g_Center: Primary state-of-charge indicator (~590 cm^-1)
"""


def run_hypothesis_test():
    """Run POPPER hypothesis test for H1."""

    # Get API key from environment
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set!")
        print("Set it with: export ANTHROPIC_API_KEY='your-key'")
        return None

    from popper.agent import SequentialFalsificationTest

    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    popper_dir = os.path.dirname(os.path.dirname(script_dir))
    data_path = os.path.join(popper_dir, "Battery_Data")
    output_dir = os.path.join(script_dir, "results")
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print(f"Testing {HYPOTHESIS_ID}: {HYPOTHESIS_NAME}")
    print("=" * 60)

    # Load data
    data_loader = BatteryDataLoader(data_path)

    # Initialize agent
    agent = SequentialFalsificationTest(
        llm="claude-sonnet-4-20250514",
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

    # Run test
    start_time = time.time()
    log, last_message, parsed_result = agent.go(HYPOTHESIS_TEXT)
    elapsed_time = time.time() - start_time

    # Save results
    result = {
        "hypothesis_id": HYPOTHESIS_ID,
        "hypothesis_name": HYPOTHESIS_NAME,
        "hypothesis_text": HYPOTHESIS_TEXT,
        "log": log,
        "last_message": last_message,
        "parsed_result": parsed_result,
        "elapsed_time_seconds": elapsed_time,
        "timestamp": datetime.now().isoformat()
    }

    log_file = os.path.join(output_dir, "log.json")
    with open(log_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)

    # Save summary
    summary_file = os.path.join(output_dir, "summary.md")
    with open(summary_file, 'w') as f:
        f.write(f"# {HYPOTHESIS_ID}: {HYPOTHESIS_NAME}\n\n")
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
