"""
Hypothesis H15: Cation Mixing Increases with Cycle Number

Test: Ni2+/Li+ cation mixing in the layered structure increases progressively
with cycle number, detectable through Eg/A1g intensity ratio changes.

Expected: NOT VERIFIABLE - Only single cycle data available.
"""

import pandas as pd
import numpy as np
import os

OUTPUT_DIR = "/Users/carrot/Desktop/POPPER/Battery_Data/hypothesis_test_outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "H15_cation_mixing_results.txt")

def main():
    results = []
    results.append("=" * 70)
    results.append("HYPOTHESIS H15: Cation Mixing vs Cycle Number")
    results.append("=" * 70)

    # Load data
    data_path = "/Users/carrot/Desktop/POPPER/Battery_Data/raman_peaks_decomposed.csv"
    df = pd.read_csv(data_path)

    results.append("\n" + "-" * 50)
    results.append("Cycle Number Analysis")
    results.append("-" * 50)

    # Check for cycle information
    results.append(f"\nTime steps in dataset: {df['time_idx'].nunique()}")
    results.append(f"Time range: 0 to {df['Time_Min'].max():.0f} minutes ({df['Time_Min'].max()/60:.1f} hours)")

    # Voltage trajectory to detect cycles
    time_avg = df.groupby('time_idx').agg({
        'Voltage': 'first',
        'Time_Min': 'first'
    }).sort_values('Time_Min')

    v_min = time_avg['Voltage'].min()
    v_max = time_avg['Voltage'].max()

    results.append(f"\nVoltage range: {v_min:.3f}V to {v_max:.3f}V")
    results.append(f"Voltage trajectory: Predominantly {'increasing' if time_avg['Voltage'].iloc[-1] > time_avg['Voltage'].iloc[0] else 'decreasing'}")

    # Count cycles
    voltage_diff = np.diff(time_avg['Voltage'])
    direction_changes = np.sum(np.diff(np.sign(voltage_diff)) != 0)
    estimated_cycles = max(0.5, direction_changes / 2)

    results.append(f"\nEstimated complete cycles: {estimated_cycles:.1f}")
    results.append("(Testing cation mixing vs cycle number requires many cycles)")

    results.append("\n" + "-" * 50)
    results.append("Eg/A1g Ratio Analysis (Current Data)")
    results.append("-" * 50)

    # Calculate Eg/A1g ratio for single cycle
    df['Eg_A1g_ratio'] = df['Eg_Amp'] / df['A1g_Amp']

    time_ratio = df.groupby('time_idx').agg({
        'Eg_A1g_ratio': 'mean',
        'Voltage': 'first'
    }).reset_index()

    results.append(f"\nEg/A1g ratio range (single cycle): {time_ratio['Eg_A1g_ratio'].min():.3f} to {time_ratio['Eg_A1g_ratio'].max():.3f}")
    results.append(f"Mean Eg/A1g ratio: {time_ratio['Eg_A1g_ratio'].mean():.3f}")

    results.append("\nNote: We can track Eg/A1g within a single cycle,")
    results.append("but CANNOT assess cycle-to-cycle evolution of cation mixing.")

    results.append("\n" + "-" * 50)
    results.append("Requirements for H15 Testing")
    results.append("-" * 50)

    results.append("\nTo test cation mixing vs cycle number:")
    results.append("  1. Raman data from multiple complete cycles - NOT AVAILABLE")
    results.append("  2. Cycle number tracking - NOT AVAILABLE")
    results.append("  3. Eg/A1g ratio at same SOC across cycles - NOT AVAILABLE")
    results.append("  4. Ideally 50-100+ cycles for trend analysis - NOT AVAILABLE")

    results.append("\nCurrent dataset provides:")
    results.append(f"  - {estimated_cycles:.1f} cycle(s) only")
    results.append("  - Eg/A1g ratio evolution WITHIN single cycle")
    results.append("  - No cycle-indexed data")

    # Conclusion
    results.append("\n" + "=" * 70)
    results.append("CONCLUSION")
    results.append("=" * 70)

    verdict = "NOT SUPPORTED (DATA INSUFFICIENT)"

    results.append(f"\nHypothesis H15: {verdict}")
    results.append("\nReason: Only single cycle data is available.")
    results.append("Testing cation mixing evolution requires tracking the")
    results.append("Eg/A1g ratio (or other cation mixing indicators) across")
    results.append("multiple complete charge-discharge cycles.")
    results.append("\nMissing data:")
    results.append("  - Multi-cycle Raman spectroscopy data")
    results.append("  - Cycle number indexing")
    results.append("  - Eg/A1g ratio at consistent SOC points per cycle")
    results.append("  - Long-term cycling Raman data (50-100+ cycles)")

    # Write results
    output_text = "\n".join(results)
    print(output_text)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output_text)

    print(f"\nResults saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
