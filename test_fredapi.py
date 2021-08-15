# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 21:09:56 2021

@author: Administrator
"""


from fredapi import Fred
import pandas as pd
import matplotlib.pyplot as plt
from functools import reduce
import quandl


def convert_timestamp(s,arg):
    s['year'] = s[arg].date().year
    s['month'] = s[arg].date().month
    return s

def get_time_series(code,dataType,dfList = [],whichApi = 'Fred'):
    if(whichApi is 'Fred'):
        s = fred.get_series(code)
    elif(whichApi is 'Quandl'):
        s = quandl.get(code)
        
    df = pd.DataFrame(s)
    #create new column with the fred series's index
    df['timestamp'] = df.index
    
    
    #reset the index
    df = df.reset_index(inplace=False,drop = True)
    #fred sends back one column we want to rename
    df = df.rename(columns = {0:dataType})
    #we extract month and year from the previously created timestamp
    df = df.apply(convert_timestamp,arg = 'timestamp', axis=1)
    #drop the timestamp
    # df = df.drop('timestamp', axis=1)
    dfList.append(df)
    return df,dfList

fred = Fred(api_key = '##')


# s = fred.get_series('SP500', observation_start='2014-09-02', observation_end='2021-08-11')
# s.tail()

dfUI,dfs = get_time_series('EECTOT','import')
dfIQ,dfs = get_time_series('IQ','export',dfs)
dfNSP,dfs = get_time_series('ASPNHSUS',' avg price new sold houses ',dfs)
dfEHS,dfs = get_time_series('EXHOSLUSM495S',' existing home sales ',dfs)
dfEHS,dfs = get_time_series('RSXFS',' retail trade sales ',dfs)
dfER,dfs = get_time_series('LREM25TTUSM156S',' employment rate',dfs)
dfER,dfs = get_time_series('PERMIT',' Housing Units Authorized',dfs)
dfPMI,dfs = get_time_series("ISM/MAN_PMI", "PMI",dfs, 'Quandl')

df_final = reduce(lambda left,right: pd.merge(left,right,on=['year', 'month','timestamp']), dfs)
#remove duplicated columns
df_final = df_final.drop(df_final.filter(regex='_y$').columns.tolist(),axis=1, inplace=True)
#remove _x suffices from columns
df_final = df_final.rename(columns=lambda x: re.sub('_x$','',x))

# specify from which year you want to plot data 
to_plot = df_final[df_final['year'].apply(lambda key: key > 2015)]
#plot wanted data
plt.plot(to_plot['timestamp'],to_plot['PMI'],color="red")
plt.xlabel("year")
plt.ylabel("import index")


