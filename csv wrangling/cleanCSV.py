from __future__ import division
import pandas as pd
import numpy as np

df = pd.read_csv('original_incident_file.csv', low_memory = False)
nRowsOriginal = len(df.index)

def clean(dfIn):
    """
    -> Drop all rows with no description
    -> Force event description to lowercase
    """
    df = dfIn.copy(deep = True) #new dataframe
    
    # (1)
    df['EventDescription'] = df['EventDescription'].replace(np.nan, 
                                                            '', 
                                                            regex = True)
    df['EventDescription'] = df['EventDescription'].str.lower()
    
    # desc type 1: no original, no update, bit of a shitshow
    df1 = df[(~df['EventDescription'].str.contains('original')) 
             & (~df['EventDescription'].str.contains('update'))]
    
    # desc type 2: original with an update
    df2 = df[(df['EventDescription'].str.contains('original')) 
             & (df['EventDescription'].str.contains('update'))]
    
    # desc type 3: only update, the update needs to be linked with the original
    df3 = df[(~df['EventDescription'].str.contains('original')) 
             & (df['EventDescription'].str.contains('update'))]
    
    return [df1,df2,df3]