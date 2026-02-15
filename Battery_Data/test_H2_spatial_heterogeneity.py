"""
Hypothesis H2: Spatial Heterogeneity of A1g Peak Position Increases During Charging

Test: The standard deviation of A1g_Center across the 900 spatial pixels increases
as voltage increases, indicating growing electrochemical heterogeneity during delithiation.
"""

import pandas as pd
import numpy as np
from scipy import stats
import os

# Output file
OUTPUT_DIR = "/Users/carrot/Desktop/VOLTA/Battery_Data/hypothesis_test_outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "H2_spatial_heterogeneity_results.txt")

def main():
    results = []
    results.append("=" * 70)
    results.append("HYPOTHESIS H2: Spatial Heterogeneity of A1g vs Voltage")
    results.append("=" * 70)

    # Load data
    data_path = "/Users/carrot/Desktop/VOLTA/Battery_Data/raman_peaks_decomposed.csv"
    df = pd.read_csv(data_path)

    results.append(f"\nDataset loaded: {len(df)} rows")
    results.append(f"Spatial grid: 30x30 = 900 pixels")
    results.append(f"Time steps: {df['time_idx'].nunique()}")

    # Calculate spatial heterogeneity (std) at each time step
    results.append("\n" + "-" * 50)
    results.append("Spatial Heterogeneity Calculation")
    results.append("-" * 50)

    heterogeneity = df.groupby('time_idx').agg({
        'A1g_Center': ['mean', 'std', 'min', 'max'],
        'Voltage': 'first',
        'Time_Min': 'first'
    }).reset_index()
    heterogeneity.columns = ['time_idx', 'A1g_mean', 'A1g_std', 'A1g_min', 'A1g_max', 'Voltage', 'Time_Min']

    # Also calculate coefficient of variation
    heterogeneity['A1g_CV'] = heterogeneity['A1g_std'] / heterogeneity['A1g_mean'] * 100
    heterogeneity['A1g_range'] = heterogeneity['A1g_max'] - heterogeneity['A1g_min']

    results.append(f"Initial heterogeneity (t=0):")
    initial = heterogeneity[heterogeneity['time_idx'] == 0].iloc[0]
    results.append(f"  Std: {initial['A1g_std']:.2f} cm^-1, CV: {initial['A1g_CV']:.2f}%")
    results.append(f"  Range: {initial['A1g_range']:.2f} cm^-1")

    final = heterogeneity[heterogeneity['time_idx'] == heterogeneity['time_idx'].max()].iloc[0]
    results.append(f"\nFinal heterogeneity (t=max):")
    results.append(f"  Std: {final['A1g_std']:.2f} cm^-1, CV: {final['A1g_CV']:.2f}%")
    results.append(f"  Range: {final['A1g_range']:.2f} cm^-1")

    # Correlation between heterogeneity and voltage
    results.append("\n" + "-" * 50)
    results.append("Correlation: Heterogeneity vs Voltage")
    results.append("-" * 50)

    # Std vs Voltage
    pearson_std, p_std = stats.pearsonr(heterogeneity['Voltage'], heterogeneity['A1g_std'])
    spearman_std, sp_std = stats.spearmanr(heterogeneity['Voltage'], heterogeneity['A1g_std'])

    results.append(f"A1g_Std vs Voltage:")
    results.append(f"  Pearson:  r = {pearson_std:.4f}, p = {p_std:.2e}")
    results.append(f"  Spearman: rho = {spearman_std:.4f}, p = {sp_std:.2e}")

    # CV vs Voltage
    pearson_cv, p_cv = stats.pearsonr(heterogeneity['Voltage'], heterogeneity['A1g_CV'])
    spearman_cv, sp_cv = stats.spearmanr(heterogeneity['Voltage'], heterogeneity['A1g_CV'])

    results.append(f"\nA1g_CV vs Voltage:")
    results.append(f"  Pearson:  r = {pearson_cv:.4f}, p = {p_cv:.2e}")
    results.append(f"  Spearman: rho = {spearman_cv:.4f}, p = {sp_cv:.2e}")

    # Range vs Voltage
    pearson_range, p_range = stats.pearsonr(heterogeneity['Voltage'], heterogeneity['A1g_range'])

    results.append(f"\nA1g_Range vs Voltage:")
    results.append(f"  Pearson:  r = {pearson_range:.4f}, p = {p_range:.2e}")

    # Voltage bin analysis
    results.append("\n" + "-" * 50)
    results.append("Voltage Bin Analysis")
    results.append("-" * 50)

    bins = [3.0, 3.5, 4.0, 4.3, 4.5, 5.0]
    heterogeneity['V_bin'] = pd.cut(heterogeneity['Voltage'], bins=bins)
    bin_stats = heterogeneity.groupby('V_bin', observed=True).agg({
        'A1g_std': ['mean', 'std'],
        'A1g_CV': 'mean'
    })

    results.append("Mean heterogeneity per voltage bin:")
    for vbin in heterogeneity['V_bin'].dropna().unique():
        subset = heterogeneity[heterogeneity['V_bin'] == vbin]
        results.append(f"  {vbin}: Std = {subset['A1g_std'].mean():.2f} +/- {subset['A1g_std'].std():.2f} cm^-1")

    # Trend analysis
    results.append("\n" + "-" * 50)
    results.append("Linear Regression: Heterogeneity vs Voltage")
    results.append("-" * 50)

    slope, intercept, r_value, p_value, std_err = stats.linregress(
        heterogeneity['Voltage'], heterogeneity['A1g_std']
    )
    results.append(f"Slope: {slope:.4f} cm^-1 per Volt")
    results.append(f"R-squared: {r_value**2:.4f}")
    results.append(f"P-value: {p_value:.2e}")

    # Conclusion
    results.append("\n" + "=" * 70)
    results.append("CONCLUSION")
    results.append("=" * 70)

    std_change = final['A1g_std'] - initial['A1g_std']
    std_change_pct = (final['A1g_std'] / initial['A1g_std'] - 1) * 100

    if pearson_std > 0.3 and p_std < 0.05:
        verdict = "SUPPORTED"
        explanation = f"Significant positive correlation (r={pearson_std:.3f}) between spatial heterogeneity and voltage."
    elif pearson_std > 0 and p_std < 0.05:
        verdict = "PARTIALLY SUPPORTED"
        explanation = f"Weak but significant positive trend (r={pearson_std:.3f})."
    elif pearson_std < 0 and p_std < 0.05:
        verdict = "REFUTED"
        explanation = f"Heterogeneity actually DECREASES with voltage (r={pearson_std:.3f})."
    else:
        verdict = "INCONCLUSIVE"
        explanation = f"No significant trend found (p={p_std:.3f})."

    results.append(f"\nHypothesis H2: {verdict}")
    results.append(explanation)
    results.append(f"Heterogeneity changed from {initial['A1g_std']:.2f} to {final['A1g_std']:.2f} cm^-1 ({std_change_pct:+.1f}%)")

    # Write results
    output_text = "\n".join(results)
    print(output_text)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output_text)

    print(f"\nResults saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
