# H09: Dband_Time_Delay

## Hypothesis

Changes in D-band amplitude (D_Amp) lag behind voltage changes by at least one measurement
interval (15 min), suggesting SEI formation is a kinetically slow process.

To test: Perform cross-correlation analysis with time lag between voltage derivative and
D_Amp derivative using D_Amp and Time_Min columns.


## Result
- **Conclusion**: True
- **Elapsed Time**: 253.1s

## Rationale
The sequential falsification test procedure failed to reject the main hypothesis after two independent tests. Both the cross-correlation analysis and variance explanation comparison found insufficient evidence that D_Amp changes are predominantly explained by instantaneous voltage effects. The combined E-value of 21.68 indicates strong statistical evidence supporting the existence of kinetic delays in D-band amplitude changes relative to voltage changes, consistent with SEI formation being a kinetically slow process occurring over time scales of at least 15 minutes.
