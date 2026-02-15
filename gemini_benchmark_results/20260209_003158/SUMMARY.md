# POPPER Full Benchmark Results (All 20 Hypotheses)

**Date**: 2026-02-09 00:32:00
**Model**: gemini-3.0
**Total Time**: 2.4 seconds

## Part A: Verifiable Hypotheses (H01-H10)

| ID | Hypothesis | Status | Conclusion | Time (s) |
|-----|-----------|--------|------------|----------|
| H01 | A1g_Voltage_Correlation | ✗ | cannot import name 'ModelProfile' from 'langchain_ | N/A |
| H02 | Spatial_Heterogeneity | ✗ | cannot import name 'ModelProfile' from 'langchain_ | N/A |
| H03 | ID_IG_High_Voltage | ✗ | cannot import name 'ModelProfile' from 'langchain_ | N/A |
| H04 | Eg_Amplitude | ✗ | cannot import name 'ModelProfile' from 'langchain_ | N/A |
| H05 | Spatial_Decoupling | ✗ | cannot import name 'ModelProfile' from 'langchain_ | N/A |
| H06 | Edge_Center_Uniformity | ✗ | cannot import name 'ModelProfile' from 'langchain_ | N/A |
| H07 | A1g_Width | ✗ | cannot import name 'ModelProfile' from 'langchain_ | N/A |
| H08 | Gband_Redshift | ✗ | cannot import name 'ModelProfile' from 'langchain_ | N/A |
| H09 | Dband_Time_Delay | ✗ | cannot import name 'ModelProfile' from 'langchain_ | N/A |
| H10 | Spatial_Autocorrelation | ✗ | cannot import name 'ModelProfile' from 'langchain_ | N/A |

## Part B: Non-Verifiable Hypotheses (H11-H20)

*These hypotheses are designed to be non-verifiable with the available data.*

| ID | Hypothesis | Status | Conclusion | Time (s) |
|-----|-----------|--------|------------|----------|
| H11 | Voltage_Fade | ✗ | cannot import name 'ModelProfile' from 'langchain_ | N/A |
| H12 | Capacity_Retention | ✗ | cannot import name 'ModelProfile' from 'langchain_ | N/A |
| H13 | Oxygen_Release | ✗ | cannot import name 'ModelProfile' from 'langchain_ | N/A |
| H14 | Temperature_Dependence | ✗ | cannot import name 'ModelProfile' from 'langchain_ | N/A |
| H15 | Cation_Mixing | ✗ | cannot import name 'ModelProfile' from 'langchain_ | N/A |
| H16 | CEI_Steady_State | ✗ | cannot import name 'ModelProfile' from 'langchain_ | N/A |
| H17 | Rate_Capability | ✗ | cannot import name 'ModelProfile' from 'langchain_ | N/A |
| H18 | Discharge_Reversibility | ✗ | cannot import name 'ModelProfile' from 'langchain_ | N/A |
| H19 | Electrolyte_Decomposition | ✗ | cannot import name 'ModelProfile' from 'langchain_ | N/A |
| H20 | Mn_Dissolution | ✗ | cannot import name 'ModelProfile' from 'langchain_ | N/A |

## Statistics
- **Successful**: 0/20
- **Failed**: 20/20

## Failures

### H02: Spatial_Heterogeneity
```
cannot import name 'ModelProfile' from 'langchain_core.language_models' (/opt/miniconda3/lib/python3.13/site-packages/langchain_core/language_models/__init__.py)
Traceback (most recent call last):
  File "/Users/carrot/Desktop/POPPER/run_all_20_hypotheses.py", line 216, in run_single_hypothesis
    from popper.agent import SequentialFalsificationTest
  File "/Users/carrot/Desktop/POPPER/popper/__init__.py", line 1, in <module>
    from .popper import Popper
  File "/Users/carrot/Desktop/POPPER/p
```

### H01: A1g_Voltage_Correlation
```
cannot import name 'ModelProfile' from 'langchain_core.language_models' (/opt/miniconda3/lib/python3.13/site-packages/langchain_core/language_models/__init__.py)
Traceback (most recent call last):
  File "/Users/carrot/Desktop/POPPER/run_all_20_hypotheses.py", line 216, in run_single_hypothesis
    from popper.agent import SequentialFalsificationTest
  File "/Users/carrot/Desktop/POPPER/popper/__init__.py", line 1, in <module>
    from .popper import Popper
  File "/Users/carrot/Desktop/POPPER/p
```

### H03: ID_IG_High_Voltage
```
cannot import name 'ModelProfile' from 'langchain_core.language_models' (/opt/miniconda3/lib/python3.13/site-packages/langchain_core/language_models/__init__.py)
Traceback (most recent call last):
  File "/Users/carrot/Desktop/POPPER/run_all_20_hypotheses.py", line 216, in run_single_hypothesis
    from popper.agent import SequentialFalsificationTest
  File "/Users/carrot/Desktop/POPPER/popper/__init__.py", line 1, in <module>
    from .popper import Popper
  File "/Users/carrot/Desktop/POPPER/p
```

