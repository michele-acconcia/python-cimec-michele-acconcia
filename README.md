python-cimec-michele-acconcia
======
This repository contains python code to perform egocentric energy landscape analysis, described in [Munn et al., 2021](https://www.nature.com/articles/s41467-021-26268-x) and [Taylor et al., 2024](https://www.sciencedirect.com/science/article/pii/S2211124724006879?via%3Dihub). The original code (from which the present code is adapted) is in MATLAB (from [Taylor et al., 2024](https://www.sciencedirect.com/science/article/pii/S2211124724006879?via%3Dihub)). The original scripts are provided for reference in the `original_matlab_code` directory.

The `python_code` directory contains the python code to perform the analysis, which assumes fMRI ROI data stored in .mat files for two groups (experimental and sham). The `nrg_sham_vs_exp.py` script computes the energy landscapes for the two groups and compares them. To calculate the energy landscape the `nrg_calc.py` is used, and to properly run the code this file should be added to your python path. To test the code sample data is provided (note, however, that it was randomly generated so the results will make no sense)

## Energy landscape

Using a dynamical system framework, the brain can be represented as a system in a state space defined by its activity. The state space can be represented as an energy landscape, where points visited more probably by the system are defined as low-energy (sometimes also refered to as attractors), while points visited more probably are defined as high-energy. For a more in depth introduction of dynamical system theory in neuroimaging see [Yohan et al.,2022](https://direct.mit.edu/netn/article/6/4/960/109066/It-s-about-time-Linking-dynamical-systems-with).

