#Import relevant python libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import scipy
from scipy import stats
import math
from expected_loss import *
import scipy.special as sc

#Define Bayesian_ab_beta class
class Bayesian_ab_beta():
    def __init__(self, df, beta_params):
        self.df=df
        self.beta_params=beta_params
#Error handling
#Check if number of columns in the dataframe matches the length of beta_params


    def calculate(self):
        try:
            pass
            if self.df.shape[1] != len(self.beta_params):
                raise ValueError('Invalid input,  no. of columns in df must match the length of self.beta_params')
        except ValueError as ve:
            print(ve)

    #Check if any of the columns in the dataframe is empty
        try:
            pass
            if min(list(self.df.nunique()))==0:
                raise ValueError('One or more columns in dataframe is empty')
        except ValueError as ve:
            print(ve)


        factors=list(self.beta_params.keys()) # get the list of factors
        loss=[]
        all_mu=[]
        self.df=self.df[factors] # reorganize columns so they are in the same order as beta_params
        df_row=dict(zip(factors,np.zeros(len(factors)).astype(int)))# initialize current row for each factor as 0
        df_max_row=dict(zip(factors,list(self.df.count(0)))) # maximum observations for each factor
        run_flag=True
        plot_id=1
        x = np.linspace(0, 1, 200)

        # Run A/B testing
        while(run_flag):

            maxbeta=-1
            rand_beta_max=-1
            best_factor=None
            for key, val in self.beta_params.items():
                rand_beta=np.random.beta(val[0],val[1])
                if rand_beta>rand_beta_max:
                    rand_beta_max=rand_beta
                    best_factor=key
            outcome=self.df[best_factor].iloc[df_row[best_factor]]
            a= self.beta_params[best_factor][0]+ outcome
            b= self.beta_params[best_factor][1]+1 -outcome
            self.beta_params[best_factor]=[a,b]
            df_row[best_factor] = df_row[best_factor] +1
            run_flag=(np.array(list(df_max_row.values()))-np.array(list(df_row.values()))).min()>0
            max_plots=max(list(df_max_row.values()))

            #Update expected values of mu and loss function
            if len(factors)==2:
                [a_temp1, b_temp1]=self.beta_params[factors[0]]
                [a_temp2, b_temp2]=self.beta_params[factors[1]]
                betas=[sc.beta(a_temp1, b_temp1), sc.beta(a_temp2, b_temp2)]
                all_mu.append([a_temp1/(a_temp1+ b_temp1), a_temp2/(a_temp2+ b_temp2)])

                if betas[1]>=betas[0]:
                    mu2=factors[1]
                    mu1=factors[0]

                else:
                    mu2=factors[0]
                    mu1=factors[1]

                [a1,b1]=self.beta_params[mu1]
                [a2,b2]=self.beta_params[mu2]
                loss.append(exp_loss(a1,b1,a2,b2))

            plot_tests = np.linspace(max_plots/10, max_plots, 5)
            plot_tests =np.floor(plot_tests)
            n_plots=len(plot_tests)

            #plot pdfs
            if int(sum(df_row.values()))in set(plot_tests) or run_flag==False:
                fig = plt.subplot(math.ceil((n_plots+1)/2), 2,  plot_id)
                plot_id=plot_id+1
                for key,val in self.beta_params.items():
                    y = scipy.stats.beta.pdf(x, val[0], val[1])
                    plt.plot(x,y, label=key)
                    plt.title('Samples tested: ' + str(df_row))
                    plt.legend()
                plt.grid()
                plt.xlabel('Total samples tested')
                plt.ylabel('pdf')
                plt.tight_layout()
        plt.show()
        #Plot expected values of mu and loss
        if len(factors)==2:

            x=np.arange(len(loss))+1
            mu_val=pd.DataFrame(all_mu, columns=factors)
            f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
            ax1.plot(loss, label ='expected value of loss')


            ax1.set_ylabel('E(Loss)')
            ax1.plot(np.ones(len(loss))*0.005, color ='red', ls='--', label='Tol =0.005')
            ax1.grid()
            ax1.set_yscale('log')
            ax2.plot(mu_val)
            ax2.set_ylabel('E(mu)')
            ax2.grid()
            ax1.legend()
            ax2.legend(factors)
            ax2.set_xlabel('No. Iterations')
            plt.tight_layout()
            plt.show()

        return None
