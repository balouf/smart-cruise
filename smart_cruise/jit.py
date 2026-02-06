import numpy as np
from numba import njit
from numba.typed import List
from numba.core import config as numba_config


@njit
def new_state_dict():
    """
    Creates empty state dict

    Returns
    -------
    :class:`~numba.typed.Dict`
        A Numba typed dict (h, s, b) -> [(w, t, p)].
    """
    return {(1, 2, 3): List([(1.0, 2.0, 3)]) for _ in range(0)}


@njit
def insert_state(states, h, s, b, w, t, p):
    """
    Defaultdict-like state insertion.

    Parameters
    ----------
    states: :class:`~numba.typed.Dict`
        A Numba typed dict (h, s, b) -> [(w, t, p)].
    h: :class:`int`
        Height index.
    s: :class:`int`
        Speed index.
    b: :class:`int`
        Backoff.
    w: :class:`float`
        Weight.
    t: :class:`float`
        Time.
    p: :class:`int`
        Index of origin state.

    Returns
    -------
    None
    """
    if w > 0 and t > 0:
        if (h, s, b) in states:
            states[h, s, b].append((w, t, p))
        else:
            states[h, s, b] = List([(w, t, p)])


np_rec = np.dtype([("h", "i8"), ("s", "i8"), ("w", "f8"), ("t", "f8")])

if numba_config.DISABLE_JIT:
    # Pure Python mode: use numpy dtypes directly
    wt_type = np.dtype([("f0", "f8"), ("f1", "f8")])
    state_type = np.dtype(
        [("h", "i8"), ("s", "i8"), ("b", "i8"), ("w", "f8"), ("t", "f8"), ("p", "i8")]
    )
    nb_rec = np_rec
else:
    # JIT mode: use Numba types
    from numba import typeof, from_dtype

    wt_type = typeof((1.0, 2.0))
    state_type = typeof((1, 2, 3, 4.0, 5.0, 6))
    nb_rec = from_dtype(np_rec)


@njit
def pareto_collapse(states, pareto_max):
    """
    Parameters
    ----------
    states: :class:`~numba.typed.Dict`
        A Numba typed dict (h, s, b) -> [(w, t, p)].
    pareto_max: :class:`int`
        Maximum number of pareto points.

    Returns
    -------
    None
    """
    for state, wtp in states.items():
        keys = np.empty(len(wtp), dtype=wt_type)
        for i, x in enumerate(wtp):
            keys[i] = (-x[0], -x[1])
        indices = np.argsort(keys)
        wtp0 = wtp[indices[0]]
        res = List([wtp0])
        tm = wtp0[1]
        for i in indices[1:]:
            t = wtp[i][1]
            if t > tm:
                res.append(wtp[i])
                tm = t

        # Sample if needed
        if len(res) > pareto_max:
            res = List(
                [res[round(y)] for y in np.linspace(0, len(res) - 1, pareto_max)]
            )
        states[state] = res


@njit
def compute(
    start,
    timings,
    speed_array,
    cruise_matrix,
    climb_matrix,
    down_matrix,
    height_gain,
    weight_cost,
    backoff,
    pareto_max,
):
    """
    Core computation of optimal trajectories.

    Parameters
    ----------
    start: :class:`list`
        Initial (weight, time) budgets.
    timings: :class:`~numpy.ndarray`
        Time cost per speed level.
    speed_array: :class:`~numpy.ndarray`
        Speed cost adjustments.
    cruise_matrix: :class:`~numpy.ndarray`
        Base energy cost matrix (waypoint x height).
    climb_matrix: :class:`~numpy.ndarray`
        Energy cost for climbing one height level.
    down_matrix: :class:`~numpy.ndarray`
        Energy gain for descending one height level.
    height_gain: :class:`float`
    weight_cost: :class:`float`
    backoff: :class:`int`
    pareto_max: :class:`int`
    """
    waypoint = np.empty(len(start), dtype=state_type)
    for i, wt in enumerate(start):
        waypoint[i] = (0, 0, 0, *wt, 0)
    waypoints = [waypoint]
    n_d, n_h = cruise_matrix.shape
    n_s = len(speed_array)
    # One waypoint after the other
    for i in range(n_d):
        # new state dict
        states = new_state_dict()
        # Browse states of current waypoint and processes their successors
        for p, state in enumerate(waypoints[i]):
            h, s, b, w, t, _ = state
            base_cost = cruise_matrix[i, h] - h * height_gain + w * weight_cost
            c = climb_matrix[i, h]
            d = down_matrix[i, h]
            bb = max(0, b - 1)
            ww = w - max(0.0, base_cost + speed_array[s])
            tt = t - timings[s]
            insert_state(states, h, s, bb, ww, tt, p)
            if h < n_h - 1:
                insert_state(states, h + 1, s, bb, ww - c, tt, p)
            if h > 0:
                insert_state(states, h - 1, s, bb, ww + d, tt, p)
            if b == 0:
                for ss in range(n_s):
                    if ss != s:
                        ww = w - max(0.0, base_cost + speed_array[ss])
                        tt = t - timings[ss]
                        insert_state(states, h, ss, backoff, ww, tt, p)
                        if h < n_h - 1:
                            insert_state(states, h + 1, ss, backoff, ww - c, tt, p)
                        if h > 0:
                            insert_state(states, h - 1, ss, backoff, ww + d, tt, p)
        pareto_collapse(states, pareto_max=pareto_max)
        n_states = sum([len(v) for v in states.values()])
        waypoint = np.empty(n_states, dtype=state_type)
        index = 0
        for k, vv in states.items():
            for v in vv:
                waypoint[index] = (*k, *v)
                index += 1
        waypoints.append(waypoint)

    # Global Pareto-reduction of last waypoint
    last = waypoints[-1]
    if len(last) == 0:
        return None
    keys = np.empty(len(last), dtype=wt_type)
    for i, x in enumerate(last):
        keys[i] = (-x[3], -x[4])
    indices = np.argsort(keys)
    ends = [last[indices[0]]]
    tm = last[indices[0]][4]
    for i in indices[1:]:
        state = last[i]
        if state[4] > tm:
            ends.append(state)
            tm = state[4]

    # Convert to trajectory array
    n_traj = len(ends)
    trajectories = np.empty((n_traj, n_d + 1), dtype=nb_rec)
    for i, end in enumerate(ends):
        trajectories[i, -1]["h"] = end[0]
        trajectories[i, -1]["s"] = end[1]
        trajectories[i, -1]["w"] = end[3]
        trajectories[i, -1]["t"] = end[4]
        pos = end[5]
        for j in range(n_d - 1, -1, -1):
            state = waypoints[j][pos]
            trajectories[i, j]["h"] = state[0]
            trajectories[i, j]["s"] = state[1]
            trajectories[i, j]["w"] = state[3]
            trajectories[i, j]["t"] = state[4]
            pos = state[5]

    return trajectories
