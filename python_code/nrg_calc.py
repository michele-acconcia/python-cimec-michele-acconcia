# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 00:52:28 2025

@author: accon
"""
import numpy as np
from scipy.stats import gaussian_kde


def nrg_calc(data,events,nMSD,nTR):
    
    """
    Inputs
    data = data organised as TIME x NODES
    events = onsets for different events - list of TRs associated with each event type
    nMSD = maximum MSD range
    nTR = number of TRs to track
    
    Outputs
    nrg = TR x MSD array containing energy values
    """
    
    MSD_range = np.arange(nMSD+1)
    TR_range = range(nTR)
    nrg = np.zeros([nTR,nMSD+1])
    
    for TR in TR_range:
        MSD = np.mean((data[TR+1:,:] - data[:-1-TR,:])**2, axis=1)
        MSD_events = MSD[events]
        
        #Calculate probability and energy at each TR
        kde = gaussian_kde(MSD_events, bw_method=4) #the bandwith 4 is hard,
        # code in the original script (and also reported in the paper formula)
        #but they don't seem to justify it in anyway
        
        # Evaluate PDF at all points in the range
        pdf_vals = kde(MSD_range)
        
        nrg_TR = -1*np.log(pdf_vals)
        
        #Pool results across time
        nrg[TR,:] = nrg_TR
        
    return nrg