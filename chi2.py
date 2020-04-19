# The objective of this code is to demonstrate a/b testing techniques for Reliability Engineers
# This code could help even Reliability Engineers and Machine learning professionals to visualize the
# difference between frequentist and Bayesian techniques in a/b testing

#Import relevant python libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import scipy
from scipy import stats
import math

class Chi2():
    def __init__(self, df, batchsize):
        self.df=df
        self.batchsize=batchsize

    def calculate(self):
        try:
            if self.df.shape[1]!=2 or len(self.batchsize)!=2:
                raise ValueError('Lengths of survival_rate and batchsize must be =2')
        except ValueError as ve:
            print(ve)

        try:
            if min(list(self.df.nunique()))==0:
                raise ValueError('One or more columns in dataframe is empty')
        except ValueError as ve:
            print(ve)

        [a_key, b_key]= list(self.batchsize.keys())
        a = self.df.loc[:,a_key]
        b = self.df.loc[:,b_key]

        nRuns=math.floor(min(a.shape[0]/self.batchsize[a_key] , b.shape[0]/self.batchsize[b_key]))
        a_end=-1
        b_end=-1
        Cumm_P_val=np.zeros(nRuns) # This variable shows cummulative P Value

        # Loop to find cummulative P value, by increasing sample size in each run
        for i in range(nRuns):
            a_end  = a_end + self.batchsize[a_key]
            b_end  = b_end + self.batchsize[b_key]
            a_pass=a[0:a_end].sum()
            a_fail=self.batchsize[a_key]*(i+1)- a[0:a_end].sum()
            b_pass=b[0:b_end].sum()
            b_fail=self.batchsize[b_key]*(i+1)- b[0:b_end].sum()
            ContingencyTable= np.array([[a_pass,a_fail],[b_pass,b_fail]])
            if np.min(ContingencyTable)==0:
                # P value cannot be determined if one or more values in the ContingencyTable is zero
                Cumm_P_val[i] = np.nan
            else:
                (chi1,Cumm_P_val[i],DOF,expected)=stats.chi2_contingency(ContingencyTable, correction=False)

        #Plot cummulative p values for all runs
        x=(np.arange(1,nRuns+1))
        Cumm_P_val=pd.DataFrame(list(zip(x,Cumm_P_val)), columns=['N_runs','Cummulative_P_Value'])
        Cumm_P_val=Cumm_P_val.dropna()


        ax=Cumm_P_val.plot(x='N_runs', y='Cummulative_P_Value', grid=True, label='p value' )
        plt.plot(np.ones(np.max(x))*0.05, color ='red', ls="--", label='alpha=0.05')
        ax.set_title("Chi2 Results")
        ax.set_xlabel('N Runs')
        ax.set_ylabel('P Value')
        ax.set_xticks(np.arange(0, nRuns+1, 10))
        ax.legend()
        def run2samples(x):
            return x * (self.batchsize[a_key]+self.batchsize[b_key])


        def samples2run(x):
            return x / (self.batchsize[a_key]+self.batchsize[b_key])

        secax = ax.secondary_xaxis('top', functions=(run2samples, samples2run))
        secax.set_xlabel('Total Samples tested')
        #secax.set_xticks(np.arange(0, (nRuns+1)*(self.batchsize[a_key]+self.batchsize[b_key]), 10))
        plt.show()
        return None
