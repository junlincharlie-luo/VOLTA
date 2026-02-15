"""
H17: Rate Capability (Non-Verifiable)

Hypothesis: At charging rates above 2C, the A1g peak shift becomes incomplete,
indicating rate-limited lithium extraction kinetics.

Note: This hypothesis is designed to be non-verifiable without rate-varied data.

Uses Claude Haiku via LangChain for VOLTA hypothesis testing.
"""

import os
import sys
import json
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

HYPOTHESIS_ID = "H17"
HYPOTHESIS_NAME = "Rate_Capability"
HYPOTHESIS_TEXT = """
At charging rates above 2C, the A1g peak shift becomes incomplete, indicating
rate-limited lithium extraction kinetics.

Note: This hypothesis requires data at different C-rates which may not be available.
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
- Key columns: A1g_Center, Voltage, Time_Min, X, Y
- Note: Data at single C-rate only, no rate variation data
"""


def run_hypothesis_test():
    """Run VOLTA hypothesis test for H17 using Claude Haiku via LangChain."""

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set!")
        print("Set it with: export ANTHROPIC_API_KEY='your-key'")
        return None

    from volta.agent import SequentialFalsificationTest

    script_dir = os.path.dirname(os.path.abspath(__file__))
    volta_dir = os.path.dirname(script_dir)
    data_path = os.path.join(volta_dir, "Battery_Data")
    output_dir = os.path.join(script_dir, "results", HYPOTHESIS_ID)
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print(f"Testing {HYPOTHESIS_ID}: {HYPOTHESIS_NAME} with Claude Haiku")
    print("=" * 60)

    data_loader = BatteryDataLoader(data_path)

    agent = SequentialFalsificationTest(
        llm="claude-3-5-haiku-20241022",
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
        "model": "claude-3-5-haiku-20241022",
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
        f.write(f"**Model**: Claude 3.5 Haiku (claude-3-5-haiku-20241022) via LangChain\n\n")
        f.write(f"**Note**: Non-verifiable hypothesis (requires multi-rate data)\n\n")
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
