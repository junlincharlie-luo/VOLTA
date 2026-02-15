# VOLTA Full Benchmark Results (All 20 Hypotheses)

**Date**: 2026-02-09 00:32:39
**Model**: gemini-3.0
**Total Time**: 2.9 seconds

## Part A: Verifiable Hypotheses (H01-H10)

| ID | Hypothesis | Status | Conclusion | Time (s) |
|-----|-----------|--------|------------|----------|
| H01 | A1g_Voltage_Correlation | ✗ | Port must be specified for local models
Traceback  | N/A |
| H02 | Spatial_Heterogeneity | ✗ | Port must be specified for local models
Traceback  | N/A |
| H03 | ID_IG_High_Voltage | ✗ | Port must be specified for local models
Traceback  | N/A |
| H04 | Eg_Amplitude | ✗ | Port must be specified for local models
Traceback  | N/A |
| H05 | Spatial_Decoupling | ✗ | Port must be specified for local models
Traceback  | N/A |
| H06 | Edge_Center_Uniformity | ✗ | Port must be specified for local models
Traceback  | N/A |
| H07 | A1g_Width | ✗ | Port must be specified for local models
Traceback  | N/A |
| H08 | Gband_Redshift | ✗ | Port must be specified for local models
Traceback  | N/A |
| H09 | Dband_Time_Delay | ✗ | Port must be specified for local models
Traceback  | N/A |
| H10 | Spatial_Autocorrelation | ✗ | Port must be specified for local models
Traceback  | N/A |

## Part B: Non-Verifiable Hypotheses (H11-H20)

*These hypotheses are designed to be non-verifiable with the available data.*

| ID | Hypothesis | Status | Conclusion | Time (s) |
|-----|-----------|--------|------------|----------|
| H11 | Voltage_Fade | ✗ | Port must be specified for local models
Traceback  | N/A |
| H12 | Capacity_Retention | ✗ | Port must be specified for local models
Traceback  | N/A |
| H13 | Oxygen_Release | ✗ | Port must be specified for local models
Traceback  | N/A |
| H14 | Temperature_Dependence | ✗ | Port must be specified for local models
Traceback  | N/A |
| H15 | Cation_Mixing | ✗ | Port must be specified for local models
Traceback  | N/A |
| H16 | CEI_Steady_State | ✗ | Port must be specified for local models
Traceback  | N/A |
| H17 | Rate_Capability | ✗ | Port must be specified for local models
Traceback  | N/A |
| H18 | Discharge_Reversibility | ✗ | Port must be specified for local models
Traceback  | N/A |
| H19 | Electrolyte_Decomposition | ✗ | Port must be specified for local models
Traceback  | N/A |
| H20 | Mn_Dissolution | ✗ | Port must be specified for local models
Traceback  | N/A |

## Statistics
- **Successful**: 0/20
- **Failed**: 20/20

## Failures

### H03: ID_IG_High_Voltage
```
Port must be specified for local models
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 231, in run_single_hypothesis
    agent.configure(
    ~~~~~~~~~~~~~~~^
        data=data_loader,
        ^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        use_react_agent=config["use_react_agent"]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/carrot/Desktop/VOLTA/volta/agent.py", line 908, in configure
    self.test_coding_a
```

### H02: Spatial_Heterogeneity
```
Port must be specified for local models
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 231, in run_single_hypothesis
    agent.configure(
    ~~~~~~~~~~~~~~~^
        data=data_loader,
        ^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        use_react_agent=config["use_react_agent"]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/carrot/Desktop/VOLTA/volta/agent.py", line 908, in configure
    self.test_coding_a
```

### H01: A1g_Voltage_Correlation
```
Port must be specified for local models
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 231, in run_single_hypothesis
    agent.configure(
    ~~~~~~~~~~~~~~~^
        data=data_loader,
        ^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        use_react_agent=config["use_react_agent"]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/carrot/Desktop/VOLTA/volta/agent.py", line 908, in configure
    self.test_coding_a
```

### H04: Eg_Amplitude
```
Port must be specified for local models
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 231, in run_single_hypothesis
    agent.configure(
    ~~~~~~~~~~~~~~~^
        data=data_loader,
        ^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        use_react_agent=config["use_react_agent"]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/carrot/Desktop/VOLTA/volta/agent.py", line 908, in configure
    self.test_coding_a
```

### H06: Edge_Center_Uniformity
```
Port must be specified for local models
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 231, in run_single_hypothesis
    agent.configure(
    ~~~~~~~~~~~~~~~^
        data=data_loader,
        ^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        use_react_agent=config["use_react_agent"]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/carrot/Desktop/VOLTA/volta/agent.py", line 908, in configure
    self.test_coding_a
```

### H05: Spatial_Decoupling
```
Port must be specified for local models
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 231, in run_single_hypothesis
    agent.configure(
    ~~~~~~~~~~~~~~~^
        data=data_loader,
        ^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        use_react_agent=config["use_react_agent"]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/carrot/Desktop/VOLTA/volta/agent.py", line 908, in configure
    self.test_coding_a
```

