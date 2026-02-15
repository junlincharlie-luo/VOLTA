#!/usr/bin/env python3
"""Run a hypothesis test with a timeout."""
import subprocess
import sys
import os

if len(sys.argv) < 3:
    print("Usage: python run_with_timeout.py <timeout_seconds> <test_file.py>")
    sys.exit(1)

timeout_sec = int(sys.argv[1])
test_file = sys.argv[2]

env = os.environ.copy()
env['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY', '')

try:
    result = subprocess.run(
        [sys.executable, test_file],
        timeout=timeout_sec,
        env=env,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    sys.exit(result.returncode)
except subprocess.TimeoutExpired:
    print(f"\n=== TIMEOUT: {test_file} exceeded {timeout_sec} seconds ===")
    sys.exit(124)
except Exception as e:
    print(f"\n=== ERROR: {e} ===")
    sys.exit(1)
