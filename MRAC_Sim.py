import numpy as np

from Generate_Data import *
from Data_Handler import *

class MRAC_Sim:

    def __init__(self, **kwargs):
        # Extract parameters
        self.__dict__.update(kwargs)

        # Instantiate object to generate plant data
        self.dyn_sys = Generate_Data(time=self.time, excite=self.excite, sys_par=self.sys_par)

        # Instantiate object to handle (manipulate) data
        self.dat = Data_Handler(self.dat_par)

    def gen_data(self):
        # Extract plant-data object
        dyn_sys = self.dyn_sys

        # Generate time vector
        t = dyn_sys.time_vec()

        # Generate excitation signal (APRBS)
        u = dyn_sys.aprbs(len(t))

        # Generate response of the system to external excitation
        y = dyn_sys.simulate(t, u)

        # Save generated data
        self.dat.savedata(t,u,y)

        # Return generated data
        return t,u,y

    def load_data(self):
        return self.dat.loaddata()