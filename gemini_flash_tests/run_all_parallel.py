#!/usr/bin/env python3
"""
Run all 20 VOLTA hypothesis tests in parallel using Gemini 3 Flash Preview.

Usage:
    export GOOGLE_API_KEY='your-api-key'
    python run_all_parallel.py [--max-workers N]
"""

import os
import sys
import json
import time
import argparse
import importlib.util
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

# List of all hypothesis IDs
HYPOTHESIS_IDS = [f"H{i:02d}" for i in range(1, 21)]


def run_single_hypothesis(hypothesis_id: str) -> dict:
    """Run a single hypothesis test and return the result."""
    try:
        # Import the test module
        script_dir = os.path.dirname(os.path.abspath(__file__))
        module_path = os.path.join(script_dir, f"test_{hypothesis_id}.py")

        spec = importlib.util.spec_from_file_location(f"test_{hypothesis_id}", module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[f"test_{hypothesis_id}"] = module
        spec.loader.exec_module(module)

        # Run the test
        result = module.run_hypothesis_test()

        return {
            "hypothesis_id": hypothesis_id,
            "status": "success" if result else "failed",
            "result": result
        }
    except Exception as e:
        return {
            "hypothesis_id": hypothesis_id,
            "status": "error",
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(description="Run all 20 VOLTA hypothesis tests in parallel")
    parser.add_argument("--max-workers", type=int, default=5,
                        help="Maximum number of parallel workers (default: 5)")
    parser.add_argument("--hypotheses", type=str, nargs="+", default=None,
                        help="Specific hypotheses to run (e.g., H01 H02 H03)")
    args = parser.parse_args()

    # Check for API key
    if not os.environ.get("GOOGLE_API_KEY"):
        print("ERROR: GOOGLE_API_KEY environment variable not set!")
        print("Set it with: export GOOGLE_API_KEY='your-key'")
        sys.exit(1)

    # Determine which hypotheses to run
    hypotheses_to_run = args.hypotheses if args.hypotheses else HYPOTHESIS_IDS

    print("=" * 70)
    print("VOLTA Benchmark: 20 Hypotheses with Gemini 2.0 Flash")
    print("=" * 70)
    print(f"Running {len(hypotheses_to_run)} hypotheses with {args.max_workers} parallel workers")
    print(f"Hypotheses: {', '.join(hypotheses_to_run)}")
    print("=" * 70)

    start_time = time.time()
    results = []
    completed = 0

    # Run tests in parallel
    with ProcessPoolExecutor(max_workers=args.max_workers) as executor:
        # Submit all tasks
        future_to_hypothesis = {
            executor.submit(run_single_hypothesis, h_id): h_id
            for h_id in hypotheses_to_run
        }

        # Collect results as they complete
        for future in as_completed(future_to_hypothesis):
            hypothesis_id = future_to_hypothesis[future]
            completed += 1

            try:
                result = future.result()
                results.append(result)

                status = result.get("status", "unknown")
                if status == "success":
                    parsed = result.get("result", {})
                    if isinstance(parsed, dict):
                        conclusion = parsed.get("parsed_result", {})
                        if isinstance(conclusion, dict):
                            conclusion = conclusion.get("conclusion", "N/A")
                        else:
                            conclusion = getattr(conclusion, "conclusion", "N/A")
                    else:
                        conclusion = "N/A"
                    print(f"[{completed}/{len(hypotheses_to_run)}] {hypothesis_id}: SUCCESS - Conclusion: {conclusion}")
                else:
                    print(f"[{completed}/{len(hypotheses_to_run)}] {hypothesis_id}: {status.upper()} - {result.get('error', 'Unknown error')}")

            except Exception as e:
                results.append({
                    "hypothesis_id": hypothesis_id,
                    "status": "error",
                    "error": str(e)
                })
                print(f"[{completed}/{len(hypotheses_to_run)}] {hypothesis_id}: ERROR - {e}")

    elapsed_time = time.time() - start_time

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    success_count = sum(1 for r in results if r.get("status") == "success")
    error_count = sum(1 for r in results if r.get("status") == "error")
    failed_count = sum(1 for r in results if r.get("status") == "failed")

    print(f"Total hypotheses tested: {len(results)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {failed_count}")
    print(f"Errors: {error_count}")
    print(f"Total elapsed time: {elapsed_time:.1f} seconds")
    print(f"Average time per hypothesis: {elapsed_time/len(results):.1f} seconds")

    # Save summary
    script_dir = os.path.dirname(os.path.abspath(__file__))
    summary_file = os.path.join(script_dir, "results", "summary.json")
    os.makedirs(os.path.dirname(summary_file), exist_ok=True)

    summary = {
        "model": "gemini-3-flash-preview",
        "total_hypotheses": len(results),
        "successful": success_count,
        "failed": failed_count,
        "errors": error_count,
        "elapsed_time_seconds": elapsed_time,
        "timestamp": datetime.now().isoformat(),
        "results": results
    }

    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2, default=str)

    print(f"\nResults saved to: {summary_file}")
    print("=" * 70)

    # Print results table
    print("\nRESULTS TABLE:")
    print("-" * 70)
    print(f"{'Hypothesis':<12} {'Status':<10} {'Conclusion':<15} {'Time (s)':<10}")
    print("-" * 70)

    for r in sorted(results, key=lambda x: x["hypothesis_id"]):
        h_id = r["hypothesis_id"]
        status = r.get("status", "unknown")

        if status == "success" and r.get("result"):
            parsed = r["result"]
            if isinstance(parsed, dict):
                elapsed = parsed.get("elapsed_time_seconds", 0)
                parsed_result = parsed.get("parsed_result", {})
                if isinstance(parsed_result, dict):
                    conclusion = str(parsed_result.get("conclusion", "N/A"))[:13]
                else:
                    conclusion = str(getattr(parsed_result, "conclusion", "N/A"))[:13]
            else:
                elapsed = 0
                conclusion = "N/A"
        else:
            elapsed = 0
            conclusion = "N/A"

        print(f"{h_id:<12} {status:<10} {conclusion:<15} {elapsed:<10.1f}")

    print("-" * 70)


if __name__ == "__main__":
    main()
