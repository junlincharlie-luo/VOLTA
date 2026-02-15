# H02: Spatial_Heterogeneity

**Model**: GPT-4o

## Hypothesis

The spatial heterogeneity of A1g peak position increases during charging. Specifically,
the standard deviation of A1g_Center values across the 900 spatial pixels (30x30 grid)
increases as voltage increases from 3.05V to 4.68V.

This reflects non-uniform delithiation across the electrode surface, with some regions
experiencing faster lithium extraction than others during high-voltage charging.

Expected Result: Positive correlation between voltage and spatial standard deviation of A1g_Center.


## Result
- **Conclusion**: True
- **Elapsed Time**: 192.9 seconds

## Rationale
The hypothesis that spatial heterogeneity increases during charging is supported because the test did not find evidence of decreased spatial standard deviation (uniformity) with increasing voltage. The significant E-value demonstrates that the observed increase in heterogeneity is consistent with the main hypothesis, hence it is not falsified.