### H07: A1g_Width
```
Port must be specified for local models
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 231, in run_single_hypothesis
    agent.configure(
    ~~~~~~~~~~~~~~~^
        data=data_loader,
        ^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        use_react_agent=config["use_react_agent"]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/carrot/Desktop/VOLTA/volta/agent.py", line 908, in configure
    self.test_coding_a
```

### H08: Gband_Redshift
```
Port must be specified for local models
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 231, in run_single_hypothesis
    agent.configure(
    ~~~~~~~~~~~~~~~^
        data=data_loader,
        ^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        use_react_agent=config["use_react_agent"]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/carrot/Desktop/VOLTA/volta/agent.py", line 908, in configure
    self.test_coding_a
```

### H09: Dband_Time_Delay
```
Port must be specified for local models
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 231, in run_single_hypothesis
    agent.configure(
    ~~~~~~~~~~~~~~~^
        data=data_loader,
        ^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        use_react_agent=config["use_react_agent"]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/carrot/Desktop/VOLTA/volta/agent.py", line 908, in configure
    self.test_coding_a
```

### H10: Spatial_Autocorrelation
```
Port must be specified for local models
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 231, in run_single_hypothesis
    agent.configure(
    ~~~~~~~~~~~~~~~^
        data=data_loader,
        ^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        use_react_agent=config["use_react_agent"]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/carrot/Desktop/VOLTA/volta/agent.py", line 908, in configure
    self.test_coding_a
```

### H12: Capacity_Retention
```
Port must be specified for local models
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 231, in run_single_hypothesis
    agent.configure(
    ~~~~~~~~~~~~~~~^
        data=data_loader,
        ^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        use_react_agent=config["use_react_agent"]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/carrot/Desktop/VOLTA/volta/agent.py", line 908, in configure
    self.test_coding_a
```

### H11: Voltage_Fade
```
Port must be specified for local models
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 231, in run_single_hypothesis
    agent.configure(
    ~~~~~~~~~~~~~~~^
        data=data_loader,
        ^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        use_react_agent=config["use_react_agent"]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/carrot/Desktop/VOLTA/volta/agent.py", line 908, in configure
    self.test_coding_a
```

### H13: Oxygen_Release
```
Port must be specified for local models
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 231, in run_single_hypothesis
    agent.configure(
    ~~~~~~~~~~~~~~~^
        data=data_loader,
        ^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        use_react_agent=config["use_react_agent"]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/carrot/Desktop/VOLTA/volta/agent.py", line 908, in configure
    self.test_coding_a
```

### H14: Temperature_Dependence
```
Port must be specified for local models
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 231, in run_single_hypothesis
    agent.configure(
    ~~~~~~~~~~~~~~~^
        data=data_loader,
        ^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        use_react_agent=config["use_react_agent"]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/carrot/Desktop/VOLTA/volta/agent.py", line 908, in configure
    self.test_coding_a
```

### H15: Cation_Mixing
```
Port must be specified for local models
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 231, in run_single_hypothesis
    agent.configure(
    ~~~~~~~~~~~~~~~^
        data=data_loader,
        ^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        use_react_agent=config["use_react_agent"]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/carrot/Desktop/VOLTA/volta/agent.py", line 908, in configure
    self.test_coding_a
```

### H16: CEI_Steady_State
```
Port must be specified for local models
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 231, in run_single_hypothesis
    agent.configure(
    ~~~~~~~~~~~~~~~^
        data=data_loader,
        ^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        use_react_agent=config["use_react_agent"]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/carrot/Desktop/VOLTA/volta/agent.py", line 908, in configure
    self.test_coding_a
```

### H18: Discharge_Reversibility
```
Port must be specified for local models
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 231, in run_single_hypothesis
    agent.configure(
    ~~~~~~~~~~~~~~~^
        data=data_loader,
        ^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        use_react_agent=config["use_react_agent"]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/carrot/Desktop/VOLTA/volta/agent.py", line 908, in configure
    self.test_coding_a
```

### H17: Rate_Capability
```
Port must be specified for local models
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 231, in run_single_hypothesis
    agent.configure(
    ~~~~~~~~~~~~~~~^
        data=data_loader,
        ^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        use_react_agent=config["use_react_agent"]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/carrot/Desktop/VOLTA/volta/agent.py", line 908, in configure
    self.test_coding_a
```

### H19: Electrolyte_Decomposition
```
Port must be specified for local models
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 231, in run_single_hypothesis
    agent.configure(
    ~~~~~~~~~~~~~~~^
        data=data_loader,
        ^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        use_react_agent=config["use_react_agent"]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/carrot/Desktop/VOLTA/volta/agent.py", line 908, in configure
    self.test_coding_a
```

### H20: Mn_Dissolution
```
Port must be specified for local models
Traceback (most recent call last):
  File "/Users/carrot/Desktop/VOLTA/run_all_20_hypotheses.py", line 231, in run_single_hypothesis
    agent.configure(
    ~~~~~~~~~~~~~~~^
        data=data_loader,
        ^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        use_react_agent=config["use_react_agent"]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/carrot/Desktop/VOLTA/volta/agent.py", line 908, in configure
    self.test_coding_a
```
