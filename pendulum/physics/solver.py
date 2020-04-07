from typing import List
import numpy as np
from scipy.integrate import odeint

from pendulum.model import Pendulum, PendulumState, Result
from pendulum.physics.odes import ODEs, gradient


class Solver:
    odes: ODEs

    def __init__(self, odes: ODEs,
                 pendulums: List[Pendulum],
                 initial_states: List[PendulumState],
                 g=9.81):
        self.odes = odes
        self.pendulums = pendulums

        masses = []
        lengths = []
        initial_angles = []
        initial_velocities = []
        for pend, state in zip(pendulums, initial_states):
            masses.append(pend.mass)
            lengths.append(pend.length)
            initial_angles.append(state.angle)
            initial_velocities.append(state.angular_velocity)

        self.parameters = np.array([g] + masses + lengths)
        self.initial = np.array(initial_angles + initial_velocities)

    def solve(self, times: np.ndarray):
        solved_odes = odeint(gradient, self.initial,
                             times, args=(self.odes, self.parameters),
                             tfirst=True)
        angles = solved_odes[:, 0:len(self.pendulums)].T
        velocities = solved_odes[:, len(self.pendulums) + 1: 2 * len(self.pendulums)].T
        return Result(angles, velocities, times, self.pendulums)
