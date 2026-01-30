import numpy as np
from dataclasses import dataclass, asdict

#: Default number of heights
N_H = 8
#: Default number of waypoints
N_D = 600
#: Default number of speeds
N_S = 7
#: Default min speed (in *mach*)
S_MIN = 0.6
#: Default max speed (in *mach*)
S_MAX = 0.9
#: Default waypoint length (in *km*)
WAYPOINT = 10.0
#: Default Mach speed (in *km/s*)
MAC = 0.3403
#: Default speed cost (additional speed cost is :math:`S * s^2`)
SPEED_COST = 50.0
#: Default base cost
CRUISE_COST = 20.0
#: Default climbing cost
CLIMB_COST = 100.0
#: Default climbing (down) gain
DOWN_GAIN = 25.0
#: Default cost reduction due to height
HEIGHT_GAIN = 3.0
#: Default weight that increases cost by 1
INVERSE_WEIGHT = 4000.0


@dataclass
class CostModel:
    """
    Energy consumption and time cost(s) depending on various parameters.
    All values are expressed in units per waypoint.

    The model is generic and applies to any vehicle with state-dependent energy costs.
    "Height" represents any discrete state dimension (altitude, depth, elevation, etc.),
    and "weight" represents remaining energy (fuel, battery charge, etc.).

    Attributes
    ----------

    timings: :class:`~numpy.ndarray`
        Time to travel the waypoint w.r.t. speed index.
    speed_array: :class:`~numpy.ndarray`
        Energy cost to travel the waypoint w.r.t. speed index.
    cruise_matrix: :class:`~numpy.ndarray`
        Base cost w.r.t. waypoint and height indices.
    climb_matrix: :class:`~numpy.ndarray`
        Cost to increase height w.r.t. waypoint and height indices.
    down_matrix: :class:`~numpy.ndarray`
        Gain from decreasing height w.r.t. waypoint and height indices.
    height_gain: :class:`float`
        Cost reduction w.r.t. height index.
    weight_cost: :class:`float`
        Cost modifier w.r.t. remaining energy (spare weight).
    """

    timings: np.ndarray
    speed_array: np.ndarray
    cruise_matrix: np.ndarray
    climb_matrix: np.ndarray
    down_matrix: np.ndarray
    height_gain: float
    weight_cost: float

    @property
    def dict(self):
        return asdict(self)


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
        Number of waypoints.
    n_s: :class:`int`, optional
        Number of speed levels.
    s_min: :class:`float`, optional
        Minimum speed (default: Mach 0.6 for aircraft).
    s_max: :class:`float`, optional
        Maximum speed (default: Mach 0.9 for aircraft).
    waypoint: :class:`float`, optional
        Waypoint length (in km).
    mac: :class:`float`, optional
        Reference speed (default: Mach 1 in km/s for aircraft).
    speed_cost: :class:`float`, optional
        Energy cost coefficient for speed.
    cruise_cost: :class:`float`, optional
        Base energy cost per waypoint.
    climb_cost: :class:`float`, optional
        Energy cost for increasing height/state.
    down_gain: :class:`float`, optional
        Energy recovered when decreasing height/state.
    height_gain: :class:`float`, optional
        Efficiency improvement from higher states.
    inverse_weight: :class:`float`, optional
        Energy level at which cost increases by 1 unit.
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
        waypoint=WAYPOINT,
        mac=MAC,
        speed_cost=SPEED_COST,
        cruise_cost=CRUISE_COST,
        climb_cost=CLIMB_COST,
        down_gain=DOWN_GAIN,
        height_gain=HEIGHT_GAIN,
        inverse_weight=INVERSE_WEIGHT,
        seed=None,
    ):
        if seed is not None:
            np.random.seed(seed)
        speeds = np.linspace(s_min, s_max, n_s)
        timings = waypoint / mac / speeds
        speed_array = speed_cost * speeds**2
        cruise_matrix = cruise_cost * (0.5 + np.random.rand(n_d, n_h))
        climb_matrix = climb_cost * (0.5 + np.random.rand(n_d, n_h))
        down_matrix = down_gain * (0.5 + np.random.rand(n_d, n_h))
        super().__init__(
            timings=timings,
            speed_array=speed_array,
            cruise_matrix=cruise_matrix,
            climb_matrix=climb_matrix,
            down_matrix=down_matrix,
            height_gain=height_gain,
            weight_cost=1 / inverse_weight,
        )
