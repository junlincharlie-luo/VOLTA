"""
Hypothesis H10: Neighboring Pixels Show Correlated A1g Behavior (Spatial Autocorrelation)

Test: The A1g_Center values of spatially adjacent pixels are more correlated than
distant pixels, indicating local electrochemical domains larger than 1 um.
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.spatial.distance import pdist, squareform
import os

OUTPUT_DIR = "/Users/carrot/Desktop/POPPER/Battery_Data/hypothesis_test_outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "H10_spatial_autocorrelation_results.txt")

def compute_morans_i(values, coords):
    """Compute Moran's I spatial autocorrelation statistic."""
    n = len(values)
    if n < 3:
        return np.nan, np.nan

    # Compute distance matrix
    dist_matrix = squareform(pdist(coords))

    # Create adjacency weight matrix (inverse distance, with cutoff)
    # Use neighbors within sqrt(2) distance (adjacent including diagonal)
    W = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j and dist_matrix[i, j] <= np.sqrt(2) + 0.01:  # Adjacent pixels
                W[i, j] = 1.0

    # Row-standardize
    row_sums = W.sum(axis=1)
    row_sums[row_sums == 0] = 1  # Avoid division by zero
    W = W / row_sums[:, np.newaxis]

    # Compute Moran's I
    z = values - values.mean()
    numerator = np.sum(W * np.outer(z, z))
    denominator = np.sum(z ** 2)

    if denominator == 0:
        return np.nan, np.nan

    I = (n / W.sum()) * (numerator / denominator)

    # Expected value under null hypothesis
    E_I = -1 / (n - 1)

    return I, E_I

