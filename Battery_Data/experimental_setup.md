# Experimental Setup and Methodology

This document details the experimental configuration, materials, and data processing pipeline used for the Operando Raman Spectroscopy analysis of Li-rich layered oxide cathodes.

## 1. Experimental Overview

**Objective**: To monitor the real-time structural evolution and degradation mechanisms of the cathode-electrolyte interface during high-voltage cycling.

### Materials
*   **Cathode Material**: Li$_{1.13}$Ni$_{0.3}$Mn$_{0.57}$O$_{2}$ (Li-rich Layered Oxide).
    *   *Note*: The material is uncoated.
*   **Electrolyte**: LiPF$_6$ salt dissolved in organic solvents.
*   **Solvent System**: Ethylene Carbonate (EC) / Dimethyl Carbonate (DMC).

### Electrochemical Cycling
*   **Cell Type**: Operando optical cell.
*   **Voltage Window**: **3.0 V to 4.7 V** vs. Li/Li$^+$.
*   **Cycling Protocol**: Constant Current - Constant Voltage (CCCV) or similar standard cycling during spectral acquisition.

## 2. Raman Spectroscopy Configuration

The experiment utilizes a confocal Raman microscope to map the electrode surface over time.

*   **Technique**: Operando Raman Mapping.
*   **Measurement Area**: 30 $\times$ 30 $\mu$m region.
*   **Spatial Resolution**: 1 $\mu$m step size (implied by 30x30 grid).
    *   **Total Pixels**: 900 pixels (30 $\times$ 30 grid).
*   **Temporal Resolution**:
    *   **Interval**: Spectra collected every **15 minutes**.
    *   **Total Duration**: 114 Time steps ($\approx$ 28.5 hours).
*   **Spectral Range**: Covers at least 200 - 1800 cm$^{-1}$ (based on fit windows).

## 3. Data Processing Pipeline

The raw spectral data undergoes a rigorous preprocessing and analysis pipeline to extract quantitative physicochemical descriptors.

### A. Preprocessing (`preprocessed_data/`)
1.  **Spatial Despiking**:
    *   Method: 3$\times$3 Median Filter.
    *   Purpose: Removes cosmic rays and single-pixel transient noise.
2.  **Spectral Smoothing**:
    *   Method: Savitzky-Golay Filter.
    *   Parameters: Window length = 15, Polynomial order = 3.
    *   Purpose: Reduces high-frequency noise while preserving peak shapes.
3.  **Baseline Correction**:
    *   Method: Asymmetric Least Squares (ALS).
    *   Purpose: Removes the broad fluorescence background to flatten the spectra.

### B. Peak Decomposition (`analysis_results_full/`)
Complex spectral profiles are deconvoluted using non-linear least squares fitting.

| Component | Peak | Approx. Position | Shape Function | Physical Significance |
| :--- | :--- | :--- | :--- | :--- |
| **Cathode** | **$E_g$** | ~475 cm$^{-1}$ | Pseudo-Voigt | M-O bending / Layered structure |
| **Cathode** | **$A_{1g}$** | ~590 cm$^{-1}$ | Pseudo-Voigt | M-O stretching / **Primary SOC Indicator** |
| **Carbon** | **D-band** | ~1350 cm$^{-1}$ | Gaussian | Disordered carbon / Defects |
| **Carbon** | **G-band** | ~1585 cm$^{-1}$ | Gaussian | Graphitic carbon / Conductivity |

### C. Key Analysis Metrics
1.  **$A_{1g}$ Peak Shift**: Tracks Lithium concentration (State of Charge). The peak blueshifts (moves to higher wavenumbers) during delithiation (charging).
2.  **$I_D / I_G$ Ratio**: Ratio of D-band to G-band amplitude. Used to monitor carbon network degradation and Surface Electrolyte Interphase (SEI) formation.

## 4. Statistical Considerations

### Sample Independence
In statistical testing, the **900 pixels are highly correlated** and cannot be treated as independent events. The spatial proximity of pixels within the 30 × 30 μm measurement area means they share common local conditions (e.g., electrolyte exposure, current distribution, thermal gradients), violating the independence assumption required for many statistical tests.

**Approach 1: Half-Cycle Based (Limited)**
- 3 half-cycles (2 charging + 1 discharge)
- Provides n=3 independent events
- Limited statistical power (min p-value = 0.125)

**Approach 2: Particle-Based (Recommended)**
- Identify spatially isolated particles from A1g intensity
- Use `identify_particles` tool for segmentation
- Typically yields 5-20 independent particles
- Each particle's behavior is independent
- Enables meaningful statistical testing with n >> 3
