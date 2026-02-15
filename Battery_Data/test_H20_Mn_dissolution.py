"""
Hypothesis H20: Manganese Dissolution Rate Correlates with ID/IG Changes

Test: Manganese dissolution from the cathode into the electrolyte correlates
with ID/IG ratio changes, as dissolved Mn catalyzes electrolyte decomposition.

Expected: NOT VERIFIABLE - No Mn concentration or dissolution measurements.
"""

import pandas as pd
import numpy as np
from scipy import stats
import os

OUTPUT_DIR = "/Users/carrot/Desktop/POPPER/Battery_Data/hypothesis_test_outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "H20_Mn_dissolution_results.txt")

def main():
    results = []
    results.append("=" * 70)
    results.append("HYPOTHESIS H20: Mn Dissolution Correlation with ID/IG")
    results.append("=" * 70)

    # Load data
    data_path = "/Users/carrot/Desktop/POPPER/Battery_Data/raman_peaks_decomposed.csv"
    df = pd.read_csv(data_path)

    results.append("\n" + "-" * 50)
    results.append("Manganese Data Search")
    results.append("-" * 50)

    # Check for Mn-related columns
    mn_keywords = ['mn', 'manganese', 'dissolution', 'icp', 'concentration', 'ppm', 'metal']
    all_columns = list(df.columns)

    results.append(f"\nDataset columns: {all_columns}")

    found_mn_cols = [col for col in all_columns if any(kw.lower() in col.lower() for kw in mn_keywords)]
    results.append(f"\nMn-related columns: {found_mn_cols if found_mn_cols else 'NONE'}")

    results.append("\n" + "-" * 50)
    results.append("Methods to Measure Mn Dissolution")
    results.append("-" * 50)

    results.append("\nStandard methods for Mn dissolution measurement:")
    results.append("  1. ICP-OES (Inductively Coupled Plasma Optical Emission)")
    results.append("     - Measures Mn concentration in electrolyte")
    results.append("     - STATUS: NOT AVAILABLE")
    results.append("")
    results.append("  2. ICP-MS (Mass Spectrometry)")
    results.append("     - High sensitivity Mn quantification")
    results.append("     - STATUS: NOT AVAILABLE")
    results.append("")
    results.append("  3. AAS (Atomic Absorption Spectroscopy)")
    results.append("     - Alternative Mn quantification method")
    results.append("     - STATUS: NOT AVAILABLE")
    results.append("")
    results.append("  4. Post-mortem electrode analysis")
    results.append("     - XPS, EDS for surface Mn content")
    results.append("     - STATUS: NOT AVAILABLE")

    results.append("\n" + "-" * 50)
    results.append("ID/IG Ratio Data (Available)")
    results.append("-" * 50)

    # Analyze ID/IG data that IS available
    time_avg = df.groupby('time_idx').agg({
        'ID_IG_Ratio': 'mean',
        'Voltage': 'first',
        'Time_Min': 'first'
    }).reset_index()

    results.append(f"\nID/IG ratio range: {time_avg['ID_IG_Ratio'].min():.4f} to {time_avg['ID_IG_Ratio'].max():.4f}")
    results.append(f"ID/IG change over time: {time_avg['ID_IG_Ratio'].iloc[-1] - time_avg['ID_IG_Ratio'].iloc[0]:.4f}")

    # Correlation with voltage (as proxy for time/cycling)
    r, p = stats.pearsonr(time_avg['Voltage'], time_avg['ID_IG_Ratio'])
    results.append(f"\nID/IG vs Voltage correlation: r = {r:.4f}, p = {p:.2e}")

    results.append("\nNote: ID/IG changes are observed, but cannot be linked")
    results.append("to Mn dissolution without Mn concentration data.")

    results.append("\n" + "-" * 50)
    results.append("Hypothesis Testing Requirements")
    results.append("-" * 50)

    results.append("\nTo test Mn dissolution ↔ ID/IG correlation:")
    results.append("  1. Mn concentration vs time - NOT AVAILABLE")
    results.append("  2. ID/IG ratio vs time - AVAILABLE")
    results.append("  3. Correlation analysis - IMPOSSIBLE (missing Mn data)")
    results.append("  4. Causation mechanism verification - IMPOSSIBLE")

    results.append("\nAlternative approaches (also not available):")
    results.append("  - Mn content in cycled electrolyte samples")
    results.append("  - Electrode Mn content before/after cycling")
    results.append("  - Operando XAS for Mn oxidation state")

    results.append("\n" + "-" * 50)
    results.append("Material Context")
    results.append("-" * 50)

    results.append("\nCathode material: Li1.13Ni0.3Mn0.57O2 (Li-rich NMC)")
    results.append("  - High Mn content (57% of transition metals)")
    results.append("  - Known to have Mn dissolution issues at high voltage")
    results.append("  - Mn3+ → Mn2+ disproportionation can occur")
    results.append("\nBut: No direct Mn measurements in this Raman dataset.")

    # Conclusion
    results.append("\n" + "=" * 70)
    results.append("CONCLUSION")
    results.append("=" * 70)

    verdict = "NOT SUPPORTED (DATA INSUFFICIENT)"

    results.append(f"\nHypothesis H20: {verdict}")
    results.append("\nReason: No manganese dissolution data is available.")
    results.append("This Raman dataset provides ID/IG ratio evolution, but")
    results.append("correlating with Mn dissolution requires ICP-MS/OES or")
    results.append("similar elemental analysis of the electrolyte.")
    results.append("\nMissing data:")
    results.append("  - Mn concentration in electrolyte (ICP-OES/MS)")
    results.append("  - Time-resolved Mn dissolution measurements")
    results.append("  - Electrode Mn content analysis")
    results.append("  - Any elemental quantification data")

    # Write results
    output_text = "\n".join(results)
    print(output_text)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output_text)

    print(f"\nResults saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
