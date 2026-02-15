# VOLTA Full Benchmark Results (All 20 Hypotheses)

**Date**: 2026-02-09 00:33:10
**Model**: gemini-3.0
**Total Time**: 3.7 seconds

## Part A: Verifiable Hypotheses (H01-H10)

| ID | Hypothesis | Status | Conclusion | Time (s) |
|-----|-----------|--------|------------|----------|
| H01 | A1g_Voltage_Correlation | ✗ | Error code: 404 - [{'error': {'code': 404, 'messag | N/A |
| H02 | Spatial_Heterogeneity | ✗ | Error code: 404 - [{'error': {'code': 404, 'messag | N/A |
| H03 | ID_IG_High_Voltage | ✗ | Error code: 404 - [{'error': {'code': 404, 'messag | N/A |
| H04 | Eg_Amplitude | ✗ | Error code: 404 - [{'error': {'code': 404, 'messag | N/A |
| H05 | Spatial_Decoupling | ✗ | Error code: 404 - [{'error': {'code': 404, 'messag | N/A |
| H06 | Edge_Center_Uniformity | ✗ | Error code: 404 - [{'error': {'code': 404, 'messag | N/A |
| H07 | A1g_Width | ✗ | Error code: 404 - [{'error': {'code': 404, 'messag | N/A |
| H08 | Gband_Redshift | ✗ | Error code: 404 - [{'error': {'code': 404, 'messag | N/A |
| H09 | Dband_Time_Delay | ✗ | Error code: 404 - [{'error': {'code': 404, 'messag | N/A |
| H10 | Spatial_Autocorrelation | ✗ | Error code: 404 - [{'error': {'code': 404, 'messag | N/A |

## Part B: Non-Verifiable Hypotheses (H11-H20)

*These hypotheses are designed to be non-verifiable with the available data.*

| ID | Hypothesis | Status | Conclusion | Time (s) |
|-----|-----------|--------|------------|----------|
| H11 | Voltage_Fade | ✗ | Error code: 404 - [{'error': {'code': 404, 'messag | N/A |
| H12 | Capacity_Retention | ✗ | Error code: 404 - [{'error': {'code': 404, 'messag | N/A |
| H13 | Oxygen_Release | ✗ | Error code: 404 - [{'error': {'code': 404, 'messag | N/A |
| H14 | Temperature_Dependence | ✗ | Error code: 404 - [{'error': {'code': 404, 'messag | N/A |
| H15 | Cation_Mixing | ✗ | Error code: 404 - [{'error': {'code': 404, 'messag | N/A |
| H16 | CEI_Steady_State | ✗ | Error code: 404 - [{'error': {'code': 404, 'messag | N/A |
| H17 | Rate_Capability | ✗ | Error code: 404 - [{'error': {'code': 404, 'messag | N/A |
| H18 | Discharge_Reversibility | ✗ | Error code: 404 - [{'error': {'code': 404, 'messag | N/A |
| H19 | Electrolyte_Decomposition | ✗ | Error code: 404 - [{'error': {'code': 404, 'messag | N/A |
| H20 | Mn_Dissolution | ✗ | Error code: 404 - [{'error': {'code': 404, 'messag | N/A |

## Statistics
- **Successful**: 0/20
- **Failed**: 20/20

## Failures

### H03: ID_IG_High_Voltage
```
Error code: 404 - [{'error': {'code': 404, 'message': 'models/gemini-3.0 is not found for API version v1main, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}]
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 244, in run_single_hypothesis
    log, last_message, parsed_result = agent.go(hypothesis_data["hypothesis"])
                            
```

### H02: Spatial_Heterogeneity
```
Error code: 404 - [{'error': {'code': 404, 'message': 'models/gemini-3.0 is not found for API version v1main, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}]
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 244, in run_single_hypothesis
    log, last_message, parsed_result = agent.go(hypothesis_data["hypothesis"])
                            
```

### H01: A1g_Voltage_Correlation
```
Error code: 404 - [{'error': {'code': 404, 'message': 'models/gemini-3.0 is not found for API version v1main, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}]
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 244, in run_single_hypothesis
    log, last_message, parsed_result = agent.go(hypothesis_data["hypothesis"])
                            
```

### H06: Edge_Center_Uniformity
```
Error code: 404 - [{'error': {'code': 404, 'message': 'models/gemini-3.0 is not found for API version v1main, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}]
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 244, in run_single_hypothesis
    log, last_message, parsed_result = agent.go(hypothesis_data["hypothesis"])
                            
```

### H04: Eg_Amplitude
```
Error code: 404 - [{'error': {'code': 404, 'message': 'models/gemini-3.0 is not found for API version v1main, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}]
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 244, in run_single_hypothesis
    log, last_message, parsed_result = agent.go(hypothesis_data["hypothesis"])
                            
```

### H05: Spatial_Decoupling
```
Error code: 404 - [{'error': {'code': 404, 'message': 'models/gemini-3.0 is not found for API version v1main, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}]
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 244, in run_single_hypothesis
    log, last_message, parsed_result = agent.go(hypothesis_data["hypothesis"])
                            
```

### H07: A1g_Width
```
Error code: 404 - [{'error': {'code': 404, 'message': 'models/gemini-3.0 is not found for API version v1main, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}]
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 244, in run_single_hypothesis
    log, last_message, parsed_result = agent.go(hypothesis_data["hypothesis"])
                            
```

### H08: Gband_Redshift
```
Error code: 404 - [{'error': {'code': 404, 'message': 'models/gemini-3.0 is not found for API version v1main, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}]
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 244, in run_single_hypothesis
    log, last_message, parsed_result = agent.go(hypothesis_data["hypothesis"])
                            
```

### H09: Dband_Time_Delay
```
Error code: 404 - [{'error': {'code': 404, 'message': 'models/gemini-3.0 is not found for API version v1main, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}]
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 244, in run_single_hypothesis
    log, last_message, parsed_result = agent.go(hypothesis_data["hypothesis"])
                            
```

### H10: Spatial_Autocorrelation
```
Error code: 404 - [{'error': {'code': 404, 'message': 'models/gemini-3.0 is not found for API version v1main, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}]
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 244, in run_single_hypothesis
    log, last_message, parsed_result = agent.go(hypothesis_data["hypothesis"])
                            
```

### H11: Voltage_Fade
```
Error code: 404 - [{'error': {'code': 404, 'message': 'models/gemini-3.0 is not found for API version v1main, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}]
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 244, in run_single_hypothesis
    log, last_message, parsed_result = agent.go(hypothesis_data["hypothesis"])
                            
```

### H12: Capacity_Retention
```
Error code: 404 - [{'error': {'code': 404, 'message': 'models/gemini-3.0 is not found for API version v1main, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}]
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 244, in run_single_hypothesis
    log, last_message, parsed_result = agent.go(hypothesis_data["hypothesis"])
                            
```

### H15: Cation_Mixing
```
Error code: 404 - [{'error': {'code': 404, 'message': 'models/gemini-3.0 is not found for API version v1main, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}]
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 244, in run_single_hypothesis
    log, last_message, parsed_result = agent.go(hypothesis_data["hypothesis"])
                            
```

### H13: Oxygen_Release
```
Error code: 404 - [{'error': {'code': 404, 'message': 'models/gemini-3.0 is not found for API version v1main, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}]
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 244, in run_single_hypothesis
    log, last_message, parsed_result = agent.go(hypothesis_data["hypothesis"])
                            
```

### H14: Temperature_Dependence
```
Error code: 404 - [{'error': {'code': 404, 'message': 'models/gemini-3.0 is not found for API version v1main, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}]
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 244, in run_single_hypothesis
    log, last_message, parsed_result = agent.go(hypothesis_data["hypothesis"])
                            
```

### H16: CEI_Steady_State
```
Error code: 404 - [{'error': {'code': 404, 'message': 'models/gemini-3.0 is not found for API version v1main, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}]
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 244, in run_single_hypothesis
    log, last_message, parsed_result = agent.go(hypothesis_data["hypothesis"])
                            
```

### H17: Rate_Capability
```
Error code: 404 - [{'error': {'code': 404, 'message': 'models/gemini-3.0 is not found for API version v1main, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}]
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 244, in run_single_hypothesis
    log, last_message, parsed_result = agent.go(hypothesis_data["hypothesis"])
                            
```

### H18: Discharge_Reversibility
```
Error code: 404 - [{'error': {'code': 404, 'message': 'models/gemini-3.0 is not found for API version v1main, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}]
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 244, in run_single_hypothesis
    log, last_message, parsed_result = agent.go(hypothesis_data["hypothesis"])
                            
```

### H20: Mn_Dissolution
```
Error code: 404 - [{'error': {'code': 404, 'message': 'models/gemini-3.0 is not found for API version v1main, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}]
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 244, in run_single_hypothesis
    log, last_message, parsed_result = agent.go(hypothesis_data["hypothesis"])
                            
```

### H19: Electrolyte_Decomposition
```
Error code: 404 - [{'error': {'code': 404, 'message': 'models/gemini-3.0 is not found for API version v1main, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}]
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 244, in run_single_hypothesis
    log, last_message, parsed_result = agent.go(hypothesis_data["hypothesis"])
                            
```