def main():
    results = []
    results.append("=" * 70)
    results.append("HYPOTHESIS H10: Spatial Autocorrelation of A1g")
    results.append("=" * 70)

    # Load data
    data_path = "/Users/carrot/Desktop/POPPER/Battery_Data/raman_peaks_decomposed.csv"
    df = pd.read_csv(data_path)

    results.append(f"\nDataset loaded: {len(df)} rows")
    results.append(f"Grid: 30x30 = 900 pixels")
    results.append(f"Time steps: {df['time_idx'].nunique()}")

    # Compute correlation by distance
    results.append("\n" + "-" * 50)
    results.append("Correlation by Pixel Distance")
    results.append("-" * 50)

    # Select a few representative time points
    time_points = [0, 30, 60, 90, 113]  # Initial, middle, and final

    distance_correlations = []

    for t in time_points:
        t_data = df[df['time_idx'] == t][['X', 'Y', 'A1g_Center', 'pixel_id']].copy()

        if len(t_data) < 100:
            continue

        # Compute pairwise distances and value differences
        for _, row1 in t_data.iterrows():
            for _, row2 in t_data.iterrows():
                if row1['pixel_id'] >= row2['pixel_id']:
                    continue
                dist = np.sqrt((row1['X'] - row2['X'])**2 + (row1['Y'] - row2['Y'])**2)
                distance_correlations.append({
                    'time_idx': t,
                    'distance': dist,
                    'value_diff': abs(row1['A1g_Center'] - row2['A1g_Center'])
                })

    dist_df = pd.DataFrame(distance_correlations)

    # Bin by distance
    dist_bins = [0, 1.5, 3, 5, 10, 15, 20, 30, 50]
    dist_df['dist_bin'] = pd.cut(dist_df['distance'], bins=dist_bins)

    results.append("\nMean |A1g difference| by pixel distance:")
    for dbin in sorted(dist_df['dist_bin'].dropna().unique()):
        subset = dist_df[dist_df['dist_bin'] == dbin]
        results.append(f"  Distance {dbin}: Mean diff = {subset['value_diff'].mean():.2f} cm^-1, N = {len(subset)}")

    # Correlation: distance vs value difference
    r_dist, p_dist = stats.pearsonr(dist_df['distance'], dist_df['value_diff'])
    results.append(f"\nCorrelation (distance vs |diff|): r = {r_dist:.4f}, p = {p_dist:.2e}")

    # Compute Moran's I for several time points
    results.append("\n" + "-" * 50)
    results.append("Moran's I Spatial Autocorrelation")
    results.append("-" * 50)

    morans_results = []
    for t in range(0, 114, 10):  # Every 10th time point
        t_data = df[df['time_idx'] == t][['X', 'Y', 'A1g_Center']].copy()
        if len(t_data) == 900:  # Full grid
            coords = t_data[['X', 'Y']].values
            values = t_data['A1g_Center'].values
            I, E_I = compute_morans_i(values, coords)
            voltage = df[df['time_idx'] == t]['Voltage'].iloc[0]
            morans_results.append({
                'time_idx': t,
                'Voltage': voltage,
                'Morans_I': I,
                'Expected_I': E_I
            })
            results.append(f"  t={t:3d} (V={voltage:.2f}V): Moran's I = {I:.4f} (Expected: {E_I:.4f})")

    morans_df = pd.DataFrame(morans_results)

    mean_morans_I = morans_df['Morans_I'].mean()
    results.append(f"\nMean Moran's I: {mean_morans_I:.4f}")
    results.append(f"(Positive values indicate positive spatial autocorrelation)")

    # Adjacent vs non-adjacent pixel correlation
    results.append("\n" + "-" * 50)
    results.append("Adjacent vs Non-Adjacent Pixel Comparison")
    results.append("-" * 50)

    # For time 0
    t0_data = df[df['time_idx'] == 0][['X', 'Y', 'A1g_Center', 'pixel_id']]

    adjacent_diffs = []
    nonadjacent_diffs = []

    for _, row1 in t0_data.iterrows():
        for _, row2 in t0_data.iterrows():
            if row1['pixel_id'] >= row2['pixel_id']:
                continue
            dist = np.sqrt((row1['X'] - row2['X'])**2 + (row1['Y'] - row2['Y'])**2)
            diff = abs(row1['A1g_Center'] - row2['A1g_Center'])
            if dist <= np.sqrt(2) + 0.01:  # Adjacent (including diagonal)
                adjacent_diffs.append(diff)
            elif dist > 10:  # Far apart
                nonadjacent_diffs.append(diff)

    adj_mean = np.mean(adjacent_diffs)
    nonadj_mean = np.mean(nonadjacent_diffs[:len(adjacent_diffs)])  # Sample same size

    results.append(f"Adjacent pixels mean |diff|:     {adj_mean:.2f} cm^-1 (N={len(adjacent_diffs)})")
    results.append(f"Non-adjacent pixels mean |diff|: {nonadj_mean:.2f} cm^-1")

    t_adj, p_adj = stats.ttest_ind(adjacent_diffs, nonadjacent_diffs[:len(adjacent_diffs)])
    results.append(f"T-test: t = {t_adj:.4f}, p = {p_adj:.2e}")

    # Conclusion
    results.append("\n" + "=" * 70)
    results.append("CONCLUSION")
    results.append("=" * 70)

    # Criteria: Moran's I > 0 and adjacent pixels more similar than distant
    has_autocorr = mean_morans_I > 0 and adj_mean < nonadj_mean

    if has_autocorr and mean_morans_I > 0.1:
        verdict = "SUPPORTED"
        explanation = f"Positive spatial autocorrelation (Moran's I = {mean_morans_I:.3f}), adjacent pixels are more similar."
    elif has_autocorr:
        verdict = "PARTIALLY SUPPORTED"
        explanation = f"Weak positive autocorrelation (Moran's I = {mean_morans_I:.3f})."
    else:
        verdict = "REFUTED"
        explanation = f"No evidence of spatial autocorrelation (Moran's I = {mean_morans_I:.3f})."

    results.append(f"\nHypothesis H10: {verdict}")
    results.append(explanation)
    results.append(f"Adjacent vs distant difference: {nonadj_mean - adj_mean:.2f} cm^-1")

    # Write results
    output_text = "\n".join(results)
    print(output_text)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output_text)

    print(f"\nResults saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
