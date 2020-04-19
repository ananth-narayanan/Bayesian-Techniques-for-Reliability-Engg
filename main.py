# Import relevant libraries
import pandas as pd
from bayesian_ab_beta import Bayesian_ab_beta
from datasimulator import datasimulator
from preparedata import *
from chi2 import Chi2

#Edit values below
survival_sim=[0.25,0.50,0.75,0.85,0.95, 0.97] #Simulation survival rates
random_seed = True # Set to False if you want to get repeatable results
survival_test =[0.95, 0.97] # Two values for Chi2 and Bayesian AB test
batchsize=[12,12]
#Uninformed priors for Bayesian AB testing, all values set to 1
priors=[[1,1]]*len(survival_test)


# Do not edit code below if you are not familiar with python
data_sim=datasimulator(survival_sim, random_seed)

if len(survival_test)==2:
    chi2_data =preparedata_chi2(data_sim, survival_test)
    chi2_batchsize=dict(zip(survival_test, batchsize))
    Chi2(chi2_data, chi2_batchsize).calculate()

bayesian_data, beta_params=preparedata_bayes(data_sim, survival_test, priors)
Bayesian_ab_beta(bayesian_data, beta_params).calculate()
