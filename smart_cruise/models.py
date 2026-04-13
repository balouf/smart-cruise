from dataclasses import asdict, dataclass

import numpy as np
import warnings
from dataclasses import dataclass, asdict

#: Default number of heights
N_H = 8
#: Default number of track-point
N_D = 600
#: Default number of speeds
N_S = 7
#: Default min speed ratio (relative to the reference speed unit)
S_MIN = 0.6
#: Default max speed ratio (relative to the reference speed unit)
S_MAX = 0.9
#: Default track-point length (in *km*)
TRACK_POINT = 10.0
#: Deprecated alias for :data:`TRACK_POINT`.
WAYPOINT = TRACK_POINT
#: Default reference speed unit (Mach 1 for aircraft, in *km/s*)
UNIT_SPEED = 0.3403
#: Deprecated alias for :data:`UNIT_SPEED`.
MAC = UNIT_SPEED
#: Default speed cost (additional speed cost is :math:`S * s^2`)
SPEED_COST = 50.0
#: Default base cost
CRUISE_COST = 20.0
#: Default upward maneuver cost
UP_COST = 100.0
#: Deprecated alias for :data:`UP_COST`.
CLIMB_COST = UP_COST
#: Default downward maneuver gain
DOWN_GAIN = 25.0
#: Default cost reduction due to height
HEIGHT_GAIN = 3.0
#: Default weight that increases cost by 1
INVERSE_WEIGHT = 4000.0


@dataclass
class CostModel:
    """
    Energy consumption and time cost(s) depending on various parameters.
    All values are expressed in units per track point.

    The model is generic and applies to any vehicle with state-dependent energy costs.
    "Height" represents any discrete state dimension (altitude, depth, elevation, etc.),
    and "weight" represents remaining energy (fuel, battery charge, etc.).

    Attributes
    ----------

    timings: :class:`~numpy.ndarray`
        Time to travel the track point w.r.t. speed index.
    speed_array: :class:`~numpy.ndarray`
        Energy cost to travel the track point w.r.t. speed index.
    cruise_matrix: :class:`~numpy.ndarray`
        Base cost w.r.t. track point and height indices.
    up_matrix: :class:`~numpy.ndarray`
        Cost to increase height w.r.t. track point and height indices.
    down_matrix: :class:`~numpy.ndarray`
        Gain from decreasing height w.r.t. track point and height indices.
    height_gain: :class:`float`
        Cost reduction w.r.t. height index.
    weight_cost: :class:`float`
        Cost modifier w.r.t. remaining energy (spare weight).
    """

    timings: np.ndarray
    speed_array: np.ndarray
    cruise_matrix: np.ndarray
    up_matrix: np.ndarray
    down_matrix: np.ndarray
    height_gain: float
    weight_cost: float

    @property
    def dict(self):
        return asdict(self)

    @property
    def climb_matrix(self):
        warnings.warn(
            "`climb_matrix` is deprecated; use `up_matrix`.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.up_matrix

class CostRandom(CostModel):
    """
    A simple cost model with global parameters and randomized terrain.

    Default parameters are tuned for aircraft cruise, but the model
    generalizes to any vehicle. Adapt parameters for your domain.

    Parameters
    ----------
    n_h: :class:`int`, optional
        Number of height/state steps.
    n_d: :class:`int`, optional
        Number of track points.
    n_s: :class:`int`, optional
        Number of speed levels.
    s_min: :class:`float`, optional
        Minimum speed ratio relative to the reference speed unit.
    s_max: :class:`float`, optional
        Maximum speed ratio relative to the reference speed unit.
    track_point: :class:`float`, optional
        Track point length (in km).
    unit_speed: :class:`float`, optional
        Reference speed unit (Mach 1 in km/s for aircraft).
    speed_cost: :class:`float`, optional
        Energy cost coefficient for speed.
    cruise_cost: :class:`float`, optional
        Base energy cost per track point.
    up_cost: :class:`float`, optional
        Energy cost for increasing height/state.
    down_gain: :class:`float`, optional
        Energy recovered when decreasing height/state.
    height_gain: :class:`float`, optional
        Efficiency improvement from higher states.
    inverse_weight: :class:`float`, optional
        Energy level at which cost increases by 1 unit.
    waypoint: :class:`float`, optional
        Deprecated alias for ``track_point``.
    mac: :class:`float`, optional
        Deprecated alias for ``unit_speed``.
    climb_cost: :class:`float`, optional
        Deprecated alias for ``up_cost``.
    seed: :class:`int`, optional
        Random seed for reproducible terrain generation.
    """

    def __init__(
        self,
        n_h=N_H,
        n_d=N_D,
        n_s=N_S,
        s_min=S_MIN,
        s_max=S_MAX,
        track_point=TRACK_POINT,
        unit_speed=UNIT_SPEED,
        speed_cost=SPEED_COST,
        cruise_cost=CRUISE_COST,
        up_cost=UP_COST,
        down_gain=DOWN_GAIN,
        height_gain=HEIGHT_GAIN,
        inverse_weight=INVERSE_WEIGHT,
        seed=None,
        *,
        waypoint=None,
        mac=None,
        climb_cost=None,
    ):
        if waypoint is not None:
            warnings.warn(
                "`waypoint` is deprecated; use `track_point`.",
                DeprecationWarning,
                stacklevel=2,
            )
            track_point = waypoint
        if mac is not None:
            warnings.warn(
                "`mac` is deprecated; use `unit_speed`.",
                DeprecationWarning,
                stacklevel=2,
            )
            unit_speed = mac
        if climb_cost is not None:
            warnings.warn(
                "`climb_cost` is deprecated; use `up_cost`.",
                DeprecationWarning,
                stacklevel=2,
            )
            up_cost = climb_cost
        if seed is not None:
            np.random.seed(seed)
        speeds = np.linspace(s_min, s_max, n_s)
        timings = track_point / unit_speed / speeds
        speed_array = speed_cost * speeds**2
        cruise_matrix = cruise_cost * (0.5 + np.random.rand(n_d, n_h))
        up_matrix = up_cost * (0.5 + np.random.rand(n_d, n_h))
        down_matrix = down_gain * (0.5 + np.random.rand(n_d, n_h))
        super().__init__(
            timings=timings,
            speed_array=speed_array,
            cruise_matrix=cruise_matrix,
            up_matrix=up_matrix,
            down_matrix=down_matrix,
            height_gain=height_gain,
            weight_cost=1 / inverse_weight,
        )
