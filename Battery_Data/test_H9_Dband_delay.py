"""
Hypothesis H9: D-band Amplitude Shows Time-Delayed Response to Voltage Changes

Test: Changes in D-band amplitude (D_Amp) lag behind voltage changes by at least
one measurement interval (15 min), suggesting SEI formation is a kinetically slow process.
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy import signal
import os

OUTPUT_DIR = "/Users/carrot/Desktop/VOLTA/Battery_Data/hypothesis_test_outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "H9_Dband_delay_results.txt")

def main():
    results = []
    results.append("=" * 70)
    results.append("HYPOTHESIS H9: D-band Amplitude Time-Delay Response")
    results.append("=" * 70)

    # Load data
    data_path = "/Users/carrot/Desktop/VOLTA/Battery_Data/raman_peaks_decomposed.csv"
    df = pd.read_csv(data_path)

    results.append(f"\nDataset loaded: {len(df)} rows")
    results.append(f"Time interval: ~15 minutes between measurements")

    # Time-averaged D_Amp and Voltage
    time_avg = df.groupby('time_idx').agg({
        'D_Amp': 'mean',
        'Voltage': 'first',
        'Time_Min': 'first'
    }).reset_index().sort_values('time_idx')

    results.append(f"Time steps: {len(time_avg)}")

    # Compute derivatives (rate of change)
    results.append("\n" + "-" * 50)
    results.append("Rate of Change Analysis")
    results.append("-" * 50)

    voltage_diff = np.diff(time_avg['Voltage'].values)
    damp_diff = np.diff(time_avg['D_Amp'].values)

    results.append(f"Mean voltage change rate: {voltage_diff.mean():.4f} V/step")
    results.append(f"Mean D_Amp change rate: {damp_diff.mean():.4f} /step")

    # Cross-correlation analysis
    results.append("\n" + "-" * 50)
    results.append("Cross-Correlation Analysis")
    results.append("-" * 50)

    # Normalize the signals
    voltage_norm = (time_avg['Voltage'] - time_avg['Voltage'].mean()) / time_avg['Voltage'].std()
    damp_norm = (time_avg['D_Amp'] - time_avg['D_Amp'].mean()) / time_avg['D_Amp'].std()

    # Compute cross-correlation
    max_lag = 20  # Check up to 20 time steps (5 hours)
    correlations = []
    for lag in range(-max_lag, max_lag + 1):
        if lag < 0:
            corr = np.corrcoef(voltage_norm[:lag].values, damp_norm[-lag:].values)[0, 1]
        elif lag > 0:
            corr = np.corrcoef(voltage_norm[lag:].values, damp_norm[:-lag].values)[0, 1]
        else:
            corr = np.corrcoef(voltage_norm.values, damp_norm.values)[0, 1]
        correlations.append({'lag': lag, 'correlation': corr})

    corr_df = pd.DataFrame(correlations)

    # Find max correlation and its lag
    max_corr_idx = corr_df['correlation'].abs().idxmax()
    max_corr_lag = corr_df.loc[max_corr_idx, 'lag']
    max_corr_value = corr_df.loc[max_corr_idx, 'correlation']

    zero_lag_corr = corr_df[corr_df['lag'] == 0]['correlation'].values[0]

    results.append(f"Zero-lag correlation: r = {zero_lag_corr:.4f}")
    results.append(f"Maximum correlation: r = {max_corr_value:.4f} at lag = {max_corr_lag} steps")
    results.append(f"  (Positive lag = D_Amp lags behind Voltage)")

    # Show correlations around peak
    results.append("\nCorrelations at different lags:")
    for lag in [-5, -3, -1, 0, 1, 3, 5, 10]:
        if lag in corr_df['lag'].values:
            c = corr_df[corr_df['lag'] == lag]['correlation'].values[0]
            results.append(f"  Lag {lag:+3d} steps: r = {c:.4f}")

    # Direct correlation at different lags
    results.append("\n" + "-" * 50)
    results.append("Lagged Correlation Test")
    results.append("-" * 50)

    # Test: Does D_Amp at time t correlate better with Voltage at time t-1 than t?
    if len(time_avg) > 5:
        # Lag 0
        r0, p0 = stats.pearsonr(time_avg['Voltage'].values[1:], time_avg['D_Amp'].values[1:])
        # Lag 1 (D_Amp lags voltage by 1 step)
        r1, p1 = stats.pearsonr(time_avg['Voltage'].values[:-1], time_avg['D_Amp'].values[1:])
        # Lag 2
        r2, p2 = stats.pearsonr(time_avg['Voltage'].values[:-2], time_avg['D_Amp'].values[2:])

        results.append(f"Correlation D_Amp(t) vs Voltage(t):   r = {r0:.4f}, p = {p0:.2e}")
        results.append(f"Correlation D_Amp(t) vs Voltage(t-1): r = {r1:.4f}, p = {p1:.2e}")
        results.append(f"Correlation D_Amp(t) vs Voltage(t-2): r = {r2:.4f}, p = {p2:.2e}")

        # Check if lagged correlation is stronger
        lag_improvement = abs(r1) - abs(r0)
        results.append(f"\nLag-1 improvement: {lag_improvement:.4f}")

    # Phase analysis using derivatives
    results.append("\n" + "-" * 50)
    results.append("Derivative Cross-Correlation")
    results.append("-" * 50)

    # Cross-correlation of derivatives
    if len(voltage_diff) > 10:
        deriv_corr_0 = np.corrcoef(voltage_diff, damp_diff)[0, 1]
        deriv_corr_1 = np.corrcoef(voltage_diff[:-1], damp_diff[1:])[0, 1]
        deriv_corr_2 = np.corrcoef(voltage_diff[:-2], damp_diff[2:])[0, 1]

        results.append(f"dD_Amp/dt vs dV/dt (lag 0): r = {deriv_corr_0:.4f}")
        results.append(f"dD_Amp/dt vs dV/dt (lag 1): r = {deriv_corr_1:.4f}")
        results.append(f"dD_Amp/dt vs dV/dt (lag 2): r = {deriv_corr_2:.4f}")

    # Conclusion
    results.append("\n" + "=" * 70)
    results.append("CONCLUSION")
    results.append("=" * 70)

    # Check if there's evidence of lag
    has_lag = max_corr_lag > 0 and abs(max_corr_value) > abs(zero_lag_corr) * 1.05

    if has_lag and max_corr_lag >= 1:
        verdict = "SUPPORTED"
        explanation = f"D_Amp shows delayed response: max correlation at lag = {max_corr_lag} steps ({max_corr_lag * 15} min)."
    elif max_corr_lag > 0:
        verdict = "PARTIALLY SUPPORTED"
        explanation = f"Some evidence of delay (max corr at lag {max_corr_lag}), but improvement is marginal."
    else:
        verdict = "REFUTED"
        explanation = f"No time delay detected. Best correlation at lag = {max_corr_lag} steps."

    results.append(f"\nHypothesis H9: {verdict}")
    results.append(explanation)
    results.append(f"Zero-lag correlation: {zero_lag_corr:.4f}")
    results.append(f"Max correlation: {max_corr_value:.4f} at lag {max_corr_lag}")

    # Write results
    output_text = "\n".join(results)
    print(output_text)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output_text)

    print(f"\nResults saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
