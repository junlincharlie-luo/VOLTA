"""
Hypothesis H13: Oxygen Release Occurs Above 4.5V During First Charge

Test: Irreversible oxygen evolution from the lattice occurs when voltage
exceeds 4.5V during the first charge activation cycle.

Expected: NOT VERIFIABLE - No oxygen detection data available.
"""

import pandas as pd
import numpy as np
import os

OUTPUT_DIR = "/Users/carrot/Desktop/POPPER/Battery_Data/hypothesis_test_outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "H13_oxygen_release_results.txt")

def main():
    results = []
    results.append("=" * 70)
    results.append("HYPOTHESIS H13: Oxygen Release Above 4.5V")
    results.append("=" * 70)

    # Load data
    data_path = "/Users/carrot/Desktop/POPPER/Battery_Data/raman_peaks_decomposed.csv"
    df = pd.read_csv(data_path)

    results.append("\n" + "-" * 50)
    results.append("Available Raman Peaks in Dataset")
    results.append("-" * 50)

    peak_columns = ['Eg_Center', 'Eg_Amp', 'A1g_Center', 'A1g_Amp',
                    'D_Center', 'D_Amp', 'G_Center', 'G_Amp']

    results.append("\nFitted Raman peaks:")
    results.append("  1. Eg peak (~475 cm^-1) - M-O bending mode")
    results.append("  2. A1g peak (~590 cm^-1) - M-O stretching mode")
    results.append("  3. D-band (~1350 cm^-1) - Disordered carbon")
    results.append("  4. G-band (~1585 cm^-1) - Graphitic carbon")

    results.append("\n" + "-" * 50)
    results.append("Oxygen Detection Requirements")
    results.append("-" * 50)

    results.append("\nMethods to detect O2 release:")
    results.append("  1. DEMS (Differential Electrochemical Mass Spectrometry)")
    results.append("     - Directly measures evolved O2 gas")
    results.append("     - STATUS: NOT AVAILABLE")
    results.append("")
    results.append("  2. O2 Raman signature (~1555 cm^-1)")
    results.append("     - Would appear as new peak during O2 evolution")
    results.append("     - STATUS: NOT FITTED IN DATASET")
    results.append("")
    results.append("  3. Lattice oxygen loss indicators")
    results.append("     - M-O peak intensity changes could be indirect evidence")
    results.append("     - STATUS: INDIRECT, NOT CONCLUSIVE")

    # Check high voltage data
    results.append("\n" + "-" * 50)
    results.append("High Voltage Data Availability")
    results.append("-" * 50)

    high_v_data = df[df['Voltage'] > 4.5]
    results.append(f"\nData points above 4.5V: {len(high_v_data)}")
    results.append(f"Voltage range: {df['Voltage'].min():.3f}V to {df['Voltage'].max():.3f}V")

    if len(high_v_data) > 0:
        results.append(f"High voltage time range: {high_v_data['Time_Min'].min():.0f} to {high_v_data['Time_Min'].max():.0f} min")
        results.append("\nNote: While data above 4.5V exists, there is no O2-specific")
        results.append("detection method in the Raman fitting to confirm O2 release.")

    # Check for O2-related spectral features
    results.append("\n" + "-" * 50)
    results.append("Spectral Range Check")
    results.append("-" * 50)

    results.append("\nO2 Raman signature: ~1555 cm^-1")
    results.append("Fitted peak ranges in dataset:")
    results.append(f"  - Eg: {df['Eg_Center'].min():.0f} - {df['Eg_Center'].max():.0f} cm^-1")
    results.append(f"  - A1g: {df['A1g_Center'].min():.0f} - {df['A1g_Center'].max():.0f} cm^-1")
    results.append(f"  - D-band: {df['D_Center'].min():.0f} - {df['D_Center'].max():.0f} cm^-1")
    results.append(f"  - G-band: {df['G_Center'].min():.0f} - {df['G_Center'].max():.0f} cm^-1")
    results.append("\nO2 peak region (1555 cm^-1): NOT SEPARATELY FITTED")

    # Conclusion
    results.append("\n" + "=" * 70)
    results.append("CONCLUSION")
    results.append("=" * 70)

    verdict = "NOT SUPPORTED (DATA INSUFFICIENT)"

    results.append(f"\nHypothesis H13: {verdict}")
    results.append("\nReason: No oxygen-specific detection data is available.")
    results.append("The Raman dataset only contains fitted peaks for cathode M-O")
    results.append("vibrations and carbon bands. O2 gas evolution cannot be directly")
    results.append("confirmed without:")
    results.append("\nMissing data:")
    results.append("  - DEMS or mass spectrometry data")
    results.append("  - O2 Raman peak fitting at ~1555 cm^-1")
    results.append("  - Gas evolution measurements")
    results.append("  - Quantitative oxygen stoichiometry analysis")

    # Write results
    output_text = "\n".join(results)
    print(output_text)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output_text)

    print(f"\nResults saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
