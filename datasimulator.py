#import relevant python libraries
import numpy as np
import pandas as pd
import random

def datasimulator(factors, random_seed=False):
    if random_seed==False:
        seeds=np.arange(1,len(factors)+1)*10
    else:
        seeds=np.random.randint(1,100,len(factors)+1)

    # Total number of samples to simulate for each probability
    n_samples=1000

    # Create an empty Dataframe to store data
    df=pd.DataFrame([], columns=['seed','survival_rate','random_number','outcome'])

    for key, val in enumerate(factors): # Loop through the factors list to simulate data for each condition
      random.seed(seeds[key]) # Set unique seed for each factors rate


      rand = [random.random() for r in range(n_samples)] #Generate random number array which has the size of n_samples
      df_subset=pd.DataFrame([], columns=['seed','survival_rate','random_number','outcome']) # Create an empty Dataframe to store the data each iteration

      df_subset['random_number'] = rand
      df_subset['seed'] = seeds[key]
      df_subset['survival_rate'] = val
      df_subset['outcome'] = 0
      df_subset['outcome']=(df_subset['survival_rate']>df_subset['random_number']).astype(int) # Outcome is 1 if survival rate> random number
      df = pd.concat([df, df_subset], axis=0)

    #Write the simulated data to csv file for future use
    df.to_csv('data\simulated_data.csv')
    return df
