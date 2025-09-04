#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 16:48:40 2025

@author: macconcia
"""

import numpy as np
from sklearn.neighbors import KernelDensity


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
    
    MSD_range = np.arange(nMSD+1).reshape(-1,1)
    TR_range = range(nTR)
    nrg = np.zeros([nTR,nMSD+1])
    
    for TR in TR_range:
        MSD = np.mean((data[TR+1:,:] - data[:-1-TR,:])**2, axis=1)
        MSD_events = MSD[events].reshape(-1,1)
        
        ##Calculate probability and energy at each TR
        #Fit the kernel density
        kde = KernelDensity(kernel="gaussian", bandwidth=4).fit(MSD_events) #the bandwith 4 is hard coded in the original script 
        #(and also reported in the paper formula) but they don't seem to justify it in anyway
        
        #Evaluate PDF at all points in the range
        pdf_vals = np.exp(kde.score_samples(MSD_range))
        
        #Calculate energy at TR
        nrg_TR = -1*np.log(pdf_vals)
        
        #Pool results across time
        nrg[TR,:] = nrg_TR
        
    return nrg