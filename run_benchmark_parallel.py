"""
Parallel Hypothesis Benchmark Testing with POPPER

Runs the first 10 verifiable hypotheses from hypothesis_benchmark.md in parallel,
saving logs to separate folders and generating a summary.
"""

import os
import sys
import json
import time
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Dict, List, Optional
import pandas as pd

# Add POPPER to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Define the 10 verifiable hypotheses
HYPOTHESES = {
    "H1": {
        "name": "A1g_Voltage_Correlation",
        "hypothesis": """The A1g peak center position (cm⁻¹) decreases (redshifts) with increasing voltage during charging,
reflecting delithiation-induced M-O bond weakening in Li-rich layered oxides due to oxygen redox participation
and structural distortion. Expected: Strong negative correlation (r ≈ -0.88), with A1g peak shifting ~22 cm⁻¹ lower during charging."""
    },
    "H2": {
        "name": "Spatial_Heterogeneity",
        "hypothesis": """The standard deviation of A1g_Center across the 900 spatial pixels increases as voltage increases,
indicating growing electrochemical heterogeneity during delithiation."""
    },
    "H3": {
        "name": "ID_IG_High_Voltage",
        "hypothesis": """The ID/IG ratio (carbon disorder indicator) decreases significantly when voltage exceeds 4.3V,
indicating enhanced graphitic ordering or preferential G-band enhancement due to electrochemical activation
of the carbon conductive network at high potentials. Expected: Significant decrease (~10%) in ID/IG at V > 4.3V."""
    },
    "H4": {
        "name": "Eg_Amplitude_Increase",
        "hypothesis": """The Eg peak amplitude (related to M-O bending in layered structure) increases during charging,
reflecting enhanced Raman scattering from M-O bending modes as lithium extraction modifies the electronic structure.
Expected: Positive correlation (r ≈ +0.28) with ~30% amplitude increase during charging."""
    },
    "H5": {
        "name": "Spatial_Decoupling",
        "hypothesis": """The A1g peak position (cathode structural indicator) and ID/IG ratio (carbon disorder indicator)
show weak or no spatial correlation, indicating that local cathode delithiation and carbon network properties
evolve independently across the electrode surface. Expected: Weak mean correlation (|r| < 0.05)."""
    },
    "H6": {
        "name": "Edge_Center_Uniformity",
        "hypothesis": """Pixels at the edges of the 30×30 mapping region exhibit statistically similar A1g peak evolution
compared to center pixels, indicating homogeneous electrochemical accessibility across the mapped electrode area
at the 30 μm scale. Expected: No significant difference in A1g shift between edge and center pixels (p > 0.05)."""
    },
    "H7": {
        "name": "A1g_Width_Decrease",
        "hypothesis": """The A1g peak width (A1g_Sigma) decreases with voltage, indicating peak sharpening as lithium
extraction creates a more uniform local bonding environment and reduces the distribution of M-O bond lengths.
Expected: Strong negative correlation (r ≈ -0.63), with ~33% width decrease during charging."""
    },
    "H8": {
        "name": "Gband_Redshift",
        "hypothesis": """The G-band center position shifts to lower wavenumbers (redshifts) with increasing voltage,
reflecting charge transfer interactions between the carbon conductive network and the delithiating cathode particles,
or electrochemical doping effects on the carbon. Expected: Strong negative correlation (r ≈ -0.74)."""
    },
    "H9": {
        "name": "Dband_Time_Delay",
        "hypothesis": """Changes in D-band amplitude (D_Amp) lag behind voltage changes by at least one measurement
interval (15 min), suggesting SEI formation is a kinetically slow process."""
    },
    "H10": {
        "name": "Spatial_Autocorrelation",
        "hypothesis": """The A1g_Center values of spatially adjacent pixels are more correlated than distant pixels,
indicating local electrochemical domains larger than 1 μm."""
    }
}


