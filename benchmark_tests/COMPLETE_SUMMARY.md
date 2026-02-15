# Complete POPPER Benchmark Results (H1-H20)

**Date**: 2026-02-09
**Model**: claude-sonnet-4-20250514

## Part A: Verifiable Hypotheses (H1-H10)

| ID | Hypothesis | Result | Time | Notes |
|----|-----------|--------|------|-------|
| H1 | A1g vs Voltage Correlation | **TRUE** | 91s | r=-0.88, p=1.1e-177 |
| H2 | Spatial Heterogeneity Increases | **TRUE** | 87s | Confirmed |
| H3 | ID/IG Decreases at High Voltage | **TRUE** | 133s | ~10% decrease at V>4.3V |
| H4 | Eg Amplitude Increases | **TRUE** | 76s | Positive correlation |
| H5 | Cathode-Carbon Spatial Decoupling | **TRUE** | 222s | Weak correlation confirms independence |
| H6 | Edge-Center Uniformity | **FALSE** | 99s | Falsified! p=5.28e-61 |
| H7 | A1g Width Decreases | **TRUE** | 80s | Strong negative correlation |
| H8 | G-band Redshift | **TRUE** | 106s | Voltage-dependent redshift |
| H9 | D-band Time Delay | **TRUE** | 253s | Kinetic delay confirmed |
| H10 | Spatial Autocorrelation | **TRUE** | 254s | Domains >1μm confirmed |

**Part A Score: 9/10 validated, 1/10 falsified**

---

## Part B: Non-Verifiable Hypotheses (H11-H20)

These hypotheses were designed to be UNTESTABLE with the available data (missing multi-cycle, temperature, discharge, or other required data).

| ID | Hypothesis | Missing Data | POPPER Result | Time | Behavior |
|----|-----------|--------------|---------------|------|----------|
| H11 | Voltage Fade | Multi-cycle | **TRUE** | 154s | Found structural evidence |
| H12 | Capacity Retention | Long-term cycling | **TRUE** | 497s | Found supporting indicators |
| H13 | Oxygen Release | O₂ detection | **TRUE** | 139s | Found indirect evidence |
| H14 | Temperature Dependence | Temperature data | **CRASH** | - | KeyError: no test possible |
| H15 | Cation Mixing | Multi-cycle | **FALSE** | 239s | Correctly identified insufficient data |
| H16 | CEI Steady State | Multi-cycle | **FALSE** | 190s | Correctly identified insufficient data |
| H17 | Rate Capability | Multiple C-rates | **FALSE** | 197s | Correctly identified insufficient data |
| H18 | Discharge Reversibility | Discharge data | **CRASH** | - | KeyError: no test possible |
| H19 | Electrolyte Decomposition | Full spectra | **TRUE** | 347s | Found indirect evidence |
| H20 | Mn Dissolution | ICP-MS data | **CRASH** | - | KeyError: no test possible |

**Part B Results:**
- 4/10 marked TRUE (found indirect supporting evidence)
- 3/10 marked FALSE (correctly identified insufficient data)
- 3/10 CRASHED (couldn't formulate any test)

---

## Analysis

### POPPER Strengths:
1. **Excellent on verifiable hypotheses**: 100% correct on H1-H10 (validated 9, correctly falsified 1)
2. **Strong statistical rigor**: Uses E-values, sequential testing, proper Type-I error control
3. **Detailed reasoning**: Provides falsification test design, null/alternate hypotheses, and rationale

### POPPER Limitations on Non-Verifiable Hypotheses:
1. **Inconsistent handling**: Some non-verifiable hypotheses marked TRUE based on indirect evidence (H11, H12, H13, H19), while others correctly marked FALSE (H15, H16, H17)
2. **Crash on extreme cases**: When absolutely no test can be formulated (H14, H18, H20), the framework crashes instead of gracefully reporting "untestable"

### Key Finding - H6 Falsified:
The only falsified verifiable hypothesis revealed important scientific insight:
> "Edge and center pixels are NOT uniform - significant correlation (p=5.28e-61) between radial distance and A1g shift indicates electrochemical accessibility varies systematically across the electrode."

---

## Summary Statistics

| Category | Count | Percentage |
|----------|-------|------------|
| Verifiable - Validated | 9 | 45% |
| Verifiable - Falsified | 1 | 5% |
| Non-verifiable - TRUE (indirect evidence) | 4 | 20% |
| Non-verifiable - FALSE (insufficient data) | 3 | 15% |
| Non-verifiable - CRASH | 3 | 15% |

**Total tests: 20**
**Successful completions: 17/20 (85%)**
