"""
Hypothesis H4: Eg Peak Amplitude Increases with Charging

Test: The Eg peak amplitude (related to M-O bending in layered structure) increases
during charging, reflecting enhanced Raman scattering from M-O bending modes as
lithium extraction modifies the electronic structure and optical transparency.
"""

import pandas as pd
import numpy as np
from scipy import stats
import os

# Output file
OUTPUT_DIR = "/Users/carrot/Desktop/POPPER/Battery_Data/hypothesis_test_outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "H4_Eg_amplitude_results.txt")

def main():
    results = []
    results.append("=" * 70)
    results.append("HYPOTHESIS H4: Eg Peak Amplitude Increases with Charging")
    results.append("=" * 70)

    # Load data
    data_path = "/Users/carrot/Desktop/POPPER/Battery_Data/raman_peaks_decomposed.csv"
    df = pd.read_csv(data_path)

    results.append(f"\nDataset loaded: {len(df)} rows")
    results.append(f"Voltage range: {df['Voltage'].min():.3f}V to {df['Voltage'].max():.3f}V")
    results.append(f"Eg_Amp range: {df['Eg_Amp'].min():.3f} to {df['Eg_Amp'].max():.3f}")

    # Overall correlation
    results.append("\n" + "-" * 50)
    results.append("Overall Correlation: Eg_Amp vs Voltage")
    results.append("-" * 50)

    pearson_r, pearson_p = stats.pearsonr(df['Voltage'], df['Eg_Amp'])
    spearman_r, spearman_p = stats.spearmanr(df['Voltage'], df['Eg_Amp'])

    results.append(f"Pearson:  r = {pearson_r:.4f}, p = {pearson_p:.2e}")
    results.append(f"Spearman: rho = {spearman_r:.4f}, p = {spearman_p:.2e}")

    # Time-averaged analysis
    results.append("\n" + "-" * 50)
    results.append("Time-Averaged Eg_Amp Evolution")
    results.append("-" * 50)

    time_avg = df.groupby('time_idx').agg({
        'Eg_Amp': ['mean', 'std', 'median'],
        'Voltage': 'first',
        'Time_Min': 'first'
    }).reset_index()
    time_avg.columns = ['time_idx', 'Eg_mean', 'Eg_std', 'Eg_median', 'Voltage', 'Time_Min']

    initial = time_avg[time_avg['time_idx'] == 0].iloc[0]
    final = time_avg[time_avg['time_idx'] == time_avg['time_idx'].max()].iloc[0]

    results.append(f"\nInitial state (V = {initial['Voltage']:.3f}V):")
    results.append(f"  Mean Eg_Amp = {initial['Eg_mean']:.4f}")
    results.append(f"  Std = {initial['Eg_std']:.4f}")

    results.append(f"\nFinal state (V = {final['Voltage']:.3f}V):")
    results.append(f"  Mean Eg_Amp = {final['Eg_mean']:.4f}")
    results.append(f"  Std = {final['Eg_std']:.4f}")

    amp_change = final['Eg_mean'] - initial['Eg_mean']
    amp_change_pct = amp_change / initial['Eg_mean'] * 100
    results.append(f"\nChange: {amp_change:.4f} ({amp_change_pct:+.2f}%)")

    # Time-averaged correlation
    results.append("\n" + "-" * 50)
    results.append("Time-Averaged Correlation")
    results.append("-" * 50)

    pearson_avg, p_avg = stats.pearsonr(time_avg['Voltage'], time_avg['Eg_mean'])
    spearman_avg, sp_avg = stats.spearmanr(time_avg['Voltage'], time_avg['Eg_mean'])

    results.append(f"Pearson (time-averaged):  r = {pearson_avg:.4f}, p = {p_avg:.2e}")
    results.append(f"Spearman (time-averaged): rho = {spearman_avg:.4f}, p = {sp_avg:.2e}")

    # Linear regression
    results.append("\n" + "-" * 50)
    results.append("Linear Regression: Eg_Amp vs Voltage")
    results.append("-" * 50)

    slope, intercept, r_value, p_value, std_err = stats.linregress(
        time_avg['Voltage'], time_avg['Eg_mean']
    )

    results.append(f"Slope: {slope:.4f} per Volt")
    results.append(f"Intercept: {intercept:.4f}")
    results.append(f"R-squared: {r_value**2:.4f}")
    results.append(f"P-value: {p_value:.2e}")

    # Voltage bin analysis
    results.append("\n" + "-" * 50)
    results.append("Voltage Bin Analysis")
    results.append("-" * 50)

    bins = [3.0, 3.5, 4.0, 4.3, 4.5, 5.0]
    df['V_bin'] = pd.cut(df['Voltage'], bins=bins)

    for vbin in sorted(df['V_bin'].dropna().unique()):
        subset = df[df['V_bin'] == vbin]['Eg_Amp']
        results.append(f"  {vbin}: Mean = {subset.mean():.4f}, Std = {subset.std():.4f}")

    # Monotonicity check
    results.append("\n" + "-" * 50)
    results.append("Monotonicity Analysis")
    results.append("-" * 50)

    sorted_by_voltage = time_avg.sort_values('Voltage')
    eg_diffs = np.diff(sorted_by_voltage['Eg_mean'].values)
    negative_changes = np.sum(eg_diffs < 0)
    total_changes = len(eg_diffs)

    results.append(f"Negative changes (decreasing): {negative_changes}/{total_changes}")
    results.append(f"Monotonicity ratio: {negative_changes/total_changes:.2%}")

    # Conclusion
    results.append("\n" + "=" * 70)
    results.append("CONCLUSION")
    results.append("=" * 70)

    # For H4, we expect POSITIVE correlation (amplitude increases with voltage)
    if pearson_avg > 0.2 and p_avg < 0.05:
        verdict = "SUPPORTED"
        explanation = f"Positive correlation (r={pearson_avg:.3f}): Eg amplitude increases with charging."
    elif pearson_avg > 0 and p_avg < 0.05:
        verdict = "PARTIALLY SUPPORTED"
        explanation = f"Weak but significant positive correlation (r={pearson_avg:.3f})."
    elif pearson_avg < 0 and p_avg < 0.05:
        verdict = "REFUTED"
        explanation = f"Eg amplitude actually DECREASES with voltage (r={pearson_avg:.3f})."
    else:
        verdict = "INCONCLUSIVE"
        explanation = f"No significant trend found (p={p_avg:.3f})."

    results.append(f"\nHypothesis H4: {verdict}")
    results.append(explanation)
    results.append(f"Eg amplitude changed by {amp_change_pct:+.2f}% during charging.")

    # Write results
    output_text = "\n".join(results)
    print(output_text)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output_text)

    print(f"\nResults saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