class BatteryDataLoader:
    """Custom data loader for battery experiment data."""

    def __init__(self, data_folder: str, random_seed: int = 42):
        self.data_path = data_folder
        self.random_seed = random_seed
        self.table_dict = {}
        self._load_battery_data()
        self.data_desc = self._generate_data_description()

    def _load_battery_data(self):
        raman_path = os.path.join(self.data_path, "raman_peaks_decomposed.csv")
        if os.path.exists(raman_path):
            self.table_dict["df_raman_peaks"] = pd.read_csv(raman_path)
        else:
            raise FileNotFoundError(f"Raman peaks file not found: {raman_path}")

        voltage_path = os.path.join(self.data_path, "voltage_profile_detailed.csv")
        if os.path.exists(voltage_path):
            self.table_dict["df_voltage_profile"] = pd.read_csv(voltage_path)

    def _generate_data_description(self) -> str:
        desc = """
=== Battery Experiment Data Description ===

This dataset contains Operando Raman Spectroscopy data from Li-rich layered oxide cathode cycling.
Material: Li₁.₁₃Ni₀.₃Mn₀.₅₇O₂
Data: 900 spatial pixels (30×30 grid), 114 time steps (~28.5 hours)
Voltage range: 3.05V to 4.68V (single charge cycle)

"""
        for name, df in self.table_dict.items():
            if df is not None:
                desc += f"**{name}**: Shape {df.shape}, Columns: {df.columns.tolist()}\n"

        desc += """
Key columns in df_raman_peaks:
- A1g_Center: A₁g peak position (~590 cm⁻¹, M-O stretching, PRIMARY SOC INDICATOR)
- A1g_Sigma: A₁g peak width
- Eg_Center/Eg_Amp: Eg peak parameters (~475 cm⁻¹, M-O bending)
- D_Center/D_Amp: D-band parameters (~1350 cm⁻¹, disordered carbon)
- G_Center/G_Amp: G-band parameters (~1585 cm⁻¹, graphitic carbon)
- ID_IG_Ratio: D/G intensity ratio (carbon disorder indicator)
- X, Y: Spatial coordinates (30×30 μm grid)
- Voltage: Cell voltage (V vs Li/Li⁺)
- Time_Min: Time in minutes
"""
        return desc


