import pandas as pd
from datasimulator import datasimulator

def preparedata(df, survival_rate):
    try:
        final_df=pd.DataFrame([])
        empty_flag=False
        for i in survival_rate:
            temp_df=(df.loc[df['survival_rate']==i,'outcome']).reset_index(drop=True)
            if temp_df.shape[0]==0:
                empty_flag=True
            final_df=pd.concat([final_df,temp_df], axis=1)
        final_df.columns=survival_rate
        return final_df
        if empty_flag ==True:
            raise ValueError('Data not available for one of more survival rates')
    except ValueError as ve:
            print(ve)



def preparedata_bayes(df, survival_rate, priors):
    try:
        bayesian_data= preparedata(df, survival_rate)
        beta_params=dict(zip(survival_rate, bayesian_data.shape[1]*priors))
        return bayesian_data, beta_params
        if len(survival_rate)!= len(priors):
            raise ValueError('Lengths of survival_rate and batchsize must be =2')
    except ValueError as ve:
        print(ve)


def preparedata_chi2(df, survival_rate):
    try:
        chi2_data= preparedata(df, survival_rate)
        return chi2_data
        if len(survival_rate)!=2 or len(batchsize)!=2:
            raise ValueError('Lengths of survival_rate and batchsize must be =2')
    except ValueError as ve:
        print(ve)
