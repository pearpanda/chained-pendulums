import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pydantic import ValidationError

from pendulum.model.result import PendulumStats, Result
from pendulum.model.input import loaders


if __name__ == '__main__':
    pendulum_file = input()
    times_file = input()
    results_file = input()
    try:
        ps, _ = loaders.load_frame(pendulum_file)
        t = loaders.load_times_file(times_file)
        res = Result.load(results_file, ps)
        positions = res.generate_stats(x=True, y=True)

        empty_space = 1.0
        ball_radius = 0.25
        length = ball_radius
        for pen in ps:
            length += pen.length
        ylims = (-length-empty_space, ball_radius+empty_space)
        xlims = (-empty_space-length, length+empty_space)

        fig = plt.figure()
        ax = fig.add_subplot(111, autoscale_on=False, ylim=ylims, xlim=xlims)
        ax.set_aspect('equal')
        ax.grid()

        line, = ax.plot([], [], 'o-', lw=2)
        time_template = 'time = %.1fs'
        time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)


        def init():
            line.set_data([], [])
            time_text.set_text('')
            return line, time_text


        def animate(i):
            thisx = [0]
            thisy = [0]

            for stats in positions:
                thisx.append(stats.x[i])
                thisy.append(stats.y[i])

            line.set_data(thisx, thisy)
            time_text.set_text(time_template % (t[i]))
            return line, time_text

        dt = (t[1] - t[0])*1000
        ani = animation.FuncAnimation(fig, animate, frames=range(len(t)),
                                      interval=dt, blit=True, init_func=init)
        plt.show()
    except ValidationError as e:
        print(e)
