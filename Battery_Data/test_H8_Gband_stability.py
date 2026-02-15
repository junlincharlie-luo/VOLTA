"""
Hypothesis H8: G-band Position Shows Voltage-Dependent Redshift During Charging

Test: The G-band center position shifts to lower wavenumbers (redshifts) with
increasing voltage, reflecting charge transfer interactions between the carbon
conductive network and the delithiating cathode particles.
"""

import pandas as pd
import numpy as np
from scipy import stats
import os

OUTPUT_DIR = "/Users/carrot/Desktop/POPPER/Battery_Data/hypothesis_test_outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "H8_Gband_stability_results.txt")

def main():
    results = []
    results.append("=" * 70)
    results.append("HYPOTHESIS H8: G-band Voltage-Dependent Redshift")
    results.append("=" * 70)

    # Load data
    data_path = "/Users/carrot/Desktop/POPPER/Battery_Data/raman_peaks_decomposed.csv"
    df = pd.read_csv(data_path)

    results.append(f"\nDataset loaded: {len(df)} rows")
    results.append(f"G_Center range: {df['G_Center'].min():.2f} to {df['G_Center'].max():.2f} cm^-1")

    # Overall statistics
    results.append("\n" + "-" * 50)
    results.append("G-band Center Statistics")
    results.append("-" * 50)

    results.append(f"Mean G_Center: {df['G_Center'].mean():.2f} cm^-1")
    results.append(f"Std G_Center:  {df['G_Center'].std():.2f} cm^-1")
    results.append(f"Total range:   {df['G_Center'].max() - df['G_Center'].min():.2f} cm^-1")

    # Time-averaged analysis
    results.append("\n" + "-" * 50)
    results.append("Time-Averaged G_Center Evolution")
    results.append("-" * 50)

    time_avg = df.groupby('time_idx').agg({
        'G_Center': ['mean', 'std'],
        'Voltage': 'first'
    }).reset_index()
    time_avg.columns = ['time_idx', 'G_mean', 'G_std', 'Voltage']

    initial = time_avg[time_avg['time_idx'] == 0].iloc[0]
    final = time_avg[time_avg['time_idx'] == time_avg['time_idx'].max()].iloc[0]

    results.append(f"\nInitial state (V = {initial['Voltage']:.3f}V): G_Center = {initial['G_mean']:.2f} cm^-1")
    results.append(f"Final state (V = {final['Voltage']:.3f}V):   G_Center = {final['G_mean']:.2f} cm^-1")

    g_shift = final['G_mean'] - initial['G_mean']
    results.append(f"Total shift: {g_shift:.2f} cm^-1")

    # Time-averaged range
    g_range = time_avg['G_mean'].max() - time_avg['G_mean'].min()
    results.append(f"Range of time-averaged G_Center: {g_range:.2f} cm^-1")

    # Correlation with voltage
    results.append("\n" + "-" * 50)
    results.append("Correlation: G_Center vs Voltage")
    results.append("-" * 50)

    pearson_r, pearson_p = stats.pearsonr(time_avg['Voltage'], time_avg['G_mean'])
    spearman_r, spearman_p = stats.spearmanr(time_avg['Voltage'], time_avg['G_mean'])

    results.append(f"Pearson (time-averaged):  r = {pearson_r:.4f}, p = {pearson_p:.2e}")
    results.append(f"Spearman (time-averaged): rho = {spearman_r:.4f}, p = {spearman_p:.2e}")

    # Linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        time_avg['Voltage'], time_avg['G_mean']
    )
    results.append(f"\nLinear regression:")
    results.append(f"  Slope: {slope:.4f} cm^-1 per Volt")
    results.append(f"  R-squared: {r_value**2:.4f}")

    # Voltage bin analysis
    results.append("\n" + "-" * 50)
    results.append("Voltage Bin Analysis")
    results.append("-" * 50)

    bins = [3.0, 3.5, 4.0, 4.3, 4.5, 5.0]
    df['V_bin'] = pd.cut(df['Voltage'], bins=bins)

    for vbin in sorted(df['V_bin'].dropna().unique()):
        subset = df[df['V_bin'] == vbin]['G_Center']
        results.append(f"  {vbin}: Mean = {subset.mean():.2f}, Std = {subset.std():.2f}")

    # Stability criterion: shift < 5 cm^-1
    results.append("\n" + "-" * 50)
    results.append("Stability Criterion Check")
    results.append("-" * 50)

    STABILITY_THRESHOLD = 5.0  # cm^-1
    results.append(f"Threshold: |shift| < {STABILITY_THRESHOLD} cm^-1")
    results.append(f"Observed total shift: {abs(g_shift):.2f} cm^-1")
    results.append(f"Observed time-averaged range: {g_range:.2f} cm^-1")

    is_stable = abs(g_shift) < STABILITY_THRESHOLD and g_range < STABILITY_THRESHOLD

    # Conclusion
    results.append("\n" + "=" * 70)
    results.append("CONCLUSION")
    results.append("=" * 70)

    if pearson_r < -0.3 and pearson_p < 0.05:
        verdict = "SUPPORTED"
        explanation = f"G-band shows voltage-dependent redshift: r = {pearson_r:.3f}, slope = {slope:.2f} cm^-1/V."
    elif pearson_r < 0 and pearson_p < 0.05:
        verdict = "PARTIALLY SUPPORTED"
        explanation = f"Weak but significant negative correlation (r={pearson_r:.3f})."
    else:
        verdict = "REFUTED"
        explanation = f"No significant voltage-dependent redshift detected."

    results.append(f"\nHypothesis H8: {verdict}")
    results.append(explanation)
    results.append(f"Total G-band shift: {g_shift:.2f} cm^-1")

    # Write results
    output_text = "\n".join(results)
    print(output_text)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output_text)

    print(f"\nResults saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
