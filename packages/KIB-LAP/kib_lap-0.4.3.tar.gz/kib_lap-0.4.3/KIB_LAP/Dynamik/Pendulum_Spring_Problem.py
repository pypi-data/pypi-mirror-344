import numpy as np
from math import sin, cos
from matplotlib import pyplot as plt
from Pendulum_Spring_Linearized import TwoMassesSpring_Lin

class TwoMassesSpringRopeRK4:
    def __init__(self):
        # geometry / material
        self.r = 5
        E = 30000e6
        A = 10*10
        I = 1e3 * 10 / 12
        l = 30
        rho = 2500

        # stiffness
        self.k_1 = 3 * E * I / l**3

        # masses
        self.m_1 = rho * A * l * 0.75
        self.m_2 = 5**3 * 7850

        # gravity
        self.g = 9.81  

        # damping coefficients (you can tweak these)
        self.c_x   = 0    # [N·s/m]
        self.c_phi =  0    # [N·m·s/rad]

        # initial state
        self.x1_0   = 0.0
        self.phi_0  = 30/180*np.pi
        self.xd1_0  = 0.0
        self.phid_0 = 0.0

        # time grid
        self.dt      = 1e-3
        self.T_ges   = 10.0
        self.N_steps = int(self.T_ges / self.dt)

    def construct_mass_matrix(self, phi):
        m11 = self.m_1 + self.m_2
        m12 = self.m_2 * self.r * cos(phi)
        m21 = m12
        m22 = self.m_2 * self.r**2
        return np.array([[m11, m12],
                         [m21, m22]])

    def construct_forces(self, state):
        """Returns total generalized force F = F_spring + F_gravity + F_damp + F_centrifugal."""
        x1, phi, xd1, phid = state

        # spring
        F_spring = np.array([-self.k_1 * x1,
                              0.0])

        # gravity on the pendulum mass
        F_grav   = np.array([0.0,
                              -self.m_2 * self.g * self.r * sin(phi)])

        # geometric (centrifugal) term from the rope
        F_geo    = np.array([ self.m_2 * self.r * phid**2 * sin(phi),
                               0.0 ])

        # viscous damping C · [xd1, phid]
        F_damp   = -np.array([ self.c_x   * xd1,
                               self.c_phi * phid ])

        return F_spring + F_grav + F_geo + F_damp

    def equations_of_motion(self, state):
        x1, phi, xd1, phid = state
        M = self.construct_mass_matrix(phi)
        F = self.construct_forces(state)
        # solve for accelerations
        xdd1, phidd = np.linalg.solve(M, F)
        return np.array([ xd1,      # ẋ₁
                          phid,     # φ̇
                          xdd1,     # ẍ₁
                          phidd ])  # φ̈

    def RK4_step(self, state):
        k1 = self.equations_of_motion(state)
        k2 = self.equations_of_motion(state + 0.5 * self.dt * k1)
        k3 = self.equations_of_motion(state + 0.5 * self.dt * k2)
        k4 = self.equations_of_motion(state +     self.dt * k3)
        return state + (self.dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)

    def solve(self):
        state = np.array([self.x1_0,
                          self.phi_0,
                          self.xd1_0,
                          self.phid_0])

        time       = []
        x1_list    = []
        phi_list   = []
        xd1_list   = []
        phid_list  = []
        xdd1_list  = []
        phidd_list = []

        for i in range(self.N_steps):
            # record current
            time.append(i * self.dt)
            x1_list.append(state[0])
            phi_list.append(state[1])
            xd1_list.append(state[2])
            phid_list.append(state[3])

            # compute acceleration at this state
            deriv = self.equations_of_motion(state)
            xdd1_list.append(deriv[2])
            phidd_list.append(deriv[3])

            # march one step
            state = self.RK4_step(state)

        return {
            't':       np.array(time),
            'x1':      np.array(x1_list),
            'phi':     np.array(phi_list),
            'xd1':     np.array(xd1_list),
            'phid':    np.array(phid_list),
            'xdd1':    np.array(xdd1_list),
            'phidd':   np.array(phidd_list),
        }








