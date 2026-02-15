"""
Hypothesis H14: Temperature-Dependent A1g Shift Follows Arrhenius Behavior

Test: The rate of A1g peak shift with voltage follows Arrhenius-type temperature
dependence, with activation energy ~0.3 eV.

Expected: NOT VERIFIABLE - No temperature data available.
"""

import pandas as pd
import numpy as np
import os

OUTPUT_DIR = "/Users/carrot/Desktop/POPPER/Battery_Data/hypothesis_test_outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "H14_temperature_results.txt")

def main():
    results = []
    results.append("=" * 70)
    results.append("HYPOTHESIS H14: Temperature-Dependent Arrhenius Behavior")
    results.append("=" * 70)

    # Load data
    data_path = "/Users/carrot/Desktop/POPPER/Battery_Data/raman_peaks_decomposed.csv"
    df = pd.read_csv(data_path)

    results.append("\n" + "-" * 50)
    results.append("Temperature Data Search")
    results.append("-" * 50)

    # Check for temperature columns
    temp_keywords = ['temp', 'temperature', 'T', 'celsius', 'kelvin', 'K', 'C']
    all_columns = list(df.columns)

    results.append(f"\nAll columns in dataset:")
    for col in all_columns:
        results.append(f"  - {col}")

    found_temp_cols = [col for col in all_columns if any(kw.lower() == col.lower() for kw in temp_keywords)]
    results.append(f"\nTemperature-related columns found: {found_temp_cols if found_temp_cols else 'NONE'}")

    results.append("\n" + "-" * 50)
    results.append("Arrhenius Analysis Requirements")
    results.append("-" * 50)

    results.append("\nTo test Arrhenius behavior, we need:")
    results.append("  1. Multiple temperature measurements - NOT AVAILABLE")
    results.append("  2. Rate constants at each temperature - CANNOT CALCULATE")
    results.append("  3. Temperature range (typically 3+ temperatures) - NOT AVAILABLE")
    results.append("  4. ln(k) vs 1/T plot capability - IMPOSSIBLE")

    results.append("\nArrhenius equation: k = A * exp(-Ea/RT)")
    results.append("  where:")
    results.append("    k = rate constant")
    results.append("    A = pre-exponential factor")
    results.append("    Ea = activation energy")
    results.append("    R = gas constant")
    results.append("    T = temperature (Kelvin)")

    results.append("\n" + "-" * 50)
    results.append("Experimental Conditions Assessment")
    results.append("-" * 50)

    # Read experimental setup if available
    try:
        with open("/Users/carrot/Desktop/POPPER/Battery_Data/experimental_setup.md", 'r') as f:
            setup_content = f.read()

        if 'temperature' in setup_content.lower():
            results.append("\nExperimental setup mentions temperature:")
            # Extract relevant lines
            for line in setup_content.split('\n'):
                if 'temperature' in line.lower() or 'ambient' in line.lower() or 'room' in line.lower():
                    results.append(f"  {line.strip()}")
        else:
            results.append("\nNo temperature information in experimental setup.")
            results.append("Assumed to be room temperature (~25°C) throughout.")
    except:
        results.append("\nCould not read experimental setup file.")
        results.append("Temperature conditions unknown.")

    results.append("\n" + "-" * 50)
    results.append("What We Can Analyze (Without Temperature)")
    results.append("-" * 50)

    # Show A1g shift rate at constant (unknown) temperature
    time_avg = df.groupby('time_idx').agg({
        'A1g_Center': 'mean',
        'Voltage': 'first',
        'Time_Min': 'first'
    }).reset_index().sort_values('Time_Min')

    a1g_shift_rate = (time_avg['A1g_Center'].iloc[-1] - time_avg['A1g_Center'].iloc[0]) / \
                     (time_avg['Time_Min'].iloc[-1] - time_avg['Time_Min'].iloc[0])

    results.append(f"\nA1g shift rate (at constant T): {a1g_shift_rate:.4f} cm^-1/min")
    results.append("This represents a SINGLE temperature point.")
    results.append("Arrhenius analysis requires MULTIPLE temperatures.")

    # Conclusion
    results.append("\n" + "=" * 70)
    results.append("CONCLUSION")
    results.append("=" * 70)

    verdict = "NOT SUPPORTED (DATA INSUFFICIENT)"

    results.append(f"\nHypothesis H14: {verdict}")
    results.append("\nReason: No temperature variation data is available.")
    results.append("The experiment was conducted at a single (likely ambient)")
    results.append("temperature. Arrhenius analysis requires measurements at")
    results.append("multiple temperatures to extract activation energy.")
    results.append("\nMissing data:")
    results.append("  - Temperature measurements during experiment")
    results.append("  - Data at multiple controlled temperatures")
    results.append("  - Rate constants at each temperature")
    results.append("  - Minimum 3 temperature points for reliable Ea extraction")

    # Write results
    output_text = "\n".join(results)
    print(output_text)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output_text)

    print(f"\nResults saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
