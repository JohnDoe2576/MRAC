import numpy as np

class Dynamic_Systems(object):

    def __init__(self):
        self.parms = None

    def __call__(self, t, x, p, u):
        return self.response(t, x, p, u)

    @staticmethod
    def response(t, x, p, u):
        raise NotImplemented

class Robotic_Arm(Dynamic_Systems):

    def __init__(self):
        super(Robotic_Arm, self).__init__()

    @staticmethod
    def response(t, x, p, u):
        # Extract system states
        x1, x2 = x

        # Model depicting system behaviour
        return np.array([x2, p.p3*u(t) + p.p2*np.sin(x1) - p.p1*x2])

class Magnetic_Levitation(Dynamic_Systems):
    def __init__(self):
        super(Magnetic_Levitation, self).__init__()

    @staticmethod
    def response(t, x, p, u):
        # Extract system states
        x1, x2 = x

        # Model depicting system behaviour
        return np.array([x2, -9.81 + ((p.p1/p.p3) * (u(t)**2 * np.sign(u(t))/x1)) - ((p.p2/p.p3)*x2)])

class Van_Der_Pol(Dynamic_Systems):
    def __init__(self):
        super(Van_Der_Pol, self).__init__()

    @staticmethod
    def response(t, x, p, u):
        # Extract system states
        x1, x2 = x

        # Model depicting system behaviour
        return np.array([x2, p.p3*u(t) - (p.p1*(x1**2 - 1)*x2 ) - (p.p2*x1)])