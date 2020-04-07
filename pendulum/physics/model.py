import sympy as sym
from sympy.physics import mechanics
from typing import List


class Model:
    def __init__(self, n: int):
        if n < 1:
            raise ValueError('The number of pendulums cannot be less than 1')

        self.n = n

        # Generic variables
        g, t = sym.symbols('g t')

        self.gravity = g

        # Pendulum characteristics (masses and lengths) - arrays
        masses = sym.symbols('m:{0}'.format(n))
        lengths = sym.symbols('l:{0}'.format(n))

        self.masses = list(masses)
        self.lengths = list(lengths)

        # Variables: theta - angle, omega - angular velocity
        theta = mechanics.dynamicsymbols('theta:{0}'.format(n))
        omega = mechanics.dynamicsymbols('omega:{0}'.format(n))

        self.angles = list(theta)
        self.velocities = list(omega)

        # Registering the time derivative of the angle, later to be
        # identified as the angular velocity
        d_theta = mechanics.dynamicsymbols('theta:{0}'.format(n), level=1)

        # Describing the reference frame - world coordinate system and the pivot
        frame = mechanics.ReferenceFrame('Oxy')
        origin = mechanics.Point('O')
        # The origin is fixed in the reference frame
        origin.set_vel(frame, 0 * frame.x + 0 * frame.x)

        particles = []
        forces = []
        kinematic_odes = []

        pivot = origin
        for i in range(n):
            # Local coordinate system
            local = frame.orientnew('A{0}'.format(i),
                                    rot_type='axis', amounts=[theta[i], frame.z])
            pendulum = pivot.locatenew('P{0}'.format(i),
                                       lengths[i] * local.x)

            # Instead of rotating the pendulum,
            # we'll fix the pivot (origin or previous pendulum) and the
            # current pendulum, and rotate the coordinate system
            local.set_ang_vel(frame, omega[i] * frame.z)
            pendulum.v2pt_theory(pivot, frame, local)

            # Creating the particle
            particle = mechanics.Particle('Pa{0}'.format(i),
                                          pendulum, masses[i])
            particles.append(particle)
            kinematic_odes.append(d_theta[i] - omega[i])

            gravity = masses[i] * g * frame.x
            forces.append((pendulum, gravity))

            # We set the pivot for the next pendulum as the current pendulum
            pivot = pendulum

        kanes = mechanics.KanesMethod(frame, q_ind=theta, u_ind=omega,
                                      kd_eqs=kinematic_odes)
        fr, fr_star = kanes.kanes_equations(particles, forces)
        self.kanes = kanes
        self.fr = fr
        self.fr_star = fr_star
