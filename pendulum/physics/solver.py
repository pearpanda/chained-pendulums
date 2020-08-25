from typing import List, Callable
import numpy as np
from scipy.integrate import odeint

from pendulum.io import Result


class Solver:
    odes: Callable

    def __init__(self, odes: Callable,
                 masses: np.ndarray,
                 lengths: np.ndarray,
                 initial_angles: np.ndarray,
                 initial_velocities: np.ndarray,
                 g=9.81):
        self.odes = odes
        self.pendulum_count = len(masses)
        self.lengths = lengths

        self.parameters = np.concatenate((np.array([g]), masses, lengths))
        self.initial = np.concatenate((initial_angles, initial_velocities))

    def solve(self, times: np.ndarray):
        solved_odes = odeint(self.odes, self.initial,
                             times, args=(self.parameters,),
                             tfirst=True)
        angles = solved_odes[:, 0:self.pendulum_count].T
        velocities = solved_odes[:, self.pendulum_count::].T
        return Result(angles, velocities, times, self.lengths)
