"""
Battery Hypothesis Testing with POPPER

This script loads battery experiment data (Raman spectroscopy and voltage profiles)
and uses the POPPER agentic workflow to test the hypothesis:

"The cathode A_{1g} peak (~590 cm^{-1}) shifts to higher wavenumbers during charging
and reversibly returns during discharging, showing a linear correlation with the
voltage profile."

The data comes from Operando Raman Spectroscopy analysis of Li-rich layered oxide cathodes.
"""

import os
import sys
import pandas as pd
import numpy as np
from typing import Dict, Optional

# Add POPPER to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class BatteryDataLoader:
    """
    Custom data loader for battery experiment data.
    Loads Raman peak decomposition data and voltage profile data.
    """

    def __init__(self, data_folder: str, random_seed: int = 42):
        """
        Initialize the battery data loader.

        Args:
            data_folder: Path to the Battery_Data folder containing CSV files
            random_seed: Random seed for any permutation operations
        """
        self.data_path = data_folder
        self.random_seed = random_seed
        self.table_dict = {}
        self._load_battery_data()
        self.data_desc = self._generate_data_description()

    def _load_battery_data(self):
        """Load the battery experiment CSV files."""
        # Load Raman peaks decomposed data
        raman_path = os.path.join(self.data_path, "raman_peaks_decomposed.csv")
        if os.path.exists(raman_path):
            self.table_dict["df_raman_peaks"] = pd.read_csv(raman_path)
            print(f"Loaded Raman peaks data: {len(self.table_dict['df_raman_peaks'])} rows")
        else:
            raise FileNotFoundError(f"Raman peaks file not found: {raman_path}")

        # Load voltage profile data
        voltage_path = os.path.join(self.data_path, "voltage_profile_detailed.csv")
        if os.path.exists(voltage_path):
            self.table_dict["df_voltage_profile"] = pd.read_csv(voltage_path)
            print(f"Loaded voltage profile data: {len(self.table_dict['df_voltage_profile'])} rows")
        else:
            raise FileNotFoundError(f"Voltage profile file not found: {voltage_path}")

    def _generate_data_description(self) -> str:
        """Generate a description of the battery datasets."""
        desc = """
=== Battery Experiment Data Description ===

This dataset contains Operando Raman Spectroscopy data from Li-rich layered oxide cathode cycling.

"""
        for name, df in self.table_dict.items():
            if df is not None:
                desc += f"**{name}**:\n"
                desc += f"Columns: {df.columns.tolist()}\n"
                desc += f"Shape: {df.shape}\n"
                desc += f"Sample row: {dict(zip(df.columns, df.iloc[0]))}\n\n"

                # Add column descriptions for key columns
                if name == "df_raman_peaks":
                    desc += """
Column Descriptions for df_raman_peaks:
- pixel_id: Spatial pixel identifier (0-899 for 30x30 grid)
- time_idx: Time step index (0-113, each step is 15 minutes)
- Eg_Center: E_g peak position in cm^{-1} (~475 cm^{-1}, M-O bending)
- Eg_Amp: E_g peak amplitude
- Eg_Sigma: E_g peak width
- A1g_Center: A_{1g} peak position in cm^{-1} (~590 cm^{-1}, M-O stretching, PRIMARY SOC INDICATOR)
- A1g_Amp: A_{1g} peak amplitude
- A1g_Sigma: A_{1g} peak width
- D_Center: D-band center (~1350 cm^{-1}, disordered carbon)
- D_Amp: D-band amplitude
- D_Sigma: D-band width
- G_Center: G-band center (~1585 cm^{-1}, graphitic carbon)
- G_Amp: G-band amplitude
- G_Sigma: G-band width
- ID_IG_Ratio: Ratio of D-band to G-band intensity (carbon disorder indicator)
- X, Y: Spatial coordinates on the 30x30 um grid
- Time_Min: Time in minutes from start
- Voltage: Corresponding cell voltage (V vs Li/Li+)

"""
                elif name == "df_voltage_profile":
                    desc += """
Column Descriptions for df_voltage_profile:
- time/h: Time in hours from start of experiment
- Ewe/V: Working electrode voltage (V vs Li/Li+)
  - Charging: Voltage increases from ~3.0V to ~4.7V (delithiation)
  - Discharging: Voltage decreases from ~4.7V to ~3.0V (lithiation)

"""
        return desc

    def get_data(self, table_name: str) -> Optional[pd.DataFrame]:
        """Return the requested DataFrame."""
        return self.table_dict.get(table_name, None)

    def load_into_globals(self):
        """Load each dataset into the global namespace."""
        for name, df in self.table_dict.items():
            if df is not None:
                globals()[name] = df

    def display_data_description(self):
        """Print the data description."""
        print(self.data_desc)

    def permute_selected_columns(self, random_seed: int = 42):
        """Permute columns for null hypothesis testing."""
        np.random.seed(random_seed)
        for df_name in self.table_dict:
            df = self.table_dict[df_name]
            self.table_dict[df_name] = df.apply(np.random.permutation)


