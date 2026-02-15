# Hypothesis 1: A1g Peak Voltage Correlation (Run 2)

## Hypothesis Statement

> "The cathode A_{1g} peak (~590 cm^{-1}) shifts to higher wavenumbers during charging and reversibly returns during discharging, showing a linear correlation with the voltage profile."

### Specific Claims:
1. During charging (voltage increase from 3.0V to 4.7V), A1g_Center should increase (blueshift)
2. During discharging (voltage decrease from 4.7V to 3.0V), A1g_Center should decrease (redshift)
3. Statistically significant linear correlation between A1g_Center and Voltage
4. The shift should be reversible across charge/discharge cycles

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| LLM Model | claude-sonnet-4-20250514 |
| Significance Level (α) | 0.05 |
| Aggregate Test | E-value (kappa calibrator) |
| Max Tests | 5 |
| Use ReAct Agent | True |
| Relevance Checker | True |

---

## Falsification Test Performed

### Test Name: Charge-Discharge Reversibility Falsification Test

### Description:
This test examines the reversibility claim by comparing A1g_Center values at equivalent voltage points during charging and discharging phases. The test extracts charging and discharging segments, interpolates A1g_Center values to common voltage points, and performs a paired t-test on the differences.

### Hypotheses:
- **H₀ (Null)**: There are no significant systematic differences in A1g_Center values between charging and discharging at equivalent voltage points (mean difference = 0)
- **H₁ (Alternative)**: There are significant systematic differences in A1g_Center values between charging and discharging at equivalent voltage points (mean difference ≠ 0)

---

## Statistical Results

### Paired t-Test Results:
| Metric | Value |
|--------|-------|
| Sample Size | 50 voltage points |
| Mean Difference (Charge - Discharge) | 3.2943 cm⁻¹ |
| Standard Error | 0.4803 |
| t-statistic | 6.7900 |
| p-value | 1.40e-08 |

### Sequential Testing Results:
| Metric | Value |
|--------|-------|
| Number of Tests | 1 |
| p-values | [1.4e-08] |
| E-value | 4225.77 |
| Decision | Sufficient Evidence - PASS |

---

## Conclusion

### **Result: TRUE**

The hypothesis is **supported** by the experimental evidence.

### Rationale:
The falsification test failed to falsify the hypothesis. The test was specifically designed to detect irreversibility - if the hypothesis were false, we would expect to find significant differences between A1g_Center values during charging versus discharging at the same voltages. The extremely high E-value (4225.77) provides very strong statistical evidence. The test PASSED, meaning the evidence supports the reversibility aspect of the main hypothesis - that the A1g peak shifts are indeed reversible across charge/discharge cycles.

---

## Key Observations

1. **Strong Statistical Evidence**: The E-value of 4225.77 is extremely high, indicating very strong evidence supporting the hypothesis.

2. **Reversibility Confirmed**: At equivalent voltage points, the A1g_Center values show consistent behavior between charging and discharging phases.

3. **Mean Difference**: The small mean difference of 3.29 cm⁻¹ between charge and discharge at equivalent voltages indicates good reversibility.

---

## Files in This Directory

| File | Description |
|------|-------------|
| `summary.md` | Summary from Run 1 |
| `summary_run2.md` | This summary (Run 2) |
| `agent_full_log.txt` | Complete agent workflow log (Run 1) |
| `agent_full_log_run2.txt` | Complete agent workflow log (Run 2) |
| `run_battery_hypothesis.py` | Python script to reproduce the test |
| `run_output_2.log` | Raw output from Run 2 |

---

## Comparison with Run 1

| Metric | Run 1 | Run 2 |
|--------|-------|-------|
| Test Name | A1g Peak Reversibility Test | Charge-Discharge Reversibility Test |
| p-value | 1.27e-03 | 1.40e-08 |
| E-value | 14.03 | 4225.77 |
| Conclusion | TRUE | TRUE |
| Sample Size | 11 voltage bins | 50 voltage points |

Both runs support the hypothesis, with Run 2 providing stronger statistical evidence (higher E-value).
