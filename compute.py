from typing import List, Callable, Union
from pathlib import Path
import numpy as np

from pendulum.physics import ODEs, Solver
from pendulum.physics.odes import generate_odes
from pendulum.io import Result, loaders


def save(result: Result, path: Union[Path, str]):
    result.save(path)


def compute(masses: np.ndarray,
            lengths: np.ndarray,
            initial_angles: np.ndarray,
            initial_velocities: np.ndarray,
            times: np.ndarray, odes: Callable):
    solver = Solver(odes, masses, lengths, initial_angles, initial_velocities)

    result = solver.solve(times)
    return result


def determine_chained_count(pendulums: np.ndarray):
    """Given a numpy array representing a pendulum chain, determine how many pendulums there are in it"""
    return pendulums.shape[1]


if __name__ == '__main__':
    # TODO: Check whether command line arguments can be passed
    pendulum_path = input()
    initial_states_path = input()
    time_path = input()
    out_path = input()

    ps = loaders.load_pendulum_file(pendulum_path)
    iss = loaders.load_states_file(initial_states_path)
    ts = loaders.load_times_file(time_path)

    chained_count = determine_chained_count(ps)
    ang_accelerations = generate_odes(chained_count)

    res = compute(ps[0, :], ps[1, :],  iss[0, :], iss[1, :], ts, ang_accelerations)
    save(res, out_path)

