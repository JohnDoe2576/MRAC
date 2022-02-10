import numpy as np
import pandas as pd
import pickle as pkl
import bz2 

class Data_Handler:
    
    def __init__(self, dat_par):
        self.filename = dat_par.filename
        self.fileno = dat_par.fileno

    def loaddata(self):
        # Open file object
        comp_file = self.filename + "_" + self.fileno + ".bz2"
        f = bz2.BZ2File(comp_file, 'rb')

        # Unpickle data
        dat = pkl.load(f)
        f.close()

        # Extracting data
        t = np.array(dat['t'])
        u = np.array(dat['u'])
        y = np.array(dat['y'])

        # Return obtained data
        return t,u,y

    def savedata(self, t, u, y):
        # Plug data in pandas DataFrame
        dat = pd.DataFrame({'t':t, 'u':u, 'y':y})

        # Compress using bzip2 format
        comp_file = self.filename + "_" + self.fileno + ".bz2"
        f = bz2.BZ2File(comp_file, 'wb')

        # Pickle data
        pkl.dump(dat, f)
        f.close()

    def cal_psd( x, **parms ):
        # Assumptions:
        # 1. 'x' is a 2D array of data measured/sampled at unformly spaced 
        #    instants. The data measured/sampled from a particular channel 
        #    is given along axis0, and channel numbering is given along 
        #    axis1.
        # 2. In all cases, the code returns PSD in the positive direction 
        #    of f-axis, and then doubling the energy in it to account for 
        #    the energy inthe negative direction of f-axis. This is based 
        #    on an assumption of typical symmetries of PSD(-f) = PSD(+f). 
        #    Also note that, in the event that 'x' is complex, x(-f) ~= x(f).
        # 3. Each channel data is divided into blocks of size 'nfft'with a 
        #    'overlap_pcnt' percentage of overlap between them, and the PSD 
        #    over each of the blocks are averaged. Furthermore, to avoid a 
        #    situation where few samples being unused towards the end, the 
        #    overlap between last and last-but-one block can be larger.
        # 4. PSD has units ((Unit of 'x')^**2)/(\Delta Hz). '\Delta Hz' 
        #    is a reflection of the fact that PSD is the density per unit 
        #    width of the frequency bins. In other words, \int {(PSD) (df)} 
        #    is the power of the signal irrespective of frequency parameters 
        #    like 'nfft' or 'fs'
        # 
        # Input parameters:
        #    x: Time-series (2D array)
        #    nfft: Frequency points used to calculate DFT
        #    fs: Sampling frequency
        #    window: Windowing function
        #    overlap_pcnt: Percentage overlap between successive blocks
        # 
        # Output parameters:
        #    PSD: Power Spectral Density in ((Units of x) ** 2)/(Delta Hz)
        #    f: Frequency axis

        # Extracting parameters
        nfft = parms['nfft']                    # Number of frequency points
        fs = parms['fs']                        # Sampling frequency
        window = parms['window']                # Windowing function
        overlap_pcnt = parms['ovlp_pcnt']       # Percentage of overlap

        # Get windowing function and weights (for normalization later)
        dat_wndw = np.diag(window(nfft))
        wndw_weight = np.mean(np.power(dat_wndw,2))

        # Return distinct non-negative frequencies less than Nyquist
        nfrq = int(np.ceil((nfft+1)/2))

        # Create frequency axis
        f = np.arange(0,nfrq,1)*(fs/nfft)

        # Samples to overlap between successive blocks
        noverlap = 0.01 * nfft * overlap_pcnt

        # Samples by which one block is shifted from next
        blk_shift = nfft - noverlap

        # Number of samples
        n_smpl = len(x)

        # Number of blocks to average over
        nblks = np.ceil((n_smpl - noverlap)/blk_shift)

        # Calculating Power Spectral Density
        # ----------------------------------
        # 
        # Pre-initializng PSD matrix
        PSD = np.zeros(x.shape)
        PSD = PSD[0:nfft,]

        for blk in range(0,int(nblks)):
            # Starting index of each block
            blk_strt_idx = int(min([(blk*blk_shift + nfft), n_smpl]) - nfft)

            # Indices of current block
            blk_curr_idx = np.arange(0,int(nfft),dtype='int16') + blk_strt_idx

            # Convolve window function with each block and take the Fourier transform
            p_f = np.fft.fft(np.matmul(dat_wndw,x[blk_curr_idx,]),n=nfft,axis=0)

            # Add square of DFT to running sum
            PSD = PSD + np.power( np.abs(p_f), 2 )

        # Average out values from all blocks
        PSD = PSD/nblks

        # Account for neglected energy (Refer Assumption 2)
        # -------------------------------------------------
        # 
        # Axis folding: 
        # 1. Selecting positive frequency axis 
        # 2. Knocking-off 'Zero' and 'Nyquist' frequencies
        nfrq_pos = int(np.floor((nfft+1)/2) - 1)
        nfrq_pos_idx = np.array(range(0,nfrq_pos))

        # Double the energy (Assumption 2)
        PSD[(1+nfrq_pos_idx),] = PSD[(1+nfrq_pos_idx),] + PSD[(-1+1)-nfrq_pos_idx]
    
        # Crucial normalizations
        # ----------------------
        # 
        # 1. Make PSD independent of frequency parameters: 'fs' & 'nfft'
        # 2. Account for windowing
        PSD = PSD[0:nfrq,]/(nfft*fs*wndw_weight)

        # Return frequency axis and calculated PSD
        return f,PSD