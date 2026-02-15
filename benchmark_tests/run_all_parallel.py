"""
Run All 10 Hypothesis Tests in Parallel

This script runs all hypothesis tests concurrently and generates a combined summary.
Usage: python run_all_parallel.py

Requires ANTHROPIC_API_KEY to be set in environment:
    export ANTHROPIC_API_KEY='your-key-here'
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

# Test directories
TEST_DIRS = [
    "H01_A1g_Voltage_Correlation",
    "H02_Spatial_Heterogeneity",
    "H03_ID_IG_High_Voltage",
    "H04_Eg_Amplitude",
    "H05_Spatial_Decoupling",
    "H06_Edge_Center_Uniformity",
    "H07_A1g_Width",
    "H08_Gband_Redshift",
    "H09_Dband_Time_Delay",
    "H10_Spatial_Autocorrelation",
]


def run_single_test(test_dir: str) -> dict:
    """Run a single hypothesis test."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_path = os.path.join(script_dir, test_dir, "test_hypothesis.py")

    print(f"  Starting: {test_dir}")
    start_time = time.time()

    try:
        # Run the test script
        result = subprocess.run(
            [sys.executable, test_path],
            capture_output=True,
            text=True,
            timeout=600,  # 10 minute timeout
            env=os.environ.copy()
        )

        elapsed = time.time() - start_time

        # Try to read the result
        result_file = os.path.join(script_dir, test_dir, "results", "log.json")
        if os.path.exists(result_file):
            with open(result_file, 'r') as f:
                test_result = json.load(f)
            conclusion = test_result.get("parsed_result", {}).get("conclusion", "N/A")
            status = "SUCCESS"
        else:
            conclusion = "No result file"
            status = "FAILED"
            test_result = None

        return {
            "test_dir": test_dir,
            "status": status,
            "conclusion": conclusion,
            "elapsed_time": elapsed,
            "stdout": result.stdout[-500:] if result.stdout else "",
            "stderr": result.stderr[-500:] if result.stderr else "",
            "returncode": result.returncode
        }

    except subprocess.TimeoutExpired:
        return {
            "test_dir": test_dir,
            "status": "TIMEOUT",
            "conclusion": "Test timed out after 10 minutes",
            "elapsed_time": 600,
            "error": "Timeout"
        }
    except Exception as e:
        return {
            "test_dir": test_dir,
            "status": "ERROR",
            "conclusion": str(e),
            "elapsed_time": time.time() - start_time,
            "error": str(e)
        }


def generate_summary(results: list, total_time: float, output_dir: str):
    """Generate a markdown summary of all test results."""

    summary_path = os.path.join(output_dir, "BENCHMARK_SUMMARY.md")

    with open(summary_path, 'w') as f:
        f.write("# VOLTA Hypothesis Benchmark Summary\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Model**: claude-sonnet-4-20250514\n")
        f.write(f"**Total Execution Time**: {total_time:.1f} seconds\n\n")

        # Results table
        f.write("## Results\n\n")
        f.write("| # | Hypothesis | Status | Conclusion | Time (s) |\n")
        f.write("|---|-----------|--------|------------|----------|\n")

        for r in sorted(results, key=lambda x: x["test_dir"]):
            status_icon = {"SUCCESS": "✓", "FAILED": "✗", "TIMEOUT": "⏱", "ERROR": "!"}.get(r["status"], "?")
            conclusion = str(r.get("conclusion", "N/A"))[:60]
            elapsed = f"{r.get('elapsed_time', 0):.1f}"
            f.write(f"| {r['test_dir'][:3]} | {r['test_dir'][4:]} | {status_icon} {r['status']} | {conclusion} | {elapsed} |\n")

        # Statistics
        successful = sum(1 for r in results if r["status"] == "SUCCESS")
        failed = sum(1 for r in results if r["status"] in ["FAILED", "ERROR", "TIMEOUT"])

        f.write(f"\n## Statistics\n\n")
        f.write(f"- **Successful**: {successful}/{len(results)}\n")
        f.write(f"- **Failed**: {failed}/{len(results)}\n")
        f.write(f"- **Average Time**: {sum(r.get('elapsed_time', 0) for r in results)/len(results):.1f}s\n")

        # Detailed results
        f.write("\n## Detailed Results\n\n")
        for r in sorted(results, key=lambda x: x["test_dir"]):
            f.write(f"### {r['test_dir']}\n")
            f.write(f"- **Status**: {r['status']}\n")
            f.write(f"- **Conclusion**: {r.get('conclusion', 'N/A')}\n")
            f.write(f"- **Time**: {r.get('elapsed_time', 0):.1f}s\n")
            if r.get("error"):
                f.write(f"- **Error**: {r['error']}\n")
            f.write("\n")

    print(f"\nSummary saved to: {summary_path}")
    return summary_path


def main():
    """Run all tests in parallel."""

    # Check API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY environment variable not set!")
        print("\nPlease set it with:")
        print("  export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)

    print("=" * 70)
    print("VOLTA Parallel Hypothesis Benchmark")
    print("=" * 70)
    print(f"Running {len(TEST_DIRS)} hypothesis tests in parallel...")
    print(f"Model: claude-sonnet-4-20250514")
    print("=" * 70)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    start_time = time.time()
    results = []

    # Run tests in parallel (max 5 workers to avoid API rate limits)
    max_workers = min(5, len(TEST_DIRS))
    print(f"\nUsing {max_workers} parallel workers\n")

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_test = {executor.submit(run_single_test, td): td for td in TEST_DIRS}

        for future in as_completed(future_to_test):
            test_dir = future_to_test[future]
            try:
                result = future.result()
                results.append(result)
                status_icon = {"SUCCESS": "✓", "FAILED": "✗"}.get(result["status"], "?")
                print(f"  [{status_icon}] {test_dir}: {result['status']} - {result.get('conclusion', 'N/A')[:50]}")
            except Exception as e:
                print(f"  [!] {test_dir}: Exception - {str(e)}")
                results.append({
                    "test_dir": test_dir,
                    "status": "ERROR",
                    "error": str(e)
                })

    total_time = time.time() - start_time

    print("\n" + "=" * 70)
    print("BENCHMARK COMPLETE")
    print("=" * 70)
    print(f"Total time: {total_time:.1f} seconds")

    # Generate summary
    summary_path = generate_summary(results, total_time, script_dir)

    # Save JSON results
    json_path = os.path.join(script_dir, "benchmark_results.json")
    with open(json_path, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_time": total_time,
            "results": results
        }, f, indent=2, default=str)

    print(f"JSON results: {json_path}")

    # Print quick summary
    successful = sum(1 for r in results if r["status"] == "SUCCESS")
    print(f"\nSuccessful: {successful}/{len(results)}")

    return results


if __name__ == "__main__":
    main()
