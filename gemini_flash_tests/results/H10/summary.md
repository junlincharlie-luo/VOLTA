# H10: Spatial_Autocorrelation

**Model**: Gemini 2.0 Flash

## Hypothesis

The A1g_Center values of spatially adjacent pixels are more correlated than distant pixels,
indicating local electrochemical domains larger than 1 um scale.

Expected Result: Positive spatial autocorrelation (Moran's I > 0) at each time step, with
significance testing showing non-random spatial patterns.


## Result
- **Conclusion**: True
- **Elapsed Time**: 59.2 seconds

## Rationale
The Random Pixel Shuffle Test passed, providing evidence against the null sub-hypothesis and supporting the alternate sub-hypothesis. This suggests that the observed spatial autocorrelation in the original data is likely due to the spatial arrangement of A1g_Center values, as posited by the main hypothesis. Therefore, we conclude the main hypothesis is true.
