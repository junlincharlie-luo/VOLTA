"""
Hypothesis H19: Electrolyte Decomposition Products Show Characteristic Raman Signatures

Test: Specific electrolyte decomposition products (Li2CO3, LiF, organic carbonates)
are detectable through their characteristic Raman peaks.

Expected: NOT VERIFIABLE - Only 4 peak regions fitted, no electrolyte species peaks.
"""

import pandas as pd
import numpy as np
import os

OUTPUT_DIR = "/Users/carrot/Desktop/POPPER/Battery_Data/hypothesis_test_outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "H19_electrolyte_decomposition_results.txt")

def main():
    results = []
    results.append("=" * 70)
    results.append("HYPOTHESIS H19: Electrolyte Decomposition Raman Signatures")
    results.append("=" * 70)

    # Load data
    data_path = "/Users/carrot/Desktop/POPPER/Battery_Data/raman_peaks_decomposed.csv"
    df = pd.read_csv(data_path)

    results.append("\n" + "-" * 50)
    results.append("Fitted Peaks in Dataset")
    results.append("-" * 50)

    results.append("\nPeaks included in dataset:")
    results.append("  1. Eg peak   (~475 cm^-1)  - Cathode M-O bending")
    results.append("  2. A1g peak  (~590 cm^-1)  - Cathode M-O stretching")
    results.append("  3. D-band    (~1350 cm^-1) - Disordered carbon")
    results.append("  4. G-band    (~1585 cm^-1) - Graphitic carbon")

    results.append("\n" + "-" * 50)
    results.append("Expected Electrolyte Decomposition Raman Peaks")
    results.append("-" * 50)

    results.append("\nCommon electrolyte decomposition products and their Raman signatures:")
    results.append("")
    results.append("  Li2CO3 (Lithium carbonate):")
    results.append("    - ~1090 cm^-1 (symmetric CO3 stretch) - NOT FITTED")
    results.append("    - ~155 cm^-1 (lattice mode) - NOT FITTED")
    results.append("")
    results.append("  LiF (Lithium fluoride):")
    results.append("    - ~280 cm^-1 - NOT FITTED")
    results.append("    - Weak Raman scatterer")
    results.append("")
    results.append("  Li2O (Lithium oxide):")
    results.append("    - ~525 cm^-1 - NOT FITTED (overlaps with Eg region)")
    results.append("")
    results.append("  Organic carbonates (EC, DMC decomposition):")
    results.append("    - ~900 cm^-1 (C-O stretch) - NOT FITTED")
    results.append("    - ~1750 cm^-1 (C=O stretch) - NOT FITTED")
    results.append("")
    results.append("  LixPFy species:")
    results.append("    - ~740 cm^-1 (P-F stretch) - NOT FITTED")

    results.append("\n" + "-" * 50)
    results.append("Spectral Coverage Analysis")
    results.append("-" * 50)

    results.append("\nFitted peak center ranges in dataset:")
    results.append(f"  Eg:     {df['Eg_Center'].min():.0f} - {df['Eg_Center'].max():.0f} cm^-1")
    results.append(f"  A1g:    {df['A1g_Center'].min():.0f} - {df['A1g_Center'].max():.0f} cm^-1")
    results.append(f"  D-band: {df['D_Center'].min():.0f} - {df['D_Center'].max():.0f} cm^-1")
    results.append(f"  G-band: {df['G_Center'].min():.0f} - {df['G_Center'].max():.0f} cm^-1")

    results.append("\nSpectral regions NOT covered:")
    results.append("  - 100-400 cm^-1 (LiF, Li2CO3 lattice modes)")
    results.append("  - 700-1000 cm^-1 (P-F, C-O stretches)")
    results.append("  - 1050-1150 cm^-1 (Li2CO3 symmetric stretch)")
    results.append("  - 1700-1800 cm^-1 (C=O stretches)")

    results.append("\n" + "-" * 50)
    results.append("Data Availability Summary")
    results.append("-" * 50)

    results.append("\nRequired for H19 testing:")
    results.append("  1. Full Raman spectra (raw data) - NOT AVAILABLE")
    results.append("  2. Peak fitting for Li2CO3 (~1090 cm^-1) - NOT DONE")
    results.append("  3. Peak fitting for LiF (~280 cm^-1) - NOT DONE")
    results.append("  4. Peak fitting for organic species - NOT DONE")

    results.append("\nProvided in dataset:")
    results.append("  - Only 4 pre-selected peak regions")
    results.append("  - No raw spectra for additional analysis")
    results.append("  - No electrolyte-specific peak parameters")

    # Conclusion
    results.append("\n" + "=" * 70)
    results.append("CONCLUSION")
    results.append("=" * 70)

    verdict = "NOT SUPPORTED (DATA INSUFFICIENT)"

    results.append(f"\nHypothesis H19: {verdict}")
    results.append("\nReason: The dataset only contains 4 fitted peak regions")
    results.append("(Eg, A1g, D-band, G-band). Electrolyte decomposition products")
    results.append("like Li2CO3, LiF, and organic carbonates have Raman signatures")
    results.append("in spectral regions that were not fitted or provided.")
    results.append("\nMissing data:")
    results.append("  - Raw Raman spectra")
    results.append("  - Peak fitting for electrolyte decomposition products")
    results.append("  - Spectral coverage below 400 cm^-1 and 700-1100 cm^-1")
    results.append("  - Li2CO3, LiF, LixPFy specific peak analysis")

    # Write results
    output_text = "\n".join(results)
    print(output_text)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output_text)

    print(f"\nResults saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
