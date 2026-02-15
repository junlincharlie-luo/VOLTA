"""
H16: CEI_Steady_State
Tests using Gemini 2.5 Pro
"""

import os
import sys
import json
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pandas as pd

HYPOTHESIS = """The cathode-electrolyte interface (CEI) layer thickness stabilizes after approximately
50 cycles, as indicated by saturation of D-band intensity changes."""

class BatteryDataLoader:
    def __init__(self, data_folder: str):
        self.data_path = data_folder
        self.table_dict = {}
        self._load_battery_data()
        self.data_desc = self._generate_data_description()

    def _load_battery_data(self):
        raman_path = os.path.join(self.data_path, "raman_peaks_decomposed.csv")
        if os.path.exists(raman_path):
            self.table_dict["df_raman_peaks"] = pd.read_csv(raman_path)
        voltage_path = os.path.join(self.data_path, "voltage_profile_detailed.csv")
        if os.path.exists(voltage_path):
            self.table_dict["df_voltage_profile"] = pd.read_csv(voltage_path)

    def _generate_data_description(self) -> str:
        desc = """
=== Battery Experiment Data Description ===
Material: Li1.13Ni0.3Mn0.57O2 | Data: 900 pixels (30x30), 114 time steps | Voltage: 3.05V-4.68V
"""
        for name, df in self.table_dict.items():
            if df is not None:
                desc += f"**{name}**: Shape {df.shape}, Columns: {df.columns.tolist()}\n"
        return desc

def run_test():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not set")
        return None

    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(os.path.dirname(os.path.dirname(script_dir)), "Battery_Data")
    results_dir = os.path.join(script_dir, "results")
    os.makedirs(results_dir, exist_ok=True)

    try:
        from volta.agent import SequentialFalsificationTest
        data_loader = BatteryDataLoader(data_path)
        agent = SequentialFalsificationTest(llm="gemini-2.5-pro", api_key=api_key)
        agent.configure(data=data_loader, alpha=0.1, aggregate_test='E-value', max_num_of_tests=5, max_retry=3, time_limit=5, relevance_checker=True, use_react_agent=True)

        start_time = time.time()
        log, last_message, parsed_result = agent.go(HYPOTHESIS)
        elapsed_time = time.time() - start_time

        result = {"hypothesis_id": "H16", "hypothesis_name": "CEI_Steady_State", "parsed_result": parsed_result, "elapsed_time_seconds": elapsed_time, "timestamp": datetime.now().isoformat()}
        with open(os.path.join(results_dir, "log.json"), 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"H16 completed in {elapsed_time:.1f}s | Conclusion: {parsed_result.get('conclusion', 'N/A')}")
        return result
    except Exception as e:
        import traceback
        with open(os.path.join(results_dir, "error.txt"), 'w') as f:
            f.write(f"{str(e)}\n{traceback.format_exc()}")
        print(f"H16 FAILED: {str(e)}")
        return None

if __name__ == "__main__":
    run_test()
