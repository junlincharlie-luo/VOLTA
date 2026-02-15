"""
Hypothesis H6: Edge and Center Pixels Show Uniform Electrochemical Behavior

Test: Pixels at the edges of the 30x30 mapping region exhibit statistically similar
A1g peak evolution compared to center pixels, indicating homogeneous electrochemical
accessibility across the mapped electrode area at the 30 um scale.
"""

import pandas as pd
import numpy as np
from scipy import stats
import os

OUTPUT_DIR = "/Users/carrot/Desktop/POPPER/Battery_Data/hypothesis_test_outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "H6_edge_vs_center_results.txt")

def main():
    results = []
    results.append("=" * 70)
    results.append("HYPOTHESIS H6: Edge-Center Uniformity")
    results.append("=" * 70)

    # Load data
    data_path = "/Users/carrot/Desktop/POPPER/Battery_Data/raman_peaks_decomposed.csv"
    df = pd.read_csv(data_path)

    results.append(f"\nDataset loaded: {len(df)} rows")
    results.append(f"Grid: 30x30 (X: 0-29, Y: 0-29)")

    # Define edge and center pixels
    edge_mask = (df['X'] == 0) | (df['X'] == 29) | (df['Y'] == 0) | (df['Y'] == 29)
    df['region'] = np.where(edge_mask, 'edge', 'center')

    edge_pixels = df[df['region'] == 'edge']['pixel_id'].nunique()
    center_pixels = df[df['region'] == 'center']['pixel_id'].nunique()
    results.append(f"Edge pixels: {edge_pixels}, Center pixels: {center_pixels}")

    # Compare A1g evolution
    results.append("\n" + "-" * 50)
    results.append("A1g Center Comparison: Edge vs Center")
    results.append("-" * 50)

    edge_data = df[df['region'] == 'edge']
    center_data = df[df['region'] == 'center']

    results.append(f"\nOverall A1g_Center:")
    results.append(f"  Edge:   Mean = {edge_data['A1g_Center'].mean():.2f}, Std = {edge_data['A1g_Center'].std():.2f}")
    results.append(f"  Center: Mean = {center_data['A1g_Center'].mean():.2f}, Std = {center_data['A1g_Center'].std():.2f}")

    # T-test
    t_stat, t_pvalue = stats.ttest_ind(edge_data['A1g_Center'], center_data['A1g_Center'])
    results.append(f"\nT-test (Edge vs Center A1g_Center):")
    results.append(f"  t-statistic = {t_stat:.4f}, p-value = {t_pvalue:.2e}")

    # Compare A1g shift from initial to final
    results.append("\n" + "-" * 50)
    results.append("A1g Shift Analysis (Initial to Final)")
    results.append("-" * 50)

    initial_time = df['time_idx'].min()
    final_time = df['time_idx'].max()

    def calc_shift(group):
        initial = group[group['time_idx'] == initial_time]['A1g_Center'].values
        final = group[group['time_idx'] == final_time]['A1g_Center'].values
        if len(initial) > 0 and len(final) > 0:
            return final[0] - initial[0]
        return np.nan

    pixel_shifts = df.groupby(['pixel_id', 'region']).apply(calc_shift).reset_index()
    pixel_shifts.columns = ['pixel_id', 'region', 'A1g_shift']

    edge_shifts = pixel_shifts[pixel_shifts['region'] == 'edge']['A1g_shift'].dropna()
    center_shifts = pixel_shifts[pixel_shifts['region'] == 'center']['A1g_shift'].dropna()

    results.append(f"\nA1g Shift (Final - Initial):")
    results.append(f"  Edge:   Mean = {edge_shifts.mean():.2f} cm^-1, Std = {edge_shifts.std():.2f}")
    results.append(f"  Center: Mean = {center_shifts.mean():.2f} cm^-1, Std = {center_shifts.std():.2f}")

    t_shift, p_shift = stats.ttest_ind(edge_shifts, center_shifts)
    results.append(f"\nT-test (Edge vs Center shift):")
    results.append(f"  t-statistic = {t_shift:.4f}, p-value = {p_shift:.2e}")

    # Effect size
    pooled_std = np.sqrt((edge_shifts.std()**2 + center_shifts.std()**2) / 2)
    cohens_d = (edge_shifts.mean() - center_shifts.mean()) / pooled_std
    results.append(f"  Cohen's d = {cohens_d:.4f}")

    # Time-resolved comparison
    results.append("\n" + "-" * 50)
    results.append("Time-Resolved A1g Comparison")
    results.append("-" * 50)

    time_comparison = df.groupby(['time_idx', 'region']).agg({
        'A1g_Center': 'mean',
        'Voltage': 'first'
    }).reset_index()

    edge_time = time_comparison[time_comparison['region'] == 'edge']
    center_time = time_comparison[time_comparison['region'] == 'center']

    # Merge and compute difference
    merged = pd.merge(edge_time, center_time, on='time_idx', suffixes=('_edge', '_center'))
    merged['A1g_diff'] = merged['A1g_Center_edge'] - merged['A1g_Center_center']

    results.append(f"Mean A1g difference (Edge - Center) over time: {merged['A1g_diff'].mean():.2f} cm^-1")
    results.append(f"Std of difference: {merged['A1g_diff'].std():.2f} cm^-1")

    # One-sample t-test to check if difference is significantly different from 0
    t_diff, p_diff = stats.ttest_1samp(merged['A1g_diff'], 0)
    results.append(f"\nOne-sample t-test (diff != 0):")
    results.append(f"  t-statistic = {t_diff:.4f}, p-value = {p_diff:.2e}")

    # Compare ID/IG ratio
    results.append("\n" + "-" * 50)
    results.append("ID/IG Ratio Comparison")
    results.append("-" * 50)

    results.append(f"Edge ID/IG:   Mean = {edge_data['ID_IG_Ratio'].mean():.4f}")
    results.append(f"Center ID/IG: Mean = {center_data['ID_IG_Ratio'].mean():.4f}")

    t_idig, p_idig = stats.ttest_ind(edge_data['ID_IG_Ratio'], center_data['ID_IG_Ratio'])
    results.append(f"T-test: t = {t_idig:.4f}, p = {p_idig:.2e}")

    # Conclusion
    results.append("\n" + "=" * 70)
    results.append("CONCLUSION")
    results.append("=" * 70)

    sig_diff_a1g = p_shift < 0.05

    if not sig_diff_a1g:
        verdict = "SUPPORTED"
        explanation = f"No significant difference between edge and center pixels (p={p_shift:.3f}), confirming uniformity."
    else:
        verdict = "REFUTED"
        explanation = f"Significant difference detected between edge and center (p={p_shift:.2e})."

    results.append(f"\nHypothesis H6: {verdict}")
    results.append(explanation)
    results.append(f"Edge-Center A1g shift difference: {edge_shifts.mean() - center_shifts.mean():.2f} cm^-1")

    # Write results
    output_text = "\n".join(results)
    print(output_text)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output_text)

    print(f"\nResults saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
