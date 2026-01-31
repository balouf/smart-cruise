from dataclasses import dataclass

import numpy as np
from matplotlib import pyplot as plt

from smart_cruise.jit import compute

#: Default weight budget.
W0 = 26000.0

#: Default time budget.
T0 = 26000.0

#: Default backoff for changing speed.
BACKOFF = 9

#: Default discretization of the Pareto front of individual states.
PARETO_MAX = 30


class Trajectories:
    """
    Handler class for optimal trajectories.

    Parameters
    ----------
    trajs: :class:`~numpy.ndarray`
        :math:`n_t \\times n_d` array of :math:`(h, s, w, t)` states.
    n_h: :class:`int`
        Number of heights (for normalization).
    n_s: :class:`int`
        Number of speeds (for normalization).
    """

    def __init__(self, trajs, n_h, n_s):
        self.trajs = trajs
        self.n_h = n_h
        self.n_s = n_s

    def get_traj(self, i):
        """
        Get trajectory profile.

        Parameters
        ----------
        i: :class:`int`
            Index of trajectory.

        Returns
        -------
        h: :class:`~numpy.ndarray`
        s: :class:`~numpy.ndarray`
        w: :class:`~numpy.ndarray`
        t: :class:`~numpy.ndarray`
        """
        h = np.array([t[0] for t in self.trajs[i, :]]) / self.n_h
        s = np.array([t[1] for t in self.trajs[i, :]]) / self.n_s
        w = np.array([t[2] for t in self.trajs[i, :]]) / self.trajs[0, 0][2]
        t = np.array([t[3] for t in self.trajs[i, :]]) / self.trajs[0, 0][3]
        return h, s, w, t

    def plot_traj(self, i):
        """
        Display trajectory profile.

        Parameters
        ----------
        i: :class:`int`
            Index of trajectory.

        Returns
        -------
        None
        """
        h, s, w, t = self.get_traj(i)
        plt.plot(h, label="Height")
        plt.plot(s, label="Speed")
        plt.plot(w, label="Remaining Energy")
        plt.plot(t, label="Spare Time")
        plt.ylim([0, 1])
        plt.xlim([0, len(h) - 1])
        plt.legend()
        plt.show()

    def get_front(self):
        """
        Get Pareto front.

        Returns
        -------
        w: :class:`~numpy.ndarray`
        t: :class:`~numpy.ndarray`
        """
        w = np.array([t[2] for t in self.trajs[:, -1]], dtype=float)
        t = np.array([t[3] for t in self.trajs[:, -1]], dtype=float)
        return w, t

    def plot_front(self):
        """
        Display Pareto front.

        Returns
        -------
        None
        """
        w, t = self.get_front()
        plt.plot(w, t)
        plt.xlabel("Remaining energy")
        plt.ylabel("Spare time")
        plt.xlim([0, None])
        plt.ylim([0, None])
        plt.show()


@dataclass
class CruiseParameters:
    """
    Attributes
    ----------

    backoff: :class:`int`, default=BACKOFF
        Timer to change speed.
    pareto_max: :class:`int`, default=PARETO_MAX
        Max number of pareto-optimal points per state.
    """

    backoff: int = BACKOFF
    pareto_max: int = PARETO_MAX


class Cruise:
    """

    Parameters
    ----------
    model: :class:`~opti_cruise.models.CostModel`
        The cost model.
    parameters: :class:`~opti_cruise.opti_cruise.CruiseParameters`
        Simulation parameters.

    Examples
    --------

    >>> from smart_cruise import CostRandom
    >>> model = CostRandom(n_d=100, seed=42)
    >>> cruise = Cruise(model)
    >>> cruise.parameters.pareto_max = 5
    >>> cruise.compute()
    >>> w, t = cruise.trajectories.get_front()

    Weight optimal values:

    >>> f"Weight: {w[0]:.2f}, time: {t[0]:.2f}"
    'Weight: 23160.79, time: 21102.36'

    Time optimal values:
    >>> f"Weight: {w[-1]:.2f}, time: {t[-1]:.2f}"
    'Weight: 20938.41, time: 22734.91'
    """

    def __init__(self, model=None, parameters=None):
        self.model = model
        if parameters is None:
            parameters = CruiseParameters()
        self.parameters = parameters
        self.trajectories = None

    def compute(self, w0=W0, t0=T0):
        trajectories = compute(
            [(w0, t0)],
            backoff=self.parameters.backoff,
            pareto_max=self.parameters.pareto_max,
            **self.model.dict,
        )
        self.trajectories = Trajectories(
            trajectories,
            n_s=len(self.model.timings),
            n_h=self.model.cruise_matrix.shape[1],
        )
