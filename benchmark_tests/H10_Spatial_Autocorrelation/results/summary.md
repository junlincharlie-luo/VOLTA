# H10: Spatial_Autocorrelation

## Hypothesis

The A1g_Center values of spatially adjacent pixels are more correlated than distant pixels,
indicating local electrochemical domains larger than 1 um.

To test: Compute Moran's I or variogram analysis for spatial autocorrelation at each time step
using X, Y coordinates and A1g_Center values.


## Result
- **Conclusion**: True
- **Elapsed Time**: 253.8s

## Rationale
The falsification test failed to falsify the main hypothesis. The test was specifically designed to detect if the observed spatial autocorrelation could be explained by random chance, and the results (p-value = 0.001) provide strong evidence that the spatial correlation patterns are significantly greater than what would be expected from random arrangements. Since the falsification attempt was unsuccessful - the null hypothesis of random spatial arrangement was rejected - the main hypothesis that A1g_Center values show spatial correlation indicating electrochemical domains larger than 1 μm is supported by the experimental evidence.
