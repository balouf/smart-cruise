# Models

Generation of static (i.e. time-invariant) discrete cost models for energy consumption.

## Terminology Mapping

The model uses abstract terminology that maps to domain-specific concepts:

| Model term | Aircraft | UAV | AUV | Ground vehicle |
|------------|----------|-----|-----|----------------|
| **height** | Flight level | Altitude | Depth | Terrain elevation |
| **weight** | Fuel remaining | Battery charge | Battery charge | Fuel/battery level |
| **waypoint** | Distance segment | Distance segment | Distance segment | Road segment |
| **speed** | Mach number | Airspeed | Water speed | Vehicle speed |

The "height" dimension represents any discrete state variable that affects energy consumption
(altitude, depth, elevation, etc.). The "weight" dimension represents remaining energy
(fuel mass, battery charge, etc.) which may itself affect consumption efficiency.

```{eval-rst}
.. automodule:: opti_cruise.models
    :members:
```
