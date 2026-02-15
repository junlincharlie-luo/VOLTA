"""
Hypothesis H5: Cathode and Carbon Raman Signatures Are Spatially Decoupled

Test: The A1g peak position (cathode structural indicator) and ID/IG ratio (carbon
disorder indicator) show weak or no spatial correlation, indicating that local
cathode delithiation and carbon network properties evolve independently.
"""

import pandas as pd
import numpy as np
from scipy import stats
import os

# Output file
OUTPUT_DIR = "/Users/carrot/Desktop/VOLTA/Battery_Data/hypothesis_test_outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "H5_spatial_A1g_ID_IG_correlation_results.txt")

def main():
    results = []
    results.append("=" * 70)
    results.append("HYPOTHESIS H5: Cathode-Carbon Spatial Decoupling")
    results.append("=" * 70)

    # Load data
    data_path = "/Users/carrot/Desktop/VOLTA/Battery_Data/raman_peaks_decomposed.csv"
    df = pd.read_csv(data_path)

    results.append(f"\nDataset loaded: {len(df)} rows")
    results.append(f"Unique pixels: {df['pixel_id'].nunique()}")
    results.append(f"Time steps: {df['time_idx'].nunique()}")

    # Method 1: Correlation at each time step
    results.append("\n" + "-" * 50)
    results.append("METHOD 1: Spatial Correlation at Each Time Step")
    results.append("-" * 50)

    correlations_per_time = []
    for t in df['time_idx'].unique():
        subset = df[df['time_idx'] == t]
        r, p = stats.pearsonr(subset['A1g_Center'], subset['ID_IG_Ratio'])
        voltage = subset['Voltage'].iloc[0]
        correlations_per_time.append({
            'time_idx': t,
            'pearson_r': r,
            'p_value': p,
            'Voltage': voltage
        })

    corr_df = pd.DataFrame(correlations_per_time)

    results.append(f"\nSummary of spatial correlations across {len(corr_df)} time steps:")
    results.append(f"  Mean Pearson r: {corr_df['pearson_r'].mean():.4f}")
    results.append(f"  Std Pearson r:  {corr_df['pearson_r'].std():.4f}")
    results.append(f"  Min r: {corr_df['pearson_r'].min():.4f}")
    results.append(f"  Max r: {corr_df['pearson_r'].max():.4f}")

    sig_positive = (corr_df['pearson_r'] > 0) & (corr_df['p_value'] < 0.05)
    sig_negative = (corr_df['pearson_r'] < 0) & (corr_df['p_value'] < 0.05)
    results.append(f"\n  Time steps with significant positive correlation: {sig_positive.sum()}")
    results.append(f"  Time steps with significant negative correlation: {sig_negative.sum()}")
    results.append(f"  Time steps with no significant correlation: {len(corr_df) - sig_positive.sum() - sig_negative.sum()}")

    # Method 2: Per-pixel analysis across time
    results.append("\n" + "-" * 50)
    results.append("METHOD 2: Per-Pixel A1g Shift vs ID/IG Change")
    results.append("-" * 50)

    # Calculate shift for each pixel from initial to final time
    initial_time = df['time_idx'].min()
    final_time = df['time_idx'].max()

    initial_data = df[df['time_idx'] == initial_time][['pixel_id', 'A1g_Center', 'ID_IG_Ratio', 'X', 'Y']]
    final_data = df[df['time_idx'] == final_time][['pixel_id', 'A1g_Center', 'ID_IG_Ratio']]

    initial_data.columns = ['pixel_id', 'A1g_initial', 'ID_IG_initial', 'X', 'Y']
    final_data.columns = ['pixel_id', 'A1g_final', 'ID_IG_final']

    pixel_changes = pd.merge(initial_data, final_data, on='pixel_id')
    pixel_changes['A1g_shift'] = pixel_changes['A1g_final'] - pixel_changes['A1g_initial']
    pixel_changes['ID_IG_change'] = pixel_changes['ID_IG_final'] - pixel_changes['ID_IG_initial']

    results.append(f"\nA1g shift statistics:")
    results.append(f"  Mean: {pixel_changes['A1g_shift'].mean():.2f} cm^-1")
    results.append(f"  Std:  {pixel_changes['A1g_shift'].std():.2f} cm^-1")
    results.append(f"  Range: {pixel_changes['A1g_shift'].min():.2f} to {pixel_changes['A1g_shift'].max():.2f}")

    results.append(f"\nID/IG change statistics:")
    results.append(f"  Mean: {pixel_changes['ID_IG_change'].mean():.4f}")
    results.append(f"  Std:  {pixel_changes['ID_IG_change'].std():.4f}")

    # Correlation between shift and change
    shift_corr_r, shift_corr_p = stats.pearsonr(pixel_changes['A1g_shift'], pixel_changes['ID_IG_change'])
    shift_spearman, shift_sp_p = stats.spearmanr(pixel_changes['A1g_shift'], pixel_changes['ID_IG_change'])

    results.append(f"\nCorrelation (A1g_shift vs ID/IG_change):")
    results.append(f"  Pearson:  r = {shift_corr_r:.4f}, p = {shift_corr_p:.2e}")
    results.append(f"  Spearman: rho = {shift_spearman:.4f}, p = {shift_sp_p:.2e}")

    # Method 3: Instantaneous correlation (all data pooled)
    results.append("\n" + "-" * 50)
    results.append("METHOD 3: Overall Correlation (All Data)")
    results.append("-" * 50)

    overall_r, overall_p = stats.pearsonr(df['A1g_Center'], df['ID_IG_Ratio'])
    overall_spearman, overall_sp = stats.spearmanr(df['A1g_Center'], df['ID_IG_Ratio'])

    results.append(f"Pearson (all data):  r = {overall_r:.4f}, p = {overall_p:.2e}")
    results.append(f"Spearman (all data): rho = {overall_spearman:.4f}, p = {overall_sp:.2e}")

    # Method 4: Correlation at different voltage levels
    results.append("\n" + "-" * 50)
    results.append("METHOD 4: Correlation at Different Voltage Levels")
    results.append("-" * 50)

    voltage_bins = [3.0, 3.5, 4.0, 4.3, 4.5, 5.0]
    df['V_bin'] = pd.cut(df['Voltage'], bins=voltage_bins)

    for vbin in sorted(df['V_bin'].dropna().unique()):
        subset = df[df['V_bin'] == vbin]
        r, p = stats.pearsonr(subset['A1g_Center'], subset['ID_IG_Ratio'])
        results.append(f"  {vbin}: r = {r:.4f}, p = {p:.2e}, n = {len(subset)}")

    # Trend in correlation strength
    results.append("\n" + "-" * 50)
    results.append("Does Correlation Strength Change with Voltage?")
    results.append("-" * 50)

    corr_vs_voltage_r, corr_vs_voltage_p = stats.pearsonr(
        corr_df['Voltage'], corr_df['pearson_r'].abs()
    )
    results.append(f"Correlation between |r| and Voltage: r = {corr_vs_voltage_r:.4f}, p = {corr_vs_voltage_p:.2e}")

    # Conclusion
    results.append("\n" + "=" * 70)
    results.append("CONCLUSION")
    results.append("=" * 70)

    mean_corr = corr_df['pearson_r'].mean()
    no_sig_count = len(corr_df) - sig_positive.sum() - sig_negative.sum()

    if abs(mean_corr) < 0.1 and no_sig_count > len(corr_df) * 0.5:
        verdict = "SUPPORTED"
        explanation = f"Weak/no spatial correlation (mean |r|={abs(mean_corr):.3f}), confirming decoupled behavior."
    elif abs(mean_corr) < 0.2:
        verdict = "PARTIALLY SUPPORTED"
        explanation = f"Generally weak correlations (mean r={mean_corr:.3f}), suggesting mostly decoupled behavior."
    elif abs(mean_corr) > 0.3:
        verdict = "REFUTED"
        explanation = f"Strong spatial correlation observed (mean r={mean_corr:.3f}), indicating coupled behavior."
    else:
        verdict = "INCONCLUSIVE"
        explanation = f"Moderate correlations (mean r={mean_corr:.3f})."

    results.append(f"\nHypothesis H5: {verdict}")
    results.append(explanation)
    results.append(f"Time steps with no significant correlation: {no_sig_count}/{len(corr_df)} ({no_sig_count/len(corr_df)*100:.1f}%)")

    # Write results
    output_text = "\n".join(results)
    print(output_text)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output_text)

    print(f"\nResults saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
