from typing import Iterable, List
import numpy as np

from pendulum.physics import Solver
from pendulum.model import Pendulum


class Result:
    def __init__(self, solver: Solver, times, pendulums):
        sol = solver.solve(times)
        lengths = []
        for p in pendulums:
            lengths.append(p.length)
        self.lengths = np.array(lengths)
        self.angles = sol[:, 0:len(pendulums)]
        self.velocities = sol[:, len(pendulums)+1:2*len(pendulums)]


class PendulumPositions:
    def __init__(self, result: Result):
        self.x_coords = np.cumsum(-np.sin(result.angles) * result.lengths[np.newaxis, :], axis=1)
        self.y_coords = np.cumsum(-np.cos(result.angles) * result.lengths[np.newaxis, :], axis=1)

