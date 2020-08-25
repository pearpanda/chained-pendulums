from typing import Iterable, List, Union
from pathlib import Path
import numpy as np


class PendulumStats:
    def __init__(self, angles=None, velocities=None,
                 x=None, y=None, vx=None, vy=None):
        self.angles = angles
        self.velocities = velocities
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy


class Result:
    def __init__(self, angles, velocities, times, lengths):
        self.pendulum_count = len(lengths)
        self.lengths = lengths
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
    def load(path: Union[str, Path], lengths: np.ndarray):
        """
        Loads the previously saved result

        :param path: The path to the result saved with `save`
        :param lengths: The array containing the lengths of the pendulum cords
        :return: A Result object
        """
        n = lengths.shape[0]
        joined = np.loadtxt(path)
        times = joined[0, :]
        angles = joined[1:(n+1), :]
        velocities = joined[(n+1):(2*n), :]
        return Result(angles, velocities, times, lengths)

    def generate_stats(self, angles=False, angular_velocities=False,
                       x=False, y=False, vx=False, vy=False) -> List[PendulumStats]:
        stats = []

        sines = np.sin(self.angles)
        cosines = np.cos(self.angles)

        pre_x = None
        if x:
            multiplier = sines * self.lengths[:, np.newaxis]
            pre_x = np.cumsum(multiplier, axis=0)

        pre_y = None
        if y:
            multiplier = -cosines * self.lengths[:, np.newaxis]
            pre_y = np.cumsum(multiplier, axis=0)

        pre_vx = None
        if vx:
            multiplier = self.velocities * cosines * self.lengths[:, np.newaxis]
            pre_vx = np.cumsum(multiplier, axis=0)

        pre_vy = None
        if vy:
            multiplier = self.velocities * sines * self.lengths[:, np.newaxis]
            pre_vy = np.cumsum(multiplier, axis=0)

        for i in range(len(self.lengths)):
            stats_angles = None
            stats_velocities = None
            stats_x = None
            stats_y = None
            stats_vx = None
            stats_vy = None

            if angles:
                stats_angles = self.angles[i, :]
            if angular_velocities:
                stats_velocities = self.velocities[i, :]
            if x:
                stats_x = pre_x[i, :]
            if y:
                stats_y = pre_y[i, :]
            if vx:
                stats_vx = pre_vx[i, :]
            if vy:
                stats_vy = pre_vy[i, :]

            stats.append(PendulumStats(stats_angles, stats_velocities,
                                       stats_x, stats_y, stats_vx, stats_vy))
        return stats
