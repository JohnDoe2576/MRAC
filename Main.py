from Parameters import *
from Generate_Data import *
from MRAC_Sim import *
from Plot_Data import *

import matplotlib.pyplot as plt
import pickle as pkl

# ----------------------------------------------------------------------------
#                                   Parameters
# ----------------------------------------------------------------------------
# 
# Parameters for time vector
time = Parameters(t0=0., dt=0.05, t1=50.)

# Parameters for excitation signal
alpha = Parameters(low=-6., high=6.)            # APRBS amplitude range
tau = Parameters(low=1, high=0.5/time.dt)       # APRBS delay range
excite = Parameters(alpha=alpha, tau=tau)       # Excitation signal parameters

# Parameters for plant object
model = Robotic_Arm()                           # Plant model
coeff = Parameters(p1=2., p2=-10., p3=1.)       # Coefficients of plant model
ic = [0., 0.]                                   # Initial conditions

# Parameters required to save generated plant data
filename = "RA_Dat"
fileno = "001"
dat_par = Parameters(filename=filename, fileno=fileno)

# Parameters required to generate plant data
sys_par = Parameters(model=model, coeff=coeff, ic=ic)

# Plot parameters required to create input-output plot
title="Input-Output data"
legend=['u', 'y']
xlabel = 't [s]'
plot_uy = Plot_Data(title=title, legend=legend, xlabel=xlabel)

# ----------------------------------------------------------------------------
#                               Data generation
# ----------------------------------------------------------------------------
# 
# Instantiate simulation object that is used to decide on what simulation to do
plant = MRAC_Sim(time=time, excite=excite, sys_par=sys_par, dat_par=dat_par)

# Load previously generated data
#t,u,y = plant.load_data()

# Generate input-output data required for plant training
t,u,y = plant.gen_data()

# Plot input-output data
plot_uy.plot_twin(t,u,y)