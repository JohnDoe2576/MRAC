import numpy as np
from Dynamic_Systems import *
from scipy.interpolate import interp1d
from scipy.integrate import solve_ivp

class Generate_Data:

    def __init__(self, **kwargs):
        # This object has 
        #   1. time: Time parameters
        #   2. excite: Excitation signal (APRBS) parameters
        #   3. sys_par: Parameter required for simulating system response.
        #               It includeds 'model', 'coeff' & 'ic'
        #
        # Extract parameters
        self.__dict__.update(kwargs)

    def time_vec(self):
        return np.arange(self.time.t0, self.time.t1, self.time.dt)
    
    def aprbs(self, n_samples):
        # Generate an Amplitude modulated Pseudo-Random Binary Sequence (APRBS)
        # 
        # The Pseudo-Random Binary Sequence (PRBS) is extensively used as an
        # excitation signal for System Identification of linear systems. It is 
        # characterized by randomly delayed shifts in amplitude between a 
        # user-defined minimum and maximum. These delayed shifts are usually 
        # range-bound, and are very helpful in capturing the system behaviour 
        # close to the operating frequency of the system.
        # 
        # A nonlinear system usually will have different behaviour at different 
        # amplitudes and cannot be predicted with the princlipe of superposition. 
        # Hence, the excitation signal also need to be modified to accomodate 
        # for capturing system behaviour at different amplitudes. The APRBS is 
        # an extension of PRBS by introducing randomly delayed shifts to random 
        # levels of range-bound amplitudes (rather than between a maximum and 
        # minimum).
        # 
        # Input parameters:
        #   n_samples: Number of required samples
        #   alpha: tuple of (min_amplitude, max_amplitude)
        #   tau: tuple of (min_delay, max_delay)

        # Extract signal parameters
        tau = self.excite.tau               # Delay vector
        alpha = self.excite.alpha           # Amplitude vector
        
        # Convert to usable parameters
        tau_range = tau.high - tau.low
        alpha_range = alpha.high - alpha.low
        
        # Initialize arrays
        tau_array = np.zeros((n_samples),dtype=int)
        alpha_array = np.zeros((n_samples))
        signal = np.zeros((n_samples))
        
        # Initialize counters
        sample_count = 0
        shift_count = 0
        
        while sample_count < n_samples:
            # Generate a random shift to perturb 'tau' and 'alpha'
            tau_shift = np.random.uniform(0.0, 1.0, 1)
            alpha_shift = np.random.uniform(0.0, 1.0, 1)
            
            # Introduce the random delay such that it range bound between 'tau_min' and 'tau_max'
            tau_array[shift_count] = np.fix(tau.low + (tau_shift * tau_range) ).astype(int)
            alpha_array[shift_count] = alpha.low + (alpha_shift * alpha_range)
            
            # Update counters
            sample_count += tau_array[shift_count]
            shift_count += 1
            
        # Ensure that 'max(tau_array)' doesnot exceed 'n_samples'
        tau_array[shift_count-1] -= (sample_count - n_samples)

        # Introduce random shifts in the amplitude and delay of the signal
        idx = 0
        for i in range(0,shift_count):
            idx_tmp = idx + np.arange(0,tau_array[i],1,dtype=int)
            signal[idx_tmp] = alpha_array[i]
            idx = idx + tau_array[i]

        return signal

    def simulate(self, t, u):
        # Extract data
        model = self.sys_par.model          # System model
        p = self.sys_par.coeff              # System coefficients
        x0 = self.sys_par.ic                # System initial conditions

        # Interpolate 'u' values
        u_ip = interp1d(x=t, y=u, kind='previous')

        # Extract time-limits for simulation
        t_span = (t[0], t[-1])

        # Simulate system dynamics when subjeted to APRBS 'u'
        sol = solve_ivp(model, t_span=t_span, y0=x0, t_eval=t, args=(p, u_ip), rtol=1e-10)

        # Return output (measured state)
        return np.array(sol.y[0,:])