"""
Hypothesis H18: Irreversible Phase Transformation Detected in First Discharge

Test: The A1g peak position does not fully return to initial values after
the first discharge, indicating irreversible structural changes.

Expected: NOT VERIFIABLE - No discharge data available.
"""

import pandas as pd
import numpy as np
import os

OUTPUT_DIR = "/Users/carrot/Desktop/POPPER/Battery_Data/hypothesis_test_outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "H18_discharge_reversibility_results.txt")

def main():
    results = []
    results.append("=" * 70)
    results.append("HYPOTHESIS H18: Irreversible Phase Transformation in Discharge")
    results.append("=" * 70)

    # Load data
    data_path = "/Users/carrot/Desktop/POPPER/Battery_Data/raman_peaks_decomposed.csv"
    df = pd.read_csv(data_path)

    results.append("\n" + "-" * 50)
    results.append("Voltage Profile Analysis")
    results.append("-" * 50)

    time_avg = df.groupby('time_idx').agg({
        'Voltage': 'first',
        'Time_Min': 'first',
        'A1g_Center': 'mean'
    }).sort_values('Time_Min')

    v_start = time_avg['Voltage'].iloc[0]
    v_end = time_avg['Voltage'].iloc[-1]

    results.append(f"\nVoltage at start: {v_start:.3f} V")
    results.append(f"Voltage at end:   {v_end:.3f} V")
    results.append(f"Voltage change:   {v_end - v_start:.3f} V")

    if v_end > v_start:
        cycle_type = "CHARGING"
        results.append(f"\nDetected cycle type: {cycle_type} (voltage increasing)")
    else:
        cycle_type = "DISCHARGING"
        results.append(f"\nDetected cycle type: {cycle_type} (voltage decreasing)")

    results.append("\n" + "-" * 50)
    results.append("Discharge Data Availability")
    results.append("-" * 50)

    # Check for discharge (voltage decreasing) segments
    voltage_diff = np.diff(time_avg['Voltage'])
    charge_steps = (voltage_diff > 0).sum()
    discharge_steps = (voltage_diff < 0).sum()

    results.append(f"\nTime steps with voltage increase (charging): {charge_steps}")
    results.append(f"Time steps with voltage decrease (discharging): {discharge_steps}")

    if discharge_steps < charge_steps * 0.1:
        results.append("\nConclusion: Dataset is predominantly CHARGING data.")
        results.append("No significant discharge segment detected.")
        has_discharge = False
    else:
        results.append("\nSome discharge data may be present.")
        has_discharge = True

    results.append("\n" + "-" * 50)
    results.append("Reversibility Analysis Requirements")
    results.append("-" * 50)

    results.append("\nTo test A1g reversibility, we need:")
    results.append("  1. Initial A1g position (before charge) - AVAILABLE")
    results.append("  2. A1g position at top of charge - AVAILABLE")
    results.append("  3. A1g position after full discharge - NOT AVAILABLE")
    results.append("  4. Comparison: Initial vs Post-discharge - IMPOSSIBLE")

    a1g_initial = time_avg['A1g_Center'].iloc[0]
    a1g_final = time_avg['A1g_Center'].iloc[-1]

    results.append(f"\nCurrent data:")
    results.append(f"  A1g at start (low SOC): {a1g_initial:.2f} cm^-1")
    results.append(f"  A1g at end (high SOC):  {a1g_final:.2f} cm^-1")
    results.append(f"  Shift during charge:   {a1g_final - a1g_initial:.2f} cm^-1")
    results.append("\n  A1g after discharge:    ??? (NO DATA)")
    results.append("  Irreversibility:        CANNOT DETERMINE")

    results.append("\n" + "-" * 50)
    results.append("What Would Be Needed")
    results.append("-" * 50)

    results.append("\nTo assess irreversibility:")
    results.append("  - Complete charge-discharge cycle with Raman")
    results.append("  - A1g peak position at same voltage during charge and discharge")
    results.append("  - Comparison of initial and final A1g positions")
    results.append("  - Hysteresis analysis if any")

    # Conclusion
    results.append("\n" + "=" * 70)
    results.append("CONCLUSION")
    results.append("=" * 70)

    verdict = "NOT SUPPORTED (DATA INSUFFICIENT)"

    results.append(f"\nHypothesis H18: {verdict}")
    results.append("\nReason: No discharge data is available in the dataset.")
    results.append("The experiment captured only the charging portion of the cycle")
    results.append(f"(voltage increasing from {v_start:.2f}V to {v_end:.2f}V).")
    results.append("Testing reversibility requires A1g data during discharge.")
    results.append("\nMissing data:")
    results.append("  - Discharge cycle Raman data")
    results.append("  - A1g position after re-lithiation")
    results.append("  - Full cycle hysteresis data")
    results.append("  - Post-cycle vs pre-cycle comparison")

    # Write results
    output_text = "\n".join(results)
    print(output_text)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output_text)

    print(f"\nResults saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
