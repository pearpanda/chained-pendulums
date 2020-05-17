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
