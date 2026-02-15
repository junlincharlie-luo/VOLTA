"""
Run the 15 Failed Hypothesis Tests with Gemini 2.5 Pro
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

# The 15 tests that failed previously
FAILED_TESTS = [
    "H05_Spatial_Decoupling",
    "H07_A1g_Width",
    "H08_Gband_Redshift",
    "H09_Dband_Time_Delay",
    "H10_Spatial_Autocorrelation",
    "H11_Voltage_Fade",
    "H12_Capacity_Retention",
    "H13_Oxygen_Release",
    "H14_Temperature_Dependence",
    "H15_Cation_Mixing",
    "H16_CEI_Steady_State",
    "H17_Rate_Capability",
    "H18_Discharge_Reversibility",
    "H19_Electrolyte_Decomposition",
    "H20_Mn_Dissolution",
]


def run_single_test(test_dir: str) -> dict:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_path = os.path.join(script_dir, test_dir, "test_hypothesis.py")

    print(f"  Starting: {test_dir}")
    start_time = time.time()

    try:
        result = subprocess.run(
            [sys.executable, test_path],
            capture_output=True,
            text=True,
            timeout=900,
            env=os.environ.copy()
        )

        elapsed = time.time() - start_time

        result_file = os.path.join(script_dir, test_dir, "results", "log.json")
        if os.path.exists(result_file):
            with open(result_file, 'r') as f:
                test_result = json.load(f)
            conclusion = test_result.get("parsed_result", {}).get("conclusion", "N/A")
            status = "SUCCESS"
        else:
            conclusion = "No result file"
            status = "FAILED"

        return {
            "test_dir": test_dir,
            "status": status,
            "conclusion": conclusion,
            "elapsed_time": elapsed,
            "stdout": result.stdout[-1000:] if result.stdout else "",
            "stderr": result.stderr[-500:] if result.stderr else ""
        }

    except subprocess.TimeoutExpired:
        return {"test_dir": test_dir, "status": "TIMEOUT", "conclusion": "Timed out", "elapsed_time": 900}
    except Exception as e:
        return {"test_dir": test_dir, "status": "ERROR", "conclusion": str(e), "elapsed_time": time.time() - start_time}


def main():
    if not os.environ.get("GOOGLE_API_KEY"):
        print("ERROR: GOOGLE_API_KEY not set!")
        sys.exit(1)

    print("=" * 70)
    print("Re-running 15 Failed Hypothesis Tests with Gemini 2.5 Pro")
    print("=" * 70)

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Clear old error files
    for test_dir in FAILED_TESTS:
        error_file = os.path.join(script_dir, test_dir, "results", "error.txt")
        if os.path.exists(error_file):
            os.remove(error_file)

    start_time = time.time()
    results = []

    max_workers = 3
    print(f"Running {len(FAILED_TESTS)} tests with {max_workers} parallel workers\n")

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_test = {executor.submit(run_single_test, td): td for td in FAILED_TESTS}

        for future in as_completed(future_to_test):
            test_dir = future_to_test[future]
            try:
                result = future.result()
                results.append(result)
                icon = "✓" if result["status"] == "SUCCESS" else "✗"
                print(f"  [{icon}] {test_dir}: {result['status']} - {str(result.get('conclusion', 'N/A'))[:60]}")
            except Exception as e:
                print(f"  [!] {test_dir}: Exception - {str(e)}")
                results.append({"test_dir": test_dir, "status": "ERROR", "error": str(e)})

    total_time = time.time() - start_time

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    successful = sum(1 for r in results if r["status"] == "SUCCESS")
    print(f"Total time: {total_time:.1f}s")
    print(f"Successful: {successful}/{len(results)}")

    # Update summary
    summary_file = os.path.join(script_dir, "RERUN_SUMMARY.md")
    with open(summary_file, 'w') as f:
        f.write("# Gemini 2.5 Pro - Rerun of 15 Failed Tests\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Time**: {total_time:.1f}s\n\n")
        f.write("## Results\n\n")
        f.write("| ID | Hypothesis | Status | Conclusion | Time |\n")
        f.write("|---|-----------|--------|------------|------|\n")

        for r in sorted(results, key=lambda x: x["test_dir"]):
            icon = "✓" if r["status"] == "SUCCESS" else "✗"
            conclusion = str(r.get("conclusion", "N/A"))[:50]
            elapsed = f"{r.get('elapsed_time', 0):.0f}s"
            f.write(f"| {r['test_dir'][:3]} | {r['test_dir'][4:]} | {icon} | {conclusion} | {elapsed} |\n")

    print(f"\nSummary saved to: {summary_file}")


if __name__ == "__main__":
    main()