### H04: Eg_Amplitude
```
cannot import name 'ModelProfile' from 'langchain_core.language_models' (/opt/miniconda3/lib/python3.13/site-packages/langchain_core/language_models/__init__.py)
Traceback (most recent call last):
  File "/Users/carrot/Desktop/POPPER/run_all_20_hypotheses.py", line 216, in run_single_hypothesis
    from popper.agent import SequentialFalsificationTest
  File "/Users/carrot/Desktop/POPPER/popper/__init__.py", line 1, in <module>
    from .popper import Popper
  File "/Users/carrot/Desktop/POPPER/p
```

### H06: Edge_Center_Uniformity
```
cannot import name 'ModelProfile' from 'langchain_core.language_models' (/opt/miniconda3/lib/python3.13/site-packages/langchain_core/language_models/__init__.py)
Traceback (most recent call last):
  File "/Users/carrot/Desktop/POPPER/run_all_20_hypotheses.py", line 216, in run_single_hypothesis
    from popper.agent import SequentialFalsificationTest
  File "/Users/carrot/Desktop/POPPER/popper/__init__.py", line 1, in <module>
    from .popper import Popper
  File "/Users/carrot/Desktop/POPPER/p
```

### H05: Spatial_Decoupling
```
cannot import name 'ModelProfile' from 'langchain_core.language_models' (/opt/miniconda3/lib/python3.13/site-packages/langchain_core/language_models/__init__.py)
Traceback (most recent call last):
  File "/Users/carrot/Desktop/POPPER/run_all_20_hypotheses.py", line 216, in run_single_hypothesis
    from popper.agent import SequentialFalsificationTest
  File "/Users/carrot/Desktop/POPPER/popper/__init__.py", line 1, in <module>
    from .popper import Popper
  File "/Users/carrot/Desktop/POPPER/p
```

### H07: A1g_Width
```
cannot import name 'ModelProfile' from 'langchain_core.language_models' (/opt/miniconda3/lib/python3.13/site-packages/langchain_core/language_models/__init__.py)
Traceback (most recent call last):
  File "/Users/carrot/Desktop/POPPER/run_all_20_hypotheses.py", line 216, in run_single_hypothesis
    from popper.agent import SequentialFalsificationTest
  File "/Users/carrot/Desktop/POPPER/popper/__init__.py", line 1, in <module>
    from .popper import Popper
  File "/Users/carrot/Desktop/POPPER/p
```

### H08: Gband_Redshift
```
cannot import name 'ModelProfile' from 'langchain_core.language_models' (/opt/miniconda3/lib/python3.13/site-packages/langchain_core/language_models/__init__.py)
Traceback (most recent call last):
  File "/Users/carrot/Desktop/POPPER/run_all_20_hypotheses.py", line 216, in run_single_hypothesis
    from popper.agent import SequentialFalsificationTest
  File "/Users/carrot/Desktop/POPPER/popper/__init__.py", line 1, in <module>
    from .popper import Popper
  File "/Users/carrot/Desktop/POPPER/p
```

### H09: Dband_Time_Delay
```
cannot import name 'ModelProfile' from 'langchain_core.language_models' (/opt/miniconda3/lib/python3.13/site-packages/langchain_core/language_models/__init__.py)
Traceback (most recent call last):
  File "/Users/carrot/Desktop/POPPER/run_all_20_hypotheses.py", line 216, in run_single_hypothesis
    from popper.agent import SequentialFalsificationTest
  File "/Users/carrot/Desktop/POPPER/popper/__init__.py", line 1, in <module>
    from .popper import Popper
  File "/Users/carrot/Desktop/POPPER/p
```

### H10: Spatial_Autocorrelation
```
cannot import name 'ModelProfile' from 'langchain_core.language_models' (/opt/miniconda3/lib/python3.13/site-packages/langchain_core/language_models/__init__.py)
Traceback (most recent call last):
  File "/Users/carrot/Desktop/POPPER/run_all_20_hypotheses.py", line 216, in run_single_hypothesis
    from popper.agent import SequentialFalsificationTest
  File "/Users/carrot/Desktop/POPPER/popper/__init__.py", line 1, in <module>
    from .popper import Popper
  File "/Users/carrot/Desktop/POPPER/p
```

### H11: Voltage_Fade
```
cannot import name 'ModelProfile' from 'langchain_core.language_models' (/opt/miniconda3/lib/python3.13/site-packages/langchain_core/language_models/__init__.py)
Traceback (most recent call last):
  File "/Users/carrot/Desktop/POPPER/run_all_20_hypotheses.py", line 216, in run_single_hypothesis
    from popper.agent import SequentialFalsificationTest
  File "/Users/carrot/Desktop/POPPER/popper/__init__.py", line 1, in <module>
    from .popper import Popper
  File "/Users/carrot/Desktop/POPPER/p
```

### H12: Capacity_Retention
```
cannot import name 'ModelProfile' from 'langchain_core.language_models' (/opt/miniconda3/lib/python3.13/site-packages/langchain_core/language_models/__init__.py)
Traceback (most recent call last):
  File "/Users/carrot/Desktop/POPPER/run_all_20_hypotheses.py", line 216, in run_single_hypothesis
    from popper.agent import SequentialFalsificationTest
  File "/Users/carrot/Desktop/POPPER/popper/__init__.py", line 1, in <module>
    from .popper import Popper
  File "/Users/carrot/Desktop/POPPER/p
```

