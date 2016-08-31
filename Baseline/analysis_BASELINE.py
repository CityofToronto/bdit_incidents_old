from __future__ import division
import datetime
from datetime import timedelta
import numpy as np
import pandas as pd
import pandas.io.sql as pandasql
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('seaborn-whitegrid')


engine = create_engine('postgresql://dolejar:dan@137.15.155.38:5432/bigdata_ah')

segments=['A','B','B1','C','D','E','F','G','H','I','J','K']
dvpSegmentsN = ['F','G','H','I','J','K']
dvpSegmentsS = list(reversed(dvpSegmentsN))
fggSegmentsE = ['A','B','B1','C','D','E','F']
fggSegmentsW = list(reversed(fggSegmentsE))

def readSegments(inSegments, month, day, n, engine):
    '''
    Returns list of dataframes containing bliptrack travel times for n days on inputted segments
    '''
    dfList = []
    startDate = datetime.date(2015,month,day)
    endDate = startDate + timedelta(days=n)
    strStartDate = startDate.strftime('%Y-%m-%d')
    strEndDate = endDate.strftime('%Y-%m-%d')
    for i in range(len(inSegments)-1):
        print('Query going in...')
        strSQL = 'SELECT bluetooth.raw_data."Timestamp",bluetooth.raw_data."AvgMeasuredTime",bluetooth.raw_data."StartPointName",bluetooth.raw_data."EndPointName" FROM bluetooth.raw_data INNER JOIN bluetooth.ref_segments ON (bluetooth.raw_data."StartPointName" = bluetooth.ref_segments.orig_startpointname AND bluetooth.raw_data."EndPointName" = bluetooth.ref_segments.orig_endpointname) WHERE (bluetooth.ref_segments.startpointname = \''+inSegments[i]+'\' AND bluetooth.ref_segments.endpointname = \''+inSegments[i+1]+'\' AND bluetooth.raw_data."Timestamp" >= \''+strStartDate+'\' AND bluetooth.raw_data."Timestamp" < \''+strEndDate+'\')'
        dfList.append(pandasql.read_sql(strSQL,engine))
    return dfList

def baseline(dfList,p):
    '''
    takes list of dataframes, pivots to inputed percentile 
    '''    
    
    ptList = []
    for seg in dfList:
        seg = seg[(seg.Timestamp.dt.dayofweek != 6) 
                  & (seg.Timestamp.dt.dayofweek != 5) 
                  & (seg.Timestamp.dt.dayofweek != 4) 
                  & (seg.Timestamp.dt.dayofweek != 0)]
        seg['Time'] = seg.Timestamp.apply(lambda x: x.time())
        ptList.append(pd.pivot_table(seg,
                                     index='Time',
                                     aggfunc=lambda x: np.percentile(x, p)))
                                     
    df = ptList[0]
    for seg in ptList[1:]:
        df.AvgMeasuredTime += seg.AvgMeasuredTime
    return ptList[0]


def baselineDrop(dfList):
    '''
    evaluates median of each timestamp, 
    drop all timestamps less than 1.25x that of median, reevaluate median
    returns series of baseline travel time 
    '''
    ptList = []
    for seg in dfList:
        seg = seg[(seg.Timestamp.dt.dayofweek != 6) 
                  & (seg.Timestamp.dt.dayofweek != 5) 
                  & (seg.Timestamp.dt.dayofweek != 4) 
                  & (seg.Timestamp.dt.dayofweek != 0)]
        seg['Time'] = seg.Timestamp.apply(lambda x: x.time())
        ptList.append(pd.pivot_table(seg,
                                     index='Time',
                                     aggfunc=lambda x: np.percentile(x, 50)))
    for i in range(len(dfList)):
        
        dfList[i]['Time'] = dfList[i].Timestamp.apply(lambda x: x.time())
        for t in list(ptList[i].index): #iterate through each minute of a 24h clock                     
            dfList[i] = dfList[i][(dfList[i].Time != t) 
                                   | ((dfList[i].Time == t) 
                                  & (dfList[i].AvgMeasuredTime 
                                     < 1.25*ptList[i].get_value(t,'AvgMeasuredTime')))]
    ptList = []
    for seg in dfList:
        seg = seg[(seg.Timestamp.dt.dayofweek != 6) 
                  & (seg.Timestamp.dt.dayofweek != 5) 
                  & (seg.Timestamp.dt.dayofweek != 4) 
                  & (seg.Timestamp.dt.dayofweek != 0)]
        seg['Time'] = seg.Timestamp.apply(lambda x: x.time())
        ptList.append(pd.pivot_table(seg,
                                     index='Time',
                                     aggfunc=lambda x: np.percentile(x, 50)))
    df = ptList[0]
    for seg in ptList[1:]:
        df.AvgMeasuredTime += seg.AvgMeasuredTime
    return ptList[0]
    
def baselinePlot(inSegments, month, day, baseline, engine):
    '''
    plots inputted day and baseline with fill
    returns difference in area as a timedelta
    '''
    segmentTimes = readSegments(inSegments, month, day,1, engine)
    df = segmentTimes[0]
    df.Timestamp = pd.to_datetime(df.Timestamp)
    for seg in segmentTimes[1:]:
        df.AvgMeasuredTime += seg.AvgMeasuredTime
        
    plt.figure(figsize=(12,8),dpi=300)
    plt.plot(df.Timestamp, df.AvgMeasuredTime/60,'k')
    plt.plot(df.Timestamp, baseline.AvgMeasuredTime/60,'b')
    plt.fill_between(df.Timestamp.as_matrix(),
                     df.AvgMeasuredTime.as_matrix()/60,
                     baseline.AvgMeasuredTime.as_matrix()/60,
                     where
                     = (baseline.AvgMeasuredTime/60 > df.AvgMeasuredTime/60),
                     facecolor='green')    
    plt.fill_between(df.Timestamp.as_matrix(),
                     df.AvgMeasuredTime.as_matrix()/60,
                     baseline.AvgMeasuredTime.as_matrix()/60,
                     where
                     = (baseline.AvgMeasuredTime/60 < df.AvgMeasuredTime/60),
                     facecolor='red')    
    plt.show()
    integral = np.trapz(y=df.AvgMeasuredTime.as_matrix(), x=df.Timestamp.as_matrix()) - np.trapz(y=baseline.AvgMeasuredTime.as_matrix(),x=df.Timestamp.as_matrix())
    return integral
    

