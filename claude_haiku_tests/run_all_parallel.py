"""
Run All 20 Hypotheses Benchmark with Claude Haiku via LangChain

Tests all 20 hypotheses from the VOLTA benchmark using Claude 3.5 Haiku.
Note: H11-H20 are designed to be non-verifiable with the available data.

Usage: python run_all_parallel.py [--max-workers N]
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

# Add VOLTA to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

HYPOTHESES = [f"H{i:02d}" for i in range(1, 21)]


def run_single_test(hypothesis_id: str) -> dict:
    """Run a single hypothesis test as a subprocess."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_script = os.path.join(script_dir, f"test_{hypothesis_id}.py")

    if not os.path.exists(test_script):
        return {
            "hypothesis_id": hypothesis_id,
            "status": "FAILED",
            "error": f"Test script not found: {test_script}"
        }

    try:
        start_time = time.time()
        result = subprocess.run(
            [sys.executable, test_script],
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout per test
        )
        elapsed_time = time.time() - start_time

        if result.returncode == 0:
            return {
                "hypothesis_id": hypothesis_id,
                "status": "SUCCESS",
                "elapsed_time": elapsed_time,
                "stdout": result.stdout[-1000:] if len(result.stdout) > 1000 else result.stdout
            }
        else:
            return {
                "hypothesis_id": hypothesis_id,
                "status": "FAILED",
                "elapsed_time": elapsed_time,
                "error": result.stderr[-500:] if result.stderr else "Unknown error",
                "stdout": result.stdout[-500:] if result.stdout else ""
            }
    except subprocess.TimeoutExpired:
        return {
            "hypothesis_id": hypothesis_id,
            "status": "TIMEOUT",
            "error": "Test exceeded 10 minute timeout"
        }
    except Exception as e:
        return {
            "hypothesis_id": hypothesis_id,
            "status": "EXCEPTION",
            "error": str(e)
        }


def run_all_tests(max_workers: int = 5):
    """Run all hypothesis tests in parallel."""

    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set!")
        print("Set it with: export ANTHROPIC_API_KEY='your-key'")
        return

    print("=" * 70)
    print("VOLTA Hypothesis Benchmark - Claude 3.5 Haiku via LangChain")
    print("=" * 70)
    print(f"Model: claude-3-5-haiku-20241022")
    print(f"Total hypotheses: {len(HYPOTHESES)}")
    print(f"  - Verifiable (H01-H10): 10")
    print(f"  - Non-verifiable (H11-H20): 10")
    print(f"Max parallel workers: {max_workers}")
    print("=" * 70)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    results = []
    start_time = time.time()

    print(f"\nStarting parallel execution...")

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_hypothesis = {
            executor.submit(run_single_test, h_id): h_id
            for h_id in HYPOTHESES
        }

        for future in as_completed(future_to_hypothesis):
            hypothesis_id = future_to_hypothesis[future]
            try:
                result = future.result()
                results.append(result)
                status_icon = "+" if result["status"] == "SUCCESS" else "x"
                print(f"  [{status_icon}] {hypothesis_id}: {result['status']}")
            except Exception as e:
                print(f"  [x] {hypothesis_id}: Exception - {str(e)}")
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
        "model": "claude-3-5-haiku-20241022",
        "total_time_seconds": total_time,
        "successful_count": len(successful),
        "failed_count": len(failed),
        "results": sorted(results, key=lambda x: x["hypothesis_id"])
    }

    summary_file = os.path.join(script_dir, "results", f"benchmark_summary_{timestamp}.json")
    os.makedirs(os.path.dirname(summary_file), exist_ok=True)
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2, default=str)

    # Generate markdown summary
    md_summary_file = os.path.join(script_dir, "results", f"SUMMARY_{timestamp}.md")
    with open(md_summary_file, 'w') as f:
        f.write("# VOLTA Benchmark Results - Claude 3.5 Haiku\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Model**: claude-3-5-haiku-20241022 via LangChain\n")
        f.write(f"**Total Time**: {total_time:.1f} seconds\n\n")

        f.write("## Part A: Verifiable Hypotheses (H01-H10)\n\n")
        f.write("| ID | Status | Time (s) |\n")
        f.write("|-----|--------|----------|\n")

        for r in sorted([r for r in results if r["hypothesis_id"] <= "H10"],
                       key=lambda x: x["hypothesis_id"]):
            status = "+" if r["status"] == "SUCCESS" else "x"
            elapsed = f"{r.get('elapsed_time', 0):.1f}" if r.get('elapsed_time') else "N/A"
            f.write(f"| {r['hypothesis_id']} | {status} {r['status']} | {elapsed} |\n")

        f.write("\n## Part B: Non-Verifiable Hypotheses (H11-H20)\n\n")
        f.write("*These hypotheses are designed to be non-verifiable with the available data.*\n\n")
        f.write("| ID | Status | Time (s) |\n")
        f.write("|-----|--------|----------|\n")

        for r in sorted([r for r in results if r["hypothesis_id"] > "H10"],
                       key=lambda x: x["hypothesis_id"]):
            status = "+" if r["status"] == "SUCCESS" else "x"
            elapsed = f"{r.get('elapsed_time', 0):.1f}" if r.get('elapsed_time') else "N/A"
            f.write(f"| {r['hypothesis_id']} | {status} {r['status']} | {elapsed} |\n")

        f.write(f"\n## Statistics\n")
        f.write(f"- **Successful**: {len(successful)}/{len(results)}\n")
        f.write(f"- **Failed**: {len(failed)}/{len(results)}\n")

        if failed:
            f.write("\n## Failures\n")
            for r in sorted(failed, key=lambda x: x["hypothesis_id"]):
                f.write(f"\n### {r['hypothesis_id']}\n")
                f.write(f"```\n{str(r.get('error', 'Unknown error'))[:300]}\n```\n")

    print(f"\nResults saved to: {os.path.dirname(summary_file)}")
    print(f"Summary: {md_summary_file}")

    return summary


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Run all 20 hypothesis tests with Claude Haiku"
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=5,
        help="Maximum parallel workers (default: 5)"
    )

    args = parser.parse_args()

    run_all_tests(max_workers=args.max_workers)
