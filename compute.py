from pydantic import ValidationError
import numpy as np
import matplotlib.pyplot as plt

from pendulum.model.input import loaders
from pendulum.physics import Model, ODEs, Solver
from pendulum.model.result import Result, PendulumPositions


def main():
    # TODO: Add prompts to these input statements
    file_path = input()
    time_path = input()
    out_path = input()
    try:
        pendulums, initial_states = loaders.load_frame(file_path)
        model = Model(len(pendulums))
        solver = Solver(ODEs(model), pendulums, initial_states)

        times = loaders.load_times_file(time_path)

        result = Result(solver, times, pendulums)
        positions = PendulumPositions(result)
        plt.plot(positions.x_coords, positions.y_coords)
        plt.show()

    except ValidationError as e:
        print(e)


if __name__ == '__main__':
    # TODO: Check whether command line arguments can be passed
    main()
