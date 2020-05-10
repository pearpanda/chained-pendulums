import numpy as np


def times_arange(start, end, dt):
    return dt, np.arange(start, end, dt)


def times_linspace(start, end, count):
    return (end-start) / count, np.linspace(start, end, count)
