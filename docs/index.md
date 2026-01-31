# Welcome to Smart Cruise's documentation!

**smart-cruise** is a Python package for finding Pareto-optimal trajectories that balance
energy consumption and travel time. It uses dynamic programming with multi-objective
optimization to efficiently explore the trade-off space.

## Generic Applicability

While the default parameters are tuned for aircraft cruise optimization, the underlying
algorithm is completely generic. It applies to any vehicle or system where:

- **Cruise mode**: A steady-state operation phase exists (the "cruise" in smart-cruise)
- **2D waypoint grid**: The trajectory can be discretized into distance × state (e.g., altitude, depth, elevation)
- **State-dependent costs**: Energy consumption depends on current state and remaining energy

### Example Domains

| Domain | State dimension | Energy type | Why it works |
|--------|-----------------|-------------|--------------|
| **Aircraft** | Flight level | Fuel | Lighter plane = better fuel economy |
| **UAVs** | Altitude | Battery | Altitude affects lift efficiency |
| **AUVs** | Depth | Battery | Depth changes buoyancy/drag trade-off |
| **Ground vehicles** | Terrain elevation | Fuel/Battery | Climbing costs more than descending |
| **Ships** | - | Fuel | Hull resistance varies with displacement |

See the [README](presentation/readme.md) for scientific references supporting these applications.

:::{toctree}
:maxdepth: 2
:caption: Contents:

presentation/index
tutorials/index
reference/index
:::

# Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`
