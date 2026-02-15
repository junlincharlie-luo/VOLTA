"""
Hypothesis H7: A1g Peak Width (Sigma) Decreases During Charging

Test: The A1g peak width (A1g_Sigma) decreases with voltage, indicating peak
sharpening as lithium extraction creates a more uniform local bonding environment
and reduces the distribution of M-O bond lengths.
"""

import pandas as pd
import numpy as np
from scipy import stats
import os

OUTPUT_DIR = "/Users/carrot/Desktop/POPPER/Battery_Data/hypothesis_test_outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "H7_A1g_width_results.txt")

def main():
    results = []
    results.append("=" * 70)
    results.append("HYPOTHESIS H7: A1g Peak Width Decreases with Voltage")
    results.append("=" * 70)

    # Load data
    data_path = "/Users/carrot/Desktop/POPPER/Battery_Data/raman_peaks_decomposed.csv"
    df = pd.read_csv(data_path)

    results.append(f"\nDataset loaded: {len(df)} rows")
    results.append(f"A1g_Sigma range: {df['A1g_Sigma'].min():.2f} to {df['A1g_Sigma'].max():.2f}")

    # Overall correlation
    results.append("\n" + "-" * 50)
    results.append("Overall Correlation: A1g_Sigma vs Voltage")
    results.append("-" * 50)

    pearson_r, pearson_p = stats.pearsonr(df['Voltage'], df['A1g_Sigma'])
    spearman_r, spearman_p = stats.spearmanr(df['Voltage'], df['A1g_Sigma'])

    results.append(f"Pearson:  r = {pearson_r:.4f}, p = {pearson_p:.2e}")
    results.append(f"Spearman: rho = {spearman_r:.4f}, p = {spearman_p:.2e}")

    # Time-averaged analysis
    results.append("\n" + "-" * 50)
    results.append("Time-Averaged A1g_Sigma Evolution")
    results.append("-" * 50)

    time_avg = df.groupby('time_idx').agg({
        'A1g_Sigma': ['mean', 'std', 'median'],
        'Voltage': 'first',
        'Time_Min': 'first'
    }).reset_index()
    time_avg.columns = ['time_idx', 'Sigma_mean', 'Sigma_std', 'Sigma_median', 'Voltage', 'Time_Min']

    initial = time_avg[time_avg['time_idx'] == 0].iloc[0]
    final = time_avg[time_avg['time_idx'] == time_avg['time_idx'].max()].iloc[0]

    results.append(f"\nInitial state (V = {initial['Voltage']:.3f}V):")
    results.append(f"  Mean A1g_Sigma = {initial['Sigma_mean']:.2f} cm^-1")

    results.append(f"\nFinal state (V = {final['Voltage']:.3f}V):")
    results.append(f"  Mean A1g_Sigma = {final['Sigma_mean']:.2f} cm^-1")

    sigma_change = final['Sigma_mean'] - initial['Sigma_mean']
    sigma_change_pct = sigma_change / initial['Sigma_mean'] * 100
    results.append(f"\nChange: {sigma_change:.2f} cm^-1 ({sigma_change_pct:+.1f}%)")

    # Time-averaged correlation
    results.append("\n" + "-" * 50)
    results.append("Time-Averaged Correlation")
    results.append("-" * 50)

    pearson_avg, p_avg = stats.pearsonr(time_avg['Voltage'], time_avg['Sigma_mean'])
    spearman_avg, sp_avg = stats.spearmanr(time_avg['Voltage'], time_avg['Sigma_mean'])

    results.append(f"Pearson (time-averaged):  r = {pearson_avg:.4f}, p = {p_avg:.2e}")
    results.append(f"Spearman (time-averaged): rho = {spearman_avg:.4f}, p = {sp_avg:.2e}")

    # Linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        time_avg['Voltage'], time_avg['Sigma_mean']
    )
    results.append(f"\nLinear regression:")
    results.append(f"  Slope: {slope:.4f} cm^-1 per Volt")
    results.append(f"  R-squared: {r_value**2:.4f}")
    results.append(f"  P-value: {p_value:.2e}")

    # Voltage bin analysis
    results.append("\n" + "-" * 50)
    results.append("Voltage Bin Analysis")
    results.append("-" * 50)

    bins = [3.0, 3.5, 4.0, 4.3, 4.5, 5.0]
    df['V_bin'] = pd.cut(df['Voltage'], bins=bins)

    for vbin in sorted(df['V_bin'].dropna().unique()):
        subset = df[df['V_bin'] == vbin]['A1g_Sigma']
        results.append(f"  {vbin}: Mean = {subset.mean():.2f}, Std = {subset.std():.2f}")

    # Conclusion
    results.append("\n" + "=" * 70)
    results.append("CONCLUSION")
    results.append("=" * 70)

    if pearson_avg < -0.3 and p_avg < 0.05:
        verdict = "SUPPORTED"
        explanation = f"Strong negative correlation (r={pearson_avg:.3f}): A1g width decreases with charging."
    elif pearson_avg < 0 and p_avg < 0.05:
        verdict = "PARTIALLY SUPPORTED"
        explanation = f"Weak but significant negative correlation (r={pearson_avg:.3f})."
    elif pearson_avg > 0 and p_avg < 0.05:
        verdict = "REFUTED"
        explanation = f"A1g width actually INCREASES with voltage (r={pearson_avg:.3f})."
    else:
        verdict = "INCONCLUSIVE"
        explanation = f"No significant trend found (p={p_avg:.3f})."

    results.append(f"\nHypothesis H7: {verdict}")
    results.append(explanation)
    results.append(f"A1g_Sigma changed by {sigma_change_pct:+.1f}% during charging.")

    # Write results
    output_text = "\n".join(results)
    print(output_text)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output_text)

    print(f"\nResults saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
