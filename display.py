import matplotlib.pyplot as plt
from pydantic import ValidationError

from pendulum.model.result import PendulumStats, Result
from pendulum.model.input import loaders

if __name__ == '__main__':
    pendulum_file = input()
    results_file = input()
    try:
        ps, _ = loaders.load_frame(pendulum_file)
        res = Result.load(results_file, ps)
        positions = res.generate_stats(x=True, y=True)
        for stats in positions:
            x = stats.x
            y = stats.y
            plt.plot(x, y)
        plt.show()
    except ValidationError as e:
        print(e)
