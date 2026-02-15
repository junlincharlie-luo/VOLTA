"""
Hypothesis H3: ID/IG Ratio Decreases at High Voltages (>4.3V)

Test: The ID/IG ratio (carbon disorder indicator) decreases significantly when
voltage exceeds 4.3V, indicating enhanced graphitic ordering or preferential
G-band enhancement due to electrochemical activation of the carbon network.
"""

import pandas as pd
import numpy as np
from scipy import stats
import os

# Output file
OUTPUT_DIR = "/Users/carrot/Desktop/POPPER/Battery_Data/hypothesis_test_outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "H3_ID_IG_high_voltage_results.txt")

def main():
    results = []
    results.append("=" * 70)
    results.append("HYPOTHESIS H3: ID/IG Ratio Decreases at High Voltages (>4.3V)")
    results.append("=" * 70)

    # Load data
    data_path = "/Users/carrot/Desktop/POPPER/Battery_Data/raman_peaks_decomposed.csv"
    df = pd.read_csv(data_path)

    results.append(f"\nDataset loaded: {len(df)} rows")
    results.append(f"Voltage range: {df['Voltage'].min():.3f}V to {df['Voltage'].max():.3f}V")
    results.append(f"ID/IG range: {df['ID_IG_Ratio'].min():.3f} to {df['ID_IG_Ratio'].max():.3f}")

    # Define voltage threshold
    V_THRESHOLD = 4.3

    # Split data into low and high voltage groups
    results.append("\n" + "-" * 50)
    results.append(f"Group Comparison: V < {V_THRESHOLD}V vs V >= {V_THRESHOLD}V")
    results.append("-" * 50)

    low_v = df[df['Voltage'] < V_THRESHOLD]['ID_IG_Ratio']
    high_v = df[df['Voltage'] >= V_THRESHOLD]['ID_IG_Ratio']

    results.append(f"\nLow voltage (< {V_THRESHOLD}V):")
    results.append(f"  N = {len(low_v)}")
    results.append(f"  Mean ID/IG = {low_v.mean():.4f} +/- {low_v.std():.4f}")
    results.append(f"  Median = {low_v.median():.4f}")

    results.append(f"\nHigh voltage (>= {V_THRESHOLD}V):")
    results.append(f"  N = {len(high_v)}")
    results.append(f"  Mean ID/IG = {high_v.mean():.4f} +/- {high_v.std():.4f}")
    results.append(f"  Median = {high_v.median():.4f}")

    # Statistical tests
    results.append("\n" + "-" * 50)
    results.append("Statistical Tests")
    results.append("-" * 50)

    # Independent t-test
    t_stat, t_pvalue = stats.ttest_ind(high_v, low_v)
    results.append(f"\nIndependent t-test (high vs low):")
    results.append(f"  t-statistic = {t_stat:.4f}")
    results.append(f"  p-value = {t_pvalue:.2e}")

    # Mann-Whitney U test (non-parametric)
    u_stat, u_pvalue = stats.mannwhitneyu(high_v, low_v, alternative='greater')
    results.append(f"\nMann-Whitney U test (high > low):")
    results.append(f"  U-statistic = {u_stat:.0f}")
    results.append(f"  p-value = {u_pvalue:.2e}")

    # Effect size (Cohen's d)
    pooled_std = np.sqrt((low_v.std()**2 + high_v.std()**2) / 2)
    cohens_d = (high_v.mean() - low_v.mean()) / pooled_std
    results.append(f"\nEffect size (Cohen's d): {cohens_d:.4f}")

    # Correlation analysis across all data
    results.append("\n" + "-" * 50)
    results.append("Overall Correlation: ID/IG vs Voltage")
    results.append("-" * 50)

    pearson_r, pearson_p = stats.pearsonr(df['Voltage'], df['ID_IG_Ratio'])
    spearman_r, spearman_p = stats.spearmanr(df['Voltage'], df['ID_IG_Ratio'])

    results.append(f"Pearson:  r = {pearson_r:.4f}, p = {pearson_p:.2e}")
    results.append(f"Spearman: rho = {spearman_r:.4f}, p = {spearman_p:.2e}")

    # Time-averaged analysis
    results.append("\n" + "-" * 50)
    results.append("Time-Averaged Analysis")
    results.append("-" * 50)

    time_avg = df.groupby('time_idx').agg({
        'ID_IG_Ratio': ['mean', 'std'],
        'Voltage': 'first'
    }).reset_index()
    time_avg.columns = ['time_idx', 'ID_IG_mean', 'ID_IG_std', 'Voltage']

    low_v_avg = time_avg[time_avg['Voltage'] < V_THRESHOLD]['ID_IG_mean']
    high_v_avg = time_avg[time_avg['Voltage'] >= V_THRESHOLD]['ID_IG_mean']

    results.append(f"Low voltage mean (time-averaged): {low_v_avg.mean():.4f}")
    results.append(f"High voltage mean (time-averaged): {high_v_avg.mean():.4f}")
    results.append(f"Difference: {high_v_avg.mean() - low_v_avg.mean():.4f}")

    # Multiple threshold analysis
    results.append("\n" + "-" * 50)
    results.append("Voltage Bin Analysis")
    results.append("-" * 50)

    bins = [3.0, 3.5, 4.0, 4.3, 4.5, 4.7, 5.0]
    df['V_bin'] = pd.cut(df['Voltage'], bins=bins)

    for vbin in sorted(df['V_bin'].dropna().unique()):
        subset = df[df['V_bin'] == vbin]['ID_IG_Ratio']
        results.append(f"  {vbin}: Mean = {subset.mean():.4f}, Std = {subset.std():.4f}, N = {len(subset)}")

    # Conclusion
    results.append("\n" + "=" * 70)
    results.append("CONCLUSION")
    results.append("=" * 70)

    mean_diff = high_v.mean() - low_v.mean()
    pct_change = mean_diff / low_v.mean() * 100

    if t_stat < 0 and t_pvalue < 0.05:
        if abs(cohens_d) > 0.2:
            verdict = "SUPPORTED"
            explanation = f"ID/IG significantly lower at V>{V_THRESHOLD}V (p={t_pvalue:.2e}, d={cohens_d:.3f})."
        else:
            verdict = "PARTIALLY SUPPORTED"
            explanation = f"Statistically significant but small effect (d={cohens_d:.3f})."
    elif t_stat > 0 and t_pvalue < 0.05:
        verdict = "REFUTED"
        explanation = f"ID/IG is actually HIGHER at high voltages (p={t_pvalue:.2e})."
    else:
        verdict = "INCONCLUSIVE"
        explanation = f"No significant difference found (p={t_pvalue:.3f})."

    results.append(f"\nHypothesis H3: {verdict}")
    results.append(explanation)
    results.append(f"Mean ID/IG change: {mean_diff:+.4f} ({pct_change:+.2f}%) at V>{V_THRESHOLD}V")

    # Write results
    output_text = "\n".join(results)
    print(output_text)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output_text)

    print(f"\nResults saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
