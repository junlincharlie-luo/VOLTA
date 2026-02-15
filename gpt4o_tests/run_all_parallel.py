"""
Parallel Runner for All 20 GPT-4o Hypothesis Tests

This script runs all 20 hypothesis tests in parallel using multiprocessing.
Each test uses GPT-4o to evaluate the hypothesis against the battery Raman data.

Usage:
    export OPENAI_API_KEY='your-api-key'
    python run_all_parallel.py

Options:
    - Adjust MAX_PARALLEL to control how many tests run simultaneously
    - Results are saved to gpt4o_tests/results/H{XX}/
"""

import os
import sys
import time
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime

# Maximum number of parallel tests (adjust based on API rate limits)
MAX_PARALLEL = 5

# List of all hypothesis test files
TEST_FILES = [
    "test_H01.py", "test_H02.py", "test_H03.py", "test_H04.py", "test_H05.py",
    "test_H06.py", "test_H07.py", "test_H08.py", "test_H09.py", "test_H10.py",
    "test_H11.py", "test_H12.py", "test_H13.py", "test_H14.py", "test_H15.py",
    "test_H16.py", "test_H17.py", "test_H18.py", "test_H19.py", "test_H20.py",
]


def run_test(test_file):
    """Run a single hypothesis test and return the result."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_path = os.path.join(script_dir, test_file)

    hypothesis_id = test_file.replace("test_", "").replace(".py", "")

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting {hypothesis_id}...")

    start_time = time.time()

    try:
        result = subprocess.run(
            [sys.executable, test_path],
            capture_output=True,
            text=True,
            timeout=1800  # 30 minute timeout per test
        )
        elapsed = time.time() - start_time

        success = result.returncode == 0

        print(f"[{datetime.now().strftime('%H:%M:%S')}] {hypothesis_id} completed in {elapsed:.1f}s - {'SUCCESS' if success else 'FAILED'}")

        return {
            "hypothesis_id": hypothesis_id,
            "test_file": test_file,
            "success": success,
            "elapsed_time": elapsed,
            "stdout": result.stdout[-2000:] if result.stdout else "",  # Last 2000 chars
            "stderr": result.stderr[-1000:] if result.stderr else "",
        }

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {hypothesis_id} TIMEOUT after {elapsed:.1f}s")
        return {
            "hypothesis_id": hypothesis_id,
            "test_file": test_file,
            "success": False,
            "elapsed_time": elapsed,
            "stdout": "",
            "stderr": "Test timed out after 30 minutes",
        }

    except Exception as e:
        elapsed = time.time() - start_time
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {hypothesis_id} ERROR: {str(e)}")
        return {
            "hypothesis_id": hypothesis_id,
            "test_file": test_file,
            "success": False,
            "elapsed_time": elapsed,
            "stdout": "",
            "stderr": str(e),
        }


def main():
    """Run all tests in parallel."""

    # Check for API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY environment variable not set!")
        print("Set it with: export OPENAI_API_KEY='your-key'")
        sys.exit(1)

    print("=" * 70)
    print("GPT-4o Hypothesis Testing - Parallel Runner")
    print("=" * 70)
    print(f"Running {len(TEST_FILES)} tests with max {MAX_PARALLEL} parallel processes")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    start_time = time.time()
    results = []

    with ProcessPoolExecutor(max_workers=MAX_PARALLEL) as executor:
        future_to_test = {executor.submit(run_test, tf): tf for tf in TEST_FILES}

        for future in as_completed(future_to_test):
            test_file = future_to_test[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Exception for {test_file}: {e}")
                results.append({
                    "hypothesis_id": test_file.replace("test_", "").replace(".py", ""),
                    "test_file": test_file,
                    "success": False,
                    "elapsed_time": 0,
                    "stdout": "",
                    "stderr": str(e),
                })

    total_time = time.time() - start_time

    # Sort results by hypothesis ID
    results.sort(key=lambda x: x["hypothesis_id"])

    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful

    print(f"\nTotal tests: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")

    print("\n" + "-" * 70)
    print("Results by hypothesis:")
    print("-" * 70)

    for r in results:
        status = "PASS" if r["success"] else "FAIL"
        print(f"  {r['hypothesis_id']}: {status} ({r['elapsed_time']:.1f}s)")

    # Save summary
    script_dir = os.path.dirname(os.path.abspath(__file__))
    summary_file = os.path.join(script_dir, "results", "parallel_run_summary.txt")
    os.makedirs(os.path.dirname(summary_file), exist_ok=True)

    with open(summary_file, 'w') as f:
        f.write(f"GPT-4o Hypothesis Testing - Parallel Run Summary\n")
        f.write(f"{'=' * 60}\n")
        f.write(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total tests: {len(results)}\n")
        f.write(f"Successful: {successful}\n")
        f.write(f"Failed: {failed}\n")
        f.write(f"Total time: {total_time:.1f} seconds\n\n")

        f.write(f"Results by hypothesis:\n")
        f.write(f"{'-' * 60}\n")
        for r in results:
            status = "PASS" if r["success"] else "FAIL"
            f.write(f"  {r['hypothesis_id']}: {status} ({r['elapsed_time']:.1f}s)\n")

    print(f"\nSummary saved to: {summary_file}")
    print("=" * 70)


if __name__ == "__main__":
    main()