def run_battery_hypothesis_test(
    llm: str = "claude-sonnet-4-20250514",
    alpha: float = 0.1,
    max_num_of_tests: int = 5,
    max_retry: int = 5,
    time_limit: int = 5,
    use_react_agent: bool = True,
    relevance_checker: bool = True,
    api_key: Optional[str] = None
) -> Dict:
    """
    Run the POPPER hypothesis testing workflow on the battery data.

    Args:
        llm: LLM model to use for the agents
        alpha: Significance level for hypothesis testing
        max_num_of_tests: Maximum number of falsification tests
        max_retry: Maximum retries for failed tests
        time_limit: Time limit in minutes for each test
        use_react_agent: Whether to use ReAct agent
        relevance_checker: Whether to use relevance checker
        api_key: Optional API key for the LLM

    Returns:
        Dictionary containing test results
    """
    # Import POPPER modules here to avoid import errors during quick analysis
    from popper.popper import Popper
    from popper.agent import SequentialFalsificationTest

    # Get the path to Battery_Data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    battery_data_path = os.path.join(script_dir, "Battery_Data")

    if not os.path.exists(battery_data_path):
        raise FileNotFoundError(f"Battery_Data folder not found at: {battery_data_path}")

    print("=" * 60)
    print("Battery Hypothesis Testing with POPPER")
    print("=" * 60)

    # Load battery data
    print("\nLoading battery experiment data...")
    data_loader = BatteryDataLoader(battery_data_path)
    data_loader.display_data_description()

    # Define the hypothesis to test
    hypothesis = """
    The cathode A_{1g} peak (~590 cm^{-1}) shifts to higher wavenumbers during charging
    and reversibly returns during discharging, showing a linear correlation with the
    voltage profile.

    Specifically:
    1. During charging (voltage increase from 3.0V to 4.7V), the A1g_Center should increase
       (blueshift) as lithium is extracted from the cathode
    2. During discharging (voltage decrease from 4.7V to 3.0V), the A1g_Center should decrease
       (redshift) as lithium is reinserted into the cathode
    3. There should be a statistically significant linear correlation between A1g_Center and Voltage
    4. The shift should be reversible across charge/discharge cycles
    """

    print("\n" + "=" * 60)
    print("Hypothesis to Test:")
    print("=" * 60)
    print(hypothesis)

    # Initialize POPPER with battery domain
    print("\nInitializing POPPER agent...")

    # Create and configure the sequential falsification test
    agent = SequentialFalsificationTest(llm=llm, api_key=api_key if api_key else "EMPTY")
    agent.configure(
        data=data_loader,
        alpha=alpha,
        aggregate_test='E-value',
        max_num_of_tests=max_num_of_tests,
        max_retry=max_retry,
        time_limit=time_limit,
        domain="battery",  # Use battery domain for context
        relevance_checker=relevance_checker,
        use_react_agent=use_react_agent
    )

    print("\n" + "=" * 60)
    print("Starting Sequential Falsification Testing...")
    print("=" * 60)

    # Run the hypothesis test
    log, last_message, parsed_result = agent.go(hypothesis)

    # Print results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"\nConclusion: {parsed_result.get('conclusion', 'N/A')}")
    print(f"Rationale: {parsed_result.get('rationale', 'N/A')}")
    print(f"\nFull Results:")
    print(parsed_result)

    return {
        "log": log,
        "last_message": last_message,
        "parsed_result": parsed_result,
        "hypothesis": hypothesis
    }


def quick_data_analysis():
    """
    Quick analysis of the battery data to understand the relationship
    between A1g peak position and voltage.
    """
    import matplotlib.pyplot as plt
    from scipy import stats

    # Load data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    battery_data_path = os.path.join(script_dir, "Battery_Data")

    raman_df = pd.read_csv(os.path.join(battery_data_path, "raman_peaks_decomposed.csv"))
    voltage_df = pd.read_csv(os.path.join(battery_data_path, "voltage_profile_detailed.csv"))

    print("=" * 60)
    print("Quick Data Analysis: A1g Peak vs Voltage")
    print("=" * 60)

    # Aggregate A1g_Center by time step (average across all pixels)
    a1g_by_time = raman_df.groupby('time_idx').agg({
        'A1g_Center': ['mean', 'std'],
        'Voltage': 'first'
    }).reset_index()
    a1g_by_time.columns = ['time_idx', 'A1g_mean', 'A1g_std', 'Voltage']

    print(f"\nData summary:")
    print(f"  Time steps: {len(a1g_by_time)}")
    print(f"  Voltage range: {a1g_by_time['Voltage'].min():.2f}V - {a1g_by_time['Voltage'].max():.2f}V")
    print(f"  A1g_Center range: {a1g_by_time['A1g_mean'].min():.2f} - {a1g_by_time['A1g_mean'].max():.2f} cm^-1")

    # Calculate correlation
    corr, p_value = stats.pearsonr(a1g_by_time['Voltage'], a1g_by_time['A1g_mean'])
    print(f"\nPearson correlation (A1g vs Voltage):")
    print(f"  r = {corr:.4f}")
    print(f"  p-value = {p_value:.2e}")

    # Linear regression
    slope, intercept, r_value, p_val, std_err = stats.linregress(
        a1g_by_time['Voltage'], a1g_by_time['A1g_mean']
    )
    print(f"\nLinear regression:")
    print(f"  A1g = {slope:.4f} * Voltage + {intercept:.4f}")
    print(f"  R^2 = {r_value**2:.4f}")

    return {
        'correlation': corr,
        'p_value': p_value,
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_value**2
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run battery hypothesis testing with POPPER")
    parser.add_argument("--llm", type=str, default="claude-sonnet-4-20250514",
                        help="LLM model to use")
    parser.add_argument("--alpha", type=float, default=0.1,
                        help="Significance level")
    parser.add_argument("--max-tests", type=int, default=5,
                        help="Maximum number of falsification tests")
    parser.add_argument("--quick-analysis", action="store_true",
                        help="Run quick data analysis only")
    parser.add_argument("--api-key", type=str, default=None,
                        help="API key for LLM (optional)")

    args = parser.parse_args()

    if args.quick_analysis:
        # Just run quick analysis
        results = quick_data_analysis()
    else:
        # Run full POPPER hypothesis testing
        results = run_battery_hypothesis_test(
            llm=args.llm,
            alpha=args.alpha,
            max_num_of_tests=args.max_tests,
            api_key=args.api_key
        )
