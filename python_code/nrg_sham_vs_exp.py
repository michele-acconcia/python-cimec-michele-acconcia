# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 22:27:20 2025

@author: accon
"""

from pathlib import Path
from scipy.io import loadmat
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from nrg_calc import nrg_calc

#%% Import and convert data
data_path = Path(r"path\to\sample_data")
exp_path_list = list(data_path.glob('*exp*.mat'))
sham_path_list = list(data_path.glob('*sham*.mat'))

#Data is stored in '.mat' files from the lab's preprocessing pipeline
#It needs to be converted in numpy and then concatenated

#Convert data 
exp_list = []
for subj in exp_path_list:
    data_dict = loadmat(subj)
    data = data_dict[list(data_dict.keys())[-1]]
    exp_list.append(data)
    
sham_list = []
for subj in sham_path_list:
    data_dict = loadmat(subj)
    data = data_dict[list(data_dict.keys())[-1]]
    sham_list.append(data)
    
#%% Analysis

#Set params

#The following events are taken as a reference point to calculate energy, 
#in resting state "random" points are selected
#in the original code they select one time point every 20, I kept it as that
events = np.arange(0,np.shape(exp_list[0])[0],20)
nMSD = 10 #maximum MSD to consider for energy calculation
nTR = 5 #maximum TR in the future (from every reference point) for which calculate MSD
#Considering the maximum distance from a reference point (5) and the distance
#between each reference point (20), a lot of data ends up being unused
#I don't if that' by design

#Calculate energy landscape over group
exp_nrg = [nrg_calc(subj,events,nMSD,nTR) for subj in exp_list]
exp_nrg = np.stack(exp_nrg, axis=2) 

sham_nrg = [nrg_calc(subj,events,nMSD,nTR) for subj in sham_list]
sham_nrg = np.stack(sham_nrg, axis=2)
    
#Compare energy landscape between groups
t_stat, p_val = stats.ttest_ind(exp_nrg,sham_nrg, axis=2)

#%% Figure 1, mean energy of each group

#Compute mean energy to plot
exp_nrg_mean = np.mean(exp_nrg,axis=2)
sham_nrg_mean = np.mean(sham_nrg, axis= 2)

#Initialize figure
X,Y = np.meshgrid(np.arange(nMSD+1),np.arange(nTR))
fig, axes = plt.subplots(1, 2, figsize=(12, 5), subplot_kw={"projection": "3d"})

#Plot experimental group mean
exp_ax = axes[0]

exp_ax.plot_wireframe(X, Y, exp_nrg_mean, rstride=1, cstride=1, 
                      color=np.array([105, 173, 132]) / 255.0, linewidth=0.6)
exp_ax.set_xlabel("TR")
exp_ax.set_ylabel("MSD")
exp_ax.set_zlabel("Energy")
exp_ax.view_init(elev=30, azim=-120)
exp_ax.set_title("Average exp landscape")

#Plot sham group mean
sham_ax = axes[1]

sham_ax.plot_wireframe(X, Y, sham_nrg_mean, rstride=1, cstride=1, 
                      color=np.array([105, 173, 132]) / 255.0, linewidth=0.6)
sham_ax.set_xlabel("TR")
sham_ax.set_ylabel("MSD")
sham_ax.set_zlabel("Energy")
sham_ax.view_init(elev=30, azim=-120)
sham_ax.set_title("Average sham landscape")

#%%Figure 2, difference between experimental and sham group

#Compute mean difference
nrg_mean_diff = exp_nrg_mean - sham_nrg_mean

fig, ax = plt.subplots(figsize=(12, 5), subplot_kw={"projection": "3d"})

ax.plot_wireframe(X, Y, nrg_mean_diff, rstride=1, cstride=1, 
                      color=np.array([105, 173, 132]) / 255.0, linewidth=0.6)
ax.set_xlabel("TR")
ax.set_ylabel("MSD")
ax.set_zlabel("Energy")
ax.view_init(elev=30, azim=-120)
ax.set_title("experimental - sham landscape")