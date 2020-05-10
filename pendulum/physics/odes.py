from typing import Callable
import sympy as sym
import numpy as np

from pendulum.physics.model import Model


class ODEs:
    mm_func: Callable
    fo_func: Callable

    def __init__(self, model: Model):
        variables = model.angles + model.velocities
        parameters = [model.gravity] + model.masses + model.lengths

        # Dummy symbols
        unknowns = [sym.Dummy() for i in variables]
        unknown_dict = dict(zip(variables, unknowns))

        kds = model.kanes.kindiffdict()
        mm_full_symbols = model.kanes.mass_matrix_full.subs(kds).subs(unknown_dict)
        fo_full_symbols = model.kanes.forcing_full.subs(kds).subs(unknown_dict)

        self.mm_func = sym.lambdify(unknowns + parameters,
                                    mm_full_symbols)
        self.fo_func = sym.lambdify(unknowns + parameters,
                                    fo_full_symbols)

    def __call__(self, t: np.ndarray, y: np.ndarray, *args, **kwargs):
        inputs = np.concatenate((y, *args))
        sol = np.linalg.solve(self.mm_func(*inputs), self.fo_func(*inputs))
        return np.array(sol).T[0]


def generate_odes(pendulum_count: int):
    odes = ODEs(Model(pendulum_count))
    return odes