### H13: Oxygen_Release
```
cannot import name 'ModelProfile' from 'langchain_core.language_models' (/opt/miniconda3/lib/python3.13/site-packages/langchain_core/language_models/__init__.py)
Traceback (most recent call last):
  File "/Users/carrot/Desktop/POPPER/run_all_20_hypotheses.py", line 216, in run_single_hypothesis
    from popper.agent import SequentialFalsificationTest
  File "/Users/carrot/Desktop/POPPER/popper/__init__.py", line 1, in <module>
    from .popper import Popper
  File "/Users/carrot/Desktop/POPPER/p
```

### H14: Temperature_Dependence
```
cannot import name 'ModelProfile' from 'langchain_core.language_models' (/opt/miniconda3/lib/python3.13/site-packages/langchain_core/language_models/__init__.py)
Traceback (most recent call last):
  File "/Users/carrot/Desktop/POPPER/run_all_20_hypotheses.py", line 216, in run_single_hypothesis
    from popper.agent import SequentialFalsificationTest
  File "/Users/carrot/Desktop/POPPER/popper/__init__.py", line 1, in <module>
    from .popper import Popper
  File "/Users/carrot/Desktop/POPPER/p
```

### H15: Cation_Mixing
```
cannot import name 'ModelProfile' from 'langchain_core.language_models' (/opt/miniconda3/lib/python3.13/site-packages/langchain_core/language_models/__init__.py)
Traceback (most recent call last):
  File "/Users/carrot/Desktop/POPPER/run_all_20_hypotheses.py", line 216, in run_single_hypothesis
    from popper.agent import SequentialFalsificationTest
  File "/Users/carrot/Desktop/POPPER/popper/__init__.py", line 1, in <module>
    from .popper import Popper
  File "/Users/carrot/Desktop/POPPER/p
```

### H16: CEI_Steady_State
```
cannot import name 'ModelProfile' from 'langchain_core.language_models' (/opt/miniconda3/lib/python3.13/site-packages/langchain_core/language_models/__init__.py)
Traceback (most recent call last):
  File "/Users/carrot/Desktop/POPPER/run_all_20_hypotheses.py", line 216, in run_single_hypothesis
    from popper.agent import SequentialFalsificationTest
  File "/Users/carrot/Desktop/POPPER/popper/__init__.py", line 1, in <module>
    from .popper import Popper
  File "/Users/carrot/Desktop/POPPER/p
```

### H17: Rate_Capability
```
cannot import name 'ModelProfile' from 'langchain_core.language_models' (/opt/miniconda3/lib/python3.13/site-packages/langchain_core/language_models/__init__.py)
Traceback (most recent call last):
  File "/Users/carrot/Desktop/POPPER/run_all_20_hypotheses.py", line 216, in run_single_hypothesis
    from popper.agent import SequentialFalsificationTest
  File "/Users/carrot/Desktop/POPPER/popper/__init__.py", line 1, in <module>
    from .popper import Popper
  File "/Users/carrot/Desktop/POPPER/p
```

### H18: Discharge_Reversibility
```
cannot import name 'ModelProfile' from 'langchain_core.language_models' (/opt/miniconda3/lib/python3.13/site-packages/langchain_core/language_models/__init__.py)
Traceback (most recent call last):
  File "/Users/carrot/Desktop/POPPER/run_all_20_hypotheses.py", line 216, in run_single_hypothesis
    from popper.agent import SequentialFalsificationTest
  File "/Users/carrot/Desktop/POPPER/popper/__init__.py", line 1, in <module>
    from .popper import Popper
  File "/Users/carrot/Desktop/POPPER/p
```

### H19: Electrolyte_Decomposition
```
cannot import name 'ModelProfile' from 'langchain_core.language_models' (/opt/miniconda3/lib/python3.13/site-packages/langchain_core/language_models/__init__.py)
Traceback (most recent call last):
  File "/Users/carrot/Desktop/POPPER/run_all_20_hypotheses.py", line 216, in run_single_hypothesis
    from popper.agent import SequentialFalsificationTest
  File "/Users/carrot/Desktop/POPPER/popper/__init__.py", line 1, in <module>
    from .popper import Popper
  File "/Users/carrot/Desktop/POPPER/p
```

### H20: Mn_Dissolution
```
cannot import name 'ModelProfile' from 'langchain_core.language_models' (/opt/miniconda3/lib/python3.13/site-packages/langchain_core/language_models/__init__.py)
Traceback (most recent call last):
  File "/Users/carrot/Desktop/POPPER/run_all_20_hypotheses.py", line 216, in run_single_hypothesis
    from popper.agent import SequentialFalsificationTest
  File "/Users/carrot/Desktop/POPPER/popper/__init__.py", line 1, in <module>
    from .popper import Popper
  File "/Users/carrot/Desktop/POPPER/p
```