def run_single_hypothesis(args) -> Dict:
    """Run a single hypothesis test. Called by process pool."""
    hypothesis_id, hypothesis_data, config = args

    # Set API key from environment
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {
            "hypothesis_id": hypothesis_id,
            "name": hypothesis_data["name"],
            "status": "FAILED",
            "error": "ANTHROPIC_API_KEY not set in environment",
            "log": None,
            "result": None
        }

    try:
        from popper.agent import SequentialFalsificationTest

        # Create output directory for this hypothesis
        output_dir = os.path.join(config["output_base"], f"{hypothesis_id}_{hypothesis_data['name']}")
        os.makedirs(output_dir, exist_ok=True)

        # Load data
        data_loader = BatteryDataLoader(config["data_path"])

        # Initialize agent
        agent = SequentialFalsificationTest(
            llm=config["llm"],
            api_key=api_key
        )

        agent.configure(
            data=data_loader,
            alpha=config["alpha"],
            aggregate_test='E-value',
            max_num_of_tests=config["max_tests"],
            max_retry=config["max_retry"],
            time_limit=config["time_limit"],
            relevance_checker=config["relevance_checker"],
            use_react_agent=config["use_react_agent"]
        )

        # Run the test
        start_time = time.time()
        log, last_message, parsed_result = agent.go(hypothesis_data["hypothesis"])
        elapsed_time = time.time() - start_time

        # Save log to file
        log_file = os.path.join(output_dir, "log.json")
        with open(log_file, 'w') as f:
            json.dump({
                "hypothesis_id": hypothesis_id,
                "hypothesis_name": hypothesis_data["name"],
                "hypothesis_text": hypothesis_data["hypothesis"],
                "log": log,
                "last_message": last_message,
                "parsed_result": parsed_result,
                "elapsed_time_seconds": elapsed_time,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2, default=str)

        # Save readable summary
        summary_file = os.path.join(output_dir, "summary.md")
        with open(summary_file, 'w') as f:
            f.write(f"# {hypothesis_id}: {hypothesis_data['name']}\n\n")
            f.write(f"## Hypothesis\n{hypothesis_data['hypothesis']}\n\n")
            f.write(f"## Result\n")
            f.write(f"- **Conclusion**: {parsed_result.get('conclusion', 'N/A')}\n")
            f.write(f"- **Elapsed Time**: {elapsed_time:.1f} seconds\n\n")
            f.write(f"## Rationale\n{parsed_result.get('rationale', 'N/A')}\n\n")
            f.write(f"## Full Result\n```json\n{json.dumps(parsed_result, indent=2, default=str)}\n```\n")

        return {
            "hypothesis_id": hypothesis_id,
            "name": hypothesis_data["name"],
            "status": "SUCCESS",
            "conclusion": parsed_result.get('conclusion', 'N/A'),
            "elapsed_time": elapsed_time,
            "output_dir": output_dir,
            "error": None
        }

    except Exception as e:
        import traceback
        error_msg = f"{str(e)}\n{traceback.format_exc()}"

        # Save error log
        output_dir = os.path.join(config["output_base"], f"{hypothesis_id}_{hypothesis_data['name']}")
        os.makedirs(output_dir, exist_ok=True)
        error_file = os.path.join(output_dir, "error.txt")
        with open(error_file, 'w') as f:
            f.write(error_msg)

        return {
            "hypothesis_id": hypothesis_id,
            "name": hypothesis_data["name"],
            "status": "FAILED",
            "error": error_msg,
            "output_dir": output_dir
        }


def run_parallel_benchmark(
    llm: str = "claude-sonnet-4-20250514",
    alpha: float = 0.1,
    max_tests: int = 5,
    max_retry: int = 3,
    time_limit: int = 5,
    max_workers: int = 5,
    relevance_checker: bool = True,
    use_react_agent: bool = True
) -> Dict:
    """Run all 10 hypotheses in parallel."""

    # Check API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set!")
        print("Please set it with: export ANTHROPIC_API_KEY='your-api-key'")
        return {"status": "FAILED", "error": "API key not set"}

    print("=" * 70)
    print("POPPER Parallel Hypothesis Benchmark")
    print("=" * 70)
    print(f"Model: {llm}")
    print(f"Alpha: {alpha}")
    print(f"Max tests per hypothesis: {max_tests}")
    print(f"Max parallel workers: {max_workers}")
    print(f"Total hypotheses: {len(HYPOTHESES)}")
    print("=" * 70)

    # Create output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_base = os.path.join(script_dir, "benchmark_results", timestamp)
    os.makedirs(output_base, exist_ok=True)

    data_path = os.path.join(script_dir, "Battery_Data")

    # Configuration for all workers
    config = {
        "llm": llm,
        "alpha": alpha,
        "max_tests": max_tests,
        "max_retry": max_retry,
        "time_limit": time_limit,
        "relevance_checker": relevance_checker,
        "use_react_agent": use_react_agent,
        "output_base": output_base,
        "data_path": data_path
    }

    # Prepare arguments for each hypothesis
    args_list = [
        (h_id, h_data, config)
        for h_id, h_data in HYPOTHESES.items()
    ]

    results = []
    start_time = time.time()

    print(f"\nStarting parallel execution with {max_workers} workers...")
    print(f"Output directory: {output_base}\n")

    # Run in parallel
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_hypothesis = {
            executor.submit(run_single_hypothesis, args): args[0]
            for args in args_list
        }

        for future in as_completed(future_to_hypothesis):
            hypothesis_id = future_to_hypothesis[future]
            try:
                result = future.result()
                results.append(result)
                status_icon = "✓" if result["status"] == "SUCCESS" else "✗"
                print(f"  [{status_icon}] {hypothesis_id}: {result.get('name', 'Unknown')} - {result['status']}")
                if result.get('conclusion'):
                    print(f"      Conclusion: {result['conclusion']}")
            except Exception as e:
                print(f"  [✗] {hypothesis_id}: Exception - {str(e)}")
                results.append({
                    "hypothesis_id": hypothesis_id,
                    "status": "EXCEPTION",
                    "error": str(e)
                })

    total_time = time.time() - start_time

    # Generate summary
    print("\n" + "=" * 70)
    print("BENCHMARK SUMMARY")
    print("=" * 70)

    successful = [r for r in results if r["status"] == "SUCCESS"]
    failed = [r for r in results if r["status"] != "SUCCESS"]

    print(f"Total time: {total_time:.1f} seconds")
    print(f"Successful: {len(successful)}/{len(results)}")
    print(f"Failed: {len(failed)}/{len(results)}")

    # Save summary
    summary = {
        "timestamp": timestamp,
        "config": {
            "llm": llm,
            "alpha": alpha,
            "max_tests": max_tests,
            "max_workers": max_workers
        },
        "total_time_seconds": total_time,
        "successful_count": len(successful),
        "failed_count": len(failed),
        "results": results
    }

    summary_file = os.path.join(output_base, "benchmark_summary.json")
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2, default=str)

    # Generate markdown summary
    md_summary_file = os.path.join(output_base, "SUMMARY.md")
    with open(md_summary_file, 'w') as f:
        f.write("# POPPER Benchmark Results\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Model**: {llm}\n")
        f.write(f"**Total Time**: {total_time:.1f} seconds\n\n")

        f.write("## Results Summary\n\n")
        f.write("| ID | Hypothesis | Status | Conclusion | Time (s) |\n")
        f.write("|-----|-----------|--------|------------|----------|\n")

        for r in sorted(results, key=lambda x: x["hypothesis_id"]):
            status = "✓" if r["status"] == "SUCCESS" else "✗"
            conclusion = r.get("conclusion", r.get("error", "N/A"))[:50]
            elapsed = f"{r.get('elapsed_time', 0):.1f}" if r.get('elapsed_time') else "N/A"
            f.write(f"| {r['hypothesis_id']} | {r.get('name', 'Unknown')} | {status} | {conclusion} | {elapsed} |\n")

        f.write(f"\n## Statistics\n")
        f.write(f"- **Successful**: {len(successful)}/{len(results)}\n")
        f.write(f"- **Failed**: {len(failed)}/{len(results)}\n")

        if failed:
            f.write("\n## Failures\n")
            for r in failed:
                f.write(f"\n### {r['hypothesis_id']}: {r.get('name', 'Unknown')}\n")
                f.write(f"```\n{r.get('error', 'Unknown error')[:500]}\n```\n")

    print(f"\nResults saved to: {output_base}")
    print(f"Summary: {md_summary_file}")

    return summary


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run parallel hypothesis benchmark with POPPER")
    parser.add_argument("--llm", type=str, default="claude-sonnet-4-20250514",
                        help="LLM model to use (default: claude-sonnet-4-20250514)")
    parser.add_argument("--alpha", type=float, default=0.1,
                        help="Significance level (default: 0.1)")
    parser.add_argument("--max-tests", type=int, default=5,
                        help="Maximum falsification tests per hypothesis (default: 5)")
    parser.add_argument("--max-workers", type=int, default=5,
                        help="Maximum parallel workers (default: 5)")
    parser.add_argument("--time-limit", type=int, default=5,
                        help="Time limit per test in minutes (default: 5)")

    args = parser.parse_args()

    results = run_parallel_benchmark(
        llm=args.llm,
        alpha=args.alpha,
        max_tests=args.max_tests,
        max_workers=args.max_workers,
        time_limit=args.time_limit
    )
