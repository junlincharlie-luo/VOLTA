"""
Hypothesis H11: Voltage Fade Occurs After Extended Cycling

Test: The average discharge voltage decreases by >50 mV after 100 charge-discharge
cycles due to structural transformation from layered to spinel phase.

Expected: NOT VERIFIABLE - Dataset contains only a single charge cycle.
"""

import pandas as pd
import numpy as np
import os

OUTPUT_DIR = "/Users/carrot/Desktop/VOLTA/Battery_Data/hypothesis_test_outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "H11_voltage_fade_results.txt")

def main():
    results = []
    results.append("=" * 70)
    results.append("HYPOTHESIS H11: Voltage Fade After Extended Cycling")
    results.append("=" * 70)

    # Load data
    data_path = "/Users/carrot/Desktop/VOLTA/Battery_Data/raman_peaks_decomposed.csv"
    df = pd.read_csv(data_path)

    results.append("\n" + "-" * 50)
    results.append("Dataset Analysis")
    results.append("-" * 50)

    # Check for cycle information
    results.append(f"\nTotal data points: {len(df)}")
    results.append(f"Time range: {df['Time_Min'].min():.1f} to {df['Time_Min'].max():.1f} minutes")
    results.append(f"Time range: {df['Time_Min'].max() / 60:.1f} hours")
    results.append(f"Voltage range: {df['Voltage'].min():.3f}V to {df['Voltage'].max():.3f}V")

    # Check voltage trajectory
    time_avg = df.groupby('time_idx').agg({
        'Voltage': 'first',
        'Time_Min': 'first'
    }).reset_index().sort_values('Time_Min')

    voltage_increases = (np.diff(time_avg['Voltage']) > 0).sum()
    voltage_decreases = (np.diff(time_avg['Voltage']) < 0).sum()

    results.append(f"\nVoltage trajectory analysis:")
    results.append(f"  Time steps with voltage increase: {voltage_increases}")
    results.append(f"  Time steps with voltage decrease: {voltage_decreases}")

    # Determine if this is charging or discharging
    if voltage_increases > voltage_decreases:
        cycle_type = "CHARGING (voltage increasing)"
    else:
        cycle_type = "DISCHARGING (voltage decreasing)"

    results.append(f"  Detected cycle type: {cycle_type}")

    # Check for multiple cycles
    results.append("\n" + "-" * 50)
    results.append("Cycle Detection")
    results.append("-" * 50)

    # Look for voltage reversals (would indicate cycle boundaries)
    voltage_diff = np.diff(time_avg['Voltage'])
    sign_changes = np.sum(np.diff(np.sign(voltage_diff)) != 0)

    results.append(f"Number of voltage direction changes: {sign_changes}")
    results.append(f"(Multiple cycles would show repeated charge-discharge patterns)")

    # Estimate number of complete cycles
    # A complete cycle = charge + discharge
    if sign_changes < 2:
        estimated_cycles = 0.5  # Only partial cycle
    else:
        estimated_cycles = sign_changes / 2

    results.append(f"Estimated complete cycles: {estimated_cycles:.1f}")

    # Required data check
    results.append("\n" + "-" * 50)
    results.append("Data Requirements Check")
    results.append("-" * 50)

    required_cycles = 100
    results.append(f"\nRequired for hypothesis testing:")
    results.append(f"  - At least {required_cycles} charge-discharge cycles")
    results.append(f"  - Discharge voltage data for each cycle")
    results.append(f"  - Ability to track average discharge voltage over cycles")

    results.append(f"\nAvailable in dataset:")
    results.append(f"  - Number of cycles: ~{estimated_cycles:.1f} (INSUFFICIENT)")
    results.append(f"  - Discharge data: {'NO' if voltage_increases > voltage_decreases else 'PARTIAL'}")
    results.append(f"  - Multi-cycle tracking: NO")

    # Conclusion
    results.append("\n" + "=" * 70)
    results.append("CONCLUSION")
    results.append("=" * 70)

    verdict = "NOT SUPPORTED (DATA INSUFFICIENT)"

    results.append(f"\nHypothesis H11: {verdict}")
    results.append("\nReason: The dataset contains only a SINGLE partial charge cycle")
    results.append(f"spanning {df['Time_Min'].max() / 60:.1f} hours. Testing voltage fade requires")
    results.append("at least 100 complete charge-discharge cycles with discharge")
    results.append("voltage measurements, which are not available in this dataset.")
    results.append("\nMissing data:")
    results.append("  - Multi-cycle electrochemical data")
    results.append("  - Discharge curves for each cycle")
    results.append("  - Long-term cycling data (weeks/months)")

    # Write results
    output_text = "\n".join(results)
    print(output_text)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output_text)

    print(f"\nResults saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
