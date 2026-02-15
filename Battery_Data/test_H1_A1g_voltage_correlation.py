"""
Hypothesis H1: A1g Peak Center Correlates Negatively with Voltage (State of Charge)

Test: The A1g peak center position (cm^-1) decreases (redshifts) with increasing
voltage during charging, reflecting delithiation-induced M-O bond weakening in
Li-rich layered oxides due to oxygen redox participation and structural distortion.
"""

import pandas as pd
import numpy as np
from scipy import stats
import os

# Output file
OUTPUT_DIR = "/Users/carrot/Desktop/POPPER/Battery_Data/hypothesis_test_outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "H1_A1g_voltage_correlation_results.txt")

def main():
    results = []
    results.append("=" * 70)
    results.append("HYPOTHESIS H1: A1g Peak Center NEGATIVE Correlation with Voltage")
    results.append("=" * 70)

    # Load data
    data_path = "/Users/carrot/Desktop/POPPER/Battery_Data/raman_peaks_decomposed.csv"
    df = pd.read_csv(data_path)

    results.append(f"\nDataset loaded: {len(df)} rows")
    results.append(f"Unique time steps: {df['time_idx'].nunique()}")
    results.append(f"Unique pixels: {df['pixel_id'].nunique()}")
    results.append(f"Voltage range: {df['Voltage'].min():.3f}V to {df['Voltage'].max():.3f}V")

    # Method 1: Overall correlation (all data points)
    results.append("\n" + "-" * 50)
    results.append("METHOD 1: Overall Pearson & Spearman Correlation")
    results.append("-" * 50)

    pearson_r, pearson_p = stats.pearsonr(df['Voltage'], df['A1g_Center'])
    spearman_r, spearman_p = stats.spearmanr(df['Voltage'], df['A1g_Center'])

    results.append(f"Pearson correlation:  r = {pearson_r:.4f}, p-value = {pearson_p:.2e}")
    results.append(f"Spearman correlation: rho = {spearman_r:.4f}, p-value = {spearman_p:.2e}")

    # Method 2: Mean A1g per time step vs voltage
    results.append("\n" + "-" * 50)
    results.append("METHOD 2: Mean A1g_Center per Time Step vs Voltage")
    results.append("-" * 50)

    time_grouped = df.groupby('time_idx').agg({
        'A1g_Center': ['mean', 'std'],
        'Voltage': 'first'
    }).reset_index()
    time_grouped.columns = ['time_idx', 'A1g_mean', 'A1g_std', 'Voltage']

    pearson_r2, pearson_p2 = stats.pearsonr(time_grouped['Voltage'], time_grouped['A1g_mean'])
    spearman_r2, spearman_p2 = stats.spearmanr(time_grouped['Voltage'], time_grouped['A1g_mean'])

    results.append(f"Pearson correlation:  r = {pearson_r2:.4f}, p-value = {pearson_p2:.2e}")
    results.append(f"Spearman correlation: rho = {spearman_r2:.4f}, p-value = {spearman_p2:.2e}")

    # A1g shift statistics
    results.append("\n" + "-" * 50)
    results.append("A1g Peak Shift Analysis")
    results.append("-" * 50)

    initial_A1g = time_grouped[time_grouped['time_idx'] == 0]['A1g_mean'].values[0]
    final_A1g = time_grouped[time_grouped['time_idx'] == time_grouped['time_idx'].max()]['A1g_mean'].values[0]

    results.append(f"Initial mean A1g (t=0): {initial_A1g:.2f} cm^-1")
    results.append(f"Final mean A1g (t=max): {final_A1g:.2f} cm^-1")
    results.append(f"Total shift: {final_A1g - initial_A1g:.2f} cm^-1")

    # Monotonicity test
    results.append("\n" + "-" * 50)
    results.append("Monotonicity Analysis")
    results.append("-" * 50)

    sorted_by_voltage = time_grouped.sort_values('Voltage')
    a1g_diffs = np.diff(sorted_by_voltage['A1g_mean'].values)
    positive_shifts = np.sum(a1g_diffs > 0)
    total_shifts = len(a1g_diffs)
    monotonicity_ratio = positive_shifts / total_shifts

    results.append(f"Positive shifts when voltage increases: {positive_shifts}/{total_shifts}")
    results.append(f"Monotonicity ratio: {monotonicity_ratio:.2%}")

    # Conclusion
    results.append("\n" + "=" * 70)
    results.append("CONCLUSION")
    results.append("=" * 70)

    if pearson_r2 < -0.5 and pearson_p2 < 0.05:
        verdict = "SUPPORTED"
        explanation = f"Strong negative correlation (r={pearson_r2:.3f}) between A1g center and voltage."
    elif pearson_r2 < 0 and pearson_p2 < 0.05:
        verdict = "PARTIALLY SUPPORTED"
        explanation = f"Weak but significant negative correlation (r={pearson_r2:.3f})."
    elif pearson_r2 > 0 and pearson_p2 < 0.05:
        verdict = "REFUTED"
        explanation = f"Significant POSITIVE correlation observed (r={pearson_r2:.3f})."
    else:
        verdict = "INCONCLUSIVE"
        explanation = f"No significant correlation found (p={pearson_p2:.3f})."

    results.append(f"\nHypothesis H1: {verdict}")
    results.append(explanation)
    results.append(f"A1g peak shifted by {final_A1g - initial_A1g:.2f} cm^-1 during charging.")

    # Write results
    output_text = "\n".join(results)
    print(output_text)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output_text)

    print(f"\nResults saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
