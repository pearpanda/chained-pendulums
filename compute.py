from typing import List
from pydantic import ValidationError
import numpy as np
import matplotlib.pyplot as plt

from pendulum.model.input import loaders
from pendulum.physics import Model, ODEs, Solver
from pendulum.model.result import Result, PendulumStats
from pendulum.model import Pendulum, PendulumState


def compute(pendulums: List[Pendulum], initial_states: List[PendulumState],
            times: np.ndarray):
    odes = ODEs(Model(len(pendulums)))
    solver = Solver(odes, pendulums, initial_states)

    result = solver.solve(times)
    return result


if __name__ == '__main__':
    # TODO: Check whether command line arguments can be passed
    file_path = input()
    time_path = input()
    out_path = input()
    try:
        ps, iss = loaders.load_frame(file_path)
        ts = loaders.load_times_file(time_path)
        out = compute(ps, iss, ts)
        out.save(out_path)

    except ValidationError as e:
        print(e)

