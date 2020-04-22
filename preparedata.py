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
