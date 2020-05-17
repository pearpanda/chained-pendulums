from typing import Union, List
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.pyplot import Axes
import matplotlib.animation as animation
import numpy as np

from pendulum.io.result import Result
from pendulum.io import loaders


class MultiAnimator:
    def __init__(self, results: List[Result], ax: Axes, ball_radius, line_width, **kwargs):
        self.parallel_count = len(results)
        self.n = results[0].pendulum_count
        self.t = results[0].times
        self.positions = []
        for result in results:
            self.positions.append(result.generate_stats(x=True, y=True))

        self.pendulum_lines = []
        for i in range(self.parallel_count):
            line, = ax.plot([], [], 'o-', lw=line_width, markersize=ball_radius)
            self.pendulum_lines.append(line)

        self.last_index = -1

    def reset(self):
        for i in range(self.parallel_count):
            self.pendulum_lines[i].set_data([], [])
        self.last_index = -1

    def __call__(self, i, *args, **kwargs):
        if i == self.last_index:
            return ()
        else:
            self.last_index = i

        for k in range(self.parallel_count):
            current_line_x = [0]
            current_line_y = [0]

            for pos in self.positions[k]:
                current_line_x.append(pos.x[i])
                current_line_y.append(pos.y[i])

            self.pendulum_lines[k].set_data(current_line_x, current_line_y)
        return self.pendulum_lines


class SingleAnimator:
    def __init__(self, result: Result, ax: Axes, ball_radius, line_width, trails=False, **kwargs):
        self.n = result.pendulum_count
        self.t = result.times
        self.positions = result.generate_stats(x=True, y=True)

        self.pendulum_line, = ax.plot([], [], 'o-', lw=line_width, markersize=ball_radius)

        self.trails = trails
        if self.trails:
            self.trail_lines = []
            self.trail_points_x = []
            self.trail_points_y = []
            self.trail_index = 0
            alpha = kwargs.get("alpha", 0.6)
            self.trail_duration = kwargs.get("trail_duration", 2.0)
            for i in range(self.n):
                trail, = ax.plot([], [], alpha=alpha, lw=ball_radius)
                self.trail_lines.append(trail)
                self.trail_points_x.append([])
                self.trail_points_y.append([])
        self.last_index = -1

    def reset(self):
        self.pendulum_line.set_data([], [])
        if self.trails:
            for i in range(self.n):
                self.trail_lines[i].set_data([], [])
                self.trail_points_x[i] = []
                self.trail_points_y[i] = []
            self.trail_index = 0
        self.last_index = -1

    def __call__(self, i, *args, **kwargs):
        if i == self.last_index:
            return ()
        else:
            self.last_index = i

        t_now = self.t[i]

        current_line_x = [0]
        current_line_y = [0]

        if self.trails:
            to_remove = 0
            t_past = self.t[self.trail_index]
            while t_now - t_past > self.trail_duration:
                to_remove += 1
                self.trail_index += 1
                t_past = self.t[self.trail_index]

            for k in range(self.n):
                for j in range(to_remove):
                    self.trail_points_x[k].pop()
                    self.trail_points_y[k].pop()
                self.trail_points_x[k].insert(0, self.positions[k].x[i])
                self.trail_points_y[k].insert(0, self.positions[k].y[i])
                self.trail_lines[k].set_data(self.trail_points_x[k], self.trail_points_y[k])

        for pos in self.positions:
            current_line_x.append(pos.x[i])
            current_line_y.append(pos.y[i])

        self.pendulum_line.set_data(current_line_x, current_line_y)
        if self.trails:
            return [self.pendulum_line, *self.trail_lines]
        return self.pendulum_line


def generate_animation(results: Union[Result, List[Result]], multi=False, show=True, trails=False, **kwargs):
    result = results[0] if multi else results
    total_length = np.sum(result.lengths)
    empty_space = kwargs.get("empty_space", total_length * 0.15)
    ball_radius = kwargs.get("ball_radius", empty_space)
    line_width = kwargs.get("line_width", 2.0)

    canvas_radius = total_length + ball_radius + empty_space
    lims = (-canvas_radius, canvas_radius)

    fig = plt.figure()
    ax = fig.add_subplot(111, autoscale_on=False, xlim=lims, ylim=lims)
    ax.set_aspect('equal')
    ax.grid()

    frame_count = len(result.times)
    dt = np.mean(np.diff(result.times))*1000

    animator = None
    if multi:
        animator = MultiAnimator(results, ax, ball_radius, line_width, **kwargs)
    else:
        animator = SingleAnimator(result, ax, ball_radius, line_width, trails, **kwargs)
    ani = animation.FuncAnimation(fig, animator, frames=frame_count,
                                  interval=dt, blit=True, init_func=animator.reset())
    if "outpath" in kwargs:
        ani.save(kwargs["outpath"])
    if show:
        plt.show()
