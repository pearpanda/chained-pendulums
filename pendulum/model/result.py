from typing import Iterable, List, Union
from pathlib import Path
import numpy as np

from pendulum.model import Pendulum


class PendulumStats:
    def __init__(self, angles=None, velocities=None, x=None, y=None):
        self.angles = angles
        self.velocities = velocities
        self.x = x
        self.y = y


class Result:
    def __init__(self, angles, velocities, times, pendulums):
        self.pendulums = pendulums
        self.angles = angles
        self.velocities = velocities
        self.times = times

    def save(self, path: Union[str, Path]):
        """
        Saves the result to a file.

        NOTE: The information about the pendulums isn't stored with the
        result file, so it must be stored separately.
        NOTE: The information about the pendulums is needed to later restore
        the file
        """

        joined = np.concatenate((self.times[np.newaxis, :], self.angles,
                                 self.velocities), axis=0)
        np.savetxt(path, joined)

    @staticmethod
    def load(path: Union[str, Path], pendulums: List[Pendulum]):
        """
        Loads the previously saved result

        :param path: The path to the result saved with `save`
        :param pendulums: The pendulum system
        :return: A Result object
        """
        n = len(pendulums)
        joined = np.loadtxt(path)
        times = joined[0, :]
        angles = joined[1:(n+1), :]
        velocities = joined[(n+1):(2*n), :]
        return Result(angles, velocities, times, pendulums)

    def generate_stats(self, angles=False, angular_velocities=False,
                       x=False, y=False) -> List[PendulumStats]:
        stats = []

        pre_lengths = None
        if x or y:
            lengths = []
            for pendulum in self.pendulums:
                lengths.append(pendulum.length)
            pre_lengths = np.array(lengths)

        pre_x = None
        if x:
            sines = np.sin(self.angles)
            multiplier = sines * pre_lengths[:, np.newaxis]
            pre_x = np.cumsum(multiplier, axis=0)

        pre_y = None
        if y:
            cosines = -np.cos(self.angles)
            multiplier = cosines * pre_lengths[:, np.newaxis]
            pre_y = np.cumsum(multiplier, axis=0)

        for i in range(len(self.pendulums)):
            stats_angles = None
            stats_velocities = None
            stats_x = None
            stats_y = None

            if angles:
                stats_angles = self.angles[i, :]
            if angular_velocities:
                stats_velocities = self.velocities[i, :]
            if x:
                stats_x = pre_x[i, :]
            if y:
                stats_y = pre_y[i, :]

            stats.append(PendulumStats(stats_angles, stats_velocities,
                                       stats_x, stats_y))
        return stats
