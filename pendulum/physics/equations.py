from sympy.physics import mechanics

from pendulum.physics.model import Model


def print_equations(model: Model, pretty_print: bool) -> None:
    mass_mat = model.kanes.mass_matrix
    forcing_mat = model.kanes.forcing
    rhs = mass_mat.inv() * forcing_mat
    kdd = model.kanes.kindiffdict()
    rhs = rhs.subs(kdd)
    rhs.simplify()
    if pretty_print:
        mechanics.mpprint(rhs)
    else:
        mechanics.mprint(rhs)
