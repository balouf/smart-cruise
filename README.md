# Smart Cruise


[![PyPI Status](https://img.shields.io/pypi/v/smart-cruise.svg)](https://pypi.python.org/pypi/smart-cruise)
[![Build Status](https://github.com/balouf/smart-cruise/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/balouf/smart-cruise/actions?query=workflow%3Abuild)
[![Documentation Status](https://github.com/balouf/smart-cruise/actions/workflows/docs.yml/badge.svg?branch=main)](https://github.com/balouf/smart-cruise/actions?query=workflow%3Adocs)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Coverage](https://codecov.io/gh/balouf/smart-cruise/branch/main/graphs/badge.svg)](https://codecov.io/gh/balouf/smart-cruise/tree/main)

Find Pareto-optimal cruise trajectories to optimize energy consumption and travel time.


- Free software: MIT
- Documentation: <https://balouf.github.io/smart-cruise/>.
- Github: <https://github.com/balouf/smart-cruise>


## Features

- Find Pareto-optimal cruise trajectories balancing energy consumption and travel time.
- Dynamic programming with multi-objective Pareto optimization.
- JIT-compiled core engine for fast computation.
- Customizable cost models for different scenarios.
- Trajectory visualization tools.

## Theoretical Foundations

This package implements the multi-objective dynamic programming framework described in:

> **Bui-Xuan, Mathieu, Tighilt** (2026). *La croisière s'amuse*. _submitted to_ Algotel 2026.

Main model assumptions:
- **Dominance preservation (H1)**: Any resource advantage at step d can be maintained through transitions
- **Lipschitz continuity (H2)**: Small perturbations lead to bounded output changes

**Complexity**: O(n² log n) for 2 objectives with constant precision, vs. exponential for exact Pareto front

The `pareto_max` parameter (denoted S in the paper) controls the trade-off between computation time and approximation quality.


## Model Applicability

This package implements a **state-dependent multi-objective optimization** model using dynamic
programming to find Pareto-optimal trajectories. While the default parameters are tuned
for ship / aircraft cruise optimization, the underlying model applies to any vehicle where:

1. **Cruise mode exists**: A fixed trajectory is studied, which can be split in segments.
2. A set of values (e.g. time, energy) must be optimized.
3. The rest of the state description (e.g., height, speed, ...) has finite values.
4. H1 and H2 apply.

The name _Smart Cruise_ refers to optimizing any steady-state operation mode ("cruise") and is not restricted to,
for instance, just aircraft flights.

### Example Applications

| Domain | "Height" dimension    | "Energy" dimension | State dependency |
|--------|-----------------------|-------------------|------------------|
| Aircraft | Flight level/altitude | Fuel remaining | Lighter aircraft = more efficient |
| UAV | Altitude              | Battery charge | Altitude affects efficiency |
| AUV | Depth                 | Battery charge | Depth affects drag/buoyancy |
| Ground vehicle | Terrain elevation     | Fuel/battery | Elevation changes cost energy |
| Ship | Sails                 | Fuel remaining | Weight affects hull resistance |

### Scientific References

The model draws on established principles from various domains:

- **Aircraft**: The [Breguet range equation](https://web.mit.edu/16.unified/www/FALL/thermodynamics/notes/node98.html) captures state-dependent fuel consumption
- **UAV optimization**: [Fuel-weight trajectory optimization](https://pmc.ncbi.nlm.nih.gov/articles/PMC10819899/) demonstrates 25% fuel reduction through weight tracking
- **Multi-rotor UAV**: [Energy-aware path planning](https://www.nature.com/articles/s41598-025-99001-z) shows power varies with flight state
- **Fuel cell vehicles**: [Multi-dimensional DP](https://www.mdpi.com/1996-1073/15/14/5190) for global energy optimization
- **AUV trajectory**: [Energy-optimal MPC](https://arxiv.org/pdf/1906.08719) for underwater vehicle path planning

## Quickstart

Install Smart Cruise:

```console
$ pip install smart-cruise
```

Use Smart Cruise in a Python project:

```pycon
>>> from smart_cruise import CostRandom, Cruise
>>> model = CostRandom(n_d=100, seed=42)
>>> cruise = Cruise(model)
>>> cruise.parameters.pareto_max = 5
>>> cruise.compute()
>>> w, t = cruise.trajectories.get_front()
>>> f"Weight optimal: {w[0]:.2f}, Time optimal: {t[-1]:.2f}"
'Weight optimal: 22979.35, Time optimal: 22734.91'
```

## Credits

This package was created with [Cookiecutter][CC] and the [Package Helper 3][PH3] project template.

[CC]: <https://github.com/audreyr/cookiecutter>
[PH3]: <https://balouf.github.io/package-helper-3/>
