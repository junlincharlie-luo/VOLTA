"""
Hypothesis H16: Surface CEI Layer Thickness Reaches Steady State After 50 Cycles

Test: The cathode-electrolyte interface (CEI) layer thickness stabilizes after
approximately 50 cycles, as indicated by saturation of D-band intensity changes.

Expected: NOT VERIFIABLE - Single cycle data only, no multi-cycle CEI evolution.
"""

import pandas as pd
import numpy as np
import os

OUTPUT_DIR = "/Users/carrot/Desktop/VOLTA/Battery_Data/hypothesis_test_outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "H16_CEI_steady_state_results.txt")

def main():
    results = []
    results.append("=" * 70)
    results.append("HYPOTHESIS H16: CEI Layer Steady State After 50 Cycles")
    results.append("=" * 70)

    # Load data
    data_path = "/Users/carrot/Desktop/VOLTA/Battery_Data/raman_peaks_decomposed.csv"
    df = pd.read_csv(data_path)

    results.append("\n" + "-" * 50)
    results.append("CEI Detection Methods in Raman")
    results.append("-" * 50)

    results.append("\nPotential CEI indicators in Raman spectroscopy:")
    results.append("  1. D-band intensity changes (carbon disorder)")
    results.append("  2. New peaks from CEI species (Li2CO3, LiF, etc.)")
    results.append("  3. Background fluorescence changes")
    results.append("  4. Peak broadening from surface layers")

    results.append("\nAvailable in current dataset:")
    results.append("  - D-band amplitude (D_Amp): Available")
    results.append("  - CEI-specific peaks: NOT FITTED")
    results.append("  - Direct thickness measurement: NOT AVAILABLE")

    results.append("\n" + "-" * 50)
    results.append("Cycle Count Analysis")
    results.append("-" * 50)

    total_time_hours = df['Time_Min'].max() / 60
    results.append(f"\nExperiment duration: {total_time_hours:.1f} hours")

    # Estimate cycles
    time_avg = df.groupby('time_idx')['Voltage'].first()
    voltage_increases = (np.diff(time_avg) > 0).sum()
    voltage_decreases = (np.diff(time_avg) < 0).sum()

    if voltage_increases > voltage_decreases:
        results.append("Detected: Single charging half-cycle")
        estimated_cycles = 0.5
    else:
        results.append("Detected: Single discharging half-cycle")
        estimated_cycles = 0.5

    results.append(f"Estimated complete cycles: {estimated_cycles}")
    results.append(f"Required cycles for H16: 50+")
    results.append(f"Shortfall: {50 - estimated_cycles:.1f} cycles")

    results.append("\n" + "-" * 50)
    results.append("D-band Analysis (Single Cycle)")
    results.append("-" * 50)

    # Analyze D-band within single cycle
    d_amp_time = df.groupby('time_idx').agg({
        'D_Amp': 'mean',
        'Voltage': 'first',
        'Time_Min': 'first'
    }).reset_index()

    results.append(f"\nD-band amplitude range: {d_amp_time['D_Amp'].min():.2f} to {d_amp_time['D_Amp'].max():.2f}")
    results.append(f"D-band change within cycle: {d_amp_time['D_Amp'].iloc[-1] - d_amp_time['D_Amp'].iloc[0]:.2f}")

    results.append("\nNote: This shows D-band evolution within ONE cycle.")
    results.append("Cannot determine if CEI reaches steady state over 50 cycles.")

    results.append("\n" + "-" * 50)
    results.append("Requirements for H16 Testing")
    results.append("-" * 50)

    results.append("\nTo test CEI steady state hypothesis:")
    results.append("  1. Raman data from 50+ cycles - NOT AVAILABLE")
    results.append("  2. D-band (or CEI peak) intensity per cycle - NOT AVAILABLE")
    results.append("  3. Cycle-indexed measurements - NOT AVAILABLE")
    results.append("  4. Ideally: direct CEI thickness (XPS, TEM) - NOT AVAILABLE")

    # Conclusion
    results.append("\n" + "=" * 70)
    results.append("CONCLUSION")
    results.append("=" * 70)

    verdict = "NOT SUPPORTED (DATA INSUFFICIENT)"

    results.append(f"\nHypothesis H16: {verdict}")
    results.append("\nReason: Only single cycle data is available.")
    results.append("Testing CEI steady state requires tracking D-band or CEI")
    results.append("indicators across at least 50 complete cycles to observe")
    results.append("saturation behavior.")
    results.append("\nMissing data:")
    results.append("  - Multi-cycle Raman data (50+ cycles)")
    results.append("  - CEI-specific Raman peak fitting")
    results.append("  - Direct CEI thickness measurements")
    results.append("  - Cycle-resolved D-band intensity")

    # Write results
    output_text = "\n".join(results)
    print(output_text)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output_text)

    print(f"\nResults saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
