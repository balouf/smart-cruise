# Models

Generation of static (i.e. time-invariant) discrete cost models for energy consumption.

## Terminology Mapping

The model uses abstract terminology that maps to domain-specific concepts:

| Model term          | Aircraft | UAV | AUV | Ground vehicle |
|---------------------|----------|-----|-----|----------------|
| **height**          | Flight level | Altitude | Depth | Terrain elevation |
| **weight**          | Fuel remaining | Battery charge | Battery charge | Fuel/battery level |
| **track point**     | Distance segment | Distance segment | Distance segment | Road segment |
| **up / down**       | Climb / descent | Climb / descent | Ascent / descent | Uphill / downhill |
| **speed ratio**     | Mach number | Airspeed ratio | Water-speed ratio | Vehicle-speed ratio |

The "height" dimension represents any discrete state variable that affects energy consumption
(altitude, depth, elevation, etc.). The "weight" dimension represents remaining energy
(fuel mass, battery charge, etc.) which may itself affect consumption efficiency.

The public API historically used ``waypoint``, ``mac`` and ``climb_matrix``. The canonical names
are now ``track_point``, ``unit_speed`` and ``up_matrix``. The previous public names remain
available during a transition period through deprecated aliases.

```{eval-rst}
.. automodule:: smart_cruise.models
    :members:
```
