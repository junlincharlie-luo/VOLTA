# H02: Spatial_Heterogeneity

## Hypothesis

The standard deviation of A1g_Center across the 900 spatial pixels increases as voltage increases,
indicating growing electrochemical heterogeneity during delithiation.

To test: Calculate spatial variance/std of A1g_Center at each time step and correlate with voltage.


## Result
- **Conclusion**: True
- **Elapsed Time**: 86.7s

## Rationale
The falsification test failed to falsify the main hypothesis. The test was specifically designed to find evidence against the hypothesis that spatial heterogeneity increases with voltage. However, the results showed overwhelming statistical evidence (p ≈ 2.93e-20) that the high voltage stratum does indeed have significantly greater spatial heterogeneity than the low voltage stratum. Since the falsification attempt failed with such strong contradictory evidence, and no other tests were performed that successfully falsified the hypothesis, the main hypothesis remains supported and is concluded to be True.
