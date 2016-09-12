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


print('Creating engine...')
engine = create_engine('postgresql://'\
'dolejar:dan@137.15.155.38:5432/bigdata_ah')

segments=['A','B','B1','C','D','E','F','G','H','I','J','K']
dvpSegmentsN = ['F','G','H','I','J','K']
dvpSegmentsS = list(reversed(dvpSegmentsN))
fggSegmentsE = ['A','B','B1','C','D','E','F']
fggSegmentsE2 = ['A','B','C','D','E','F']
fggSegmentsW = list(reversed(fggSegmentsE))
    
def readSegments(inSegments, month, day, engine):
    '''
    Returns list of dataframes 
    Each element is travel time on one segment
    '''
    dfList = []
    startDate = datetime.date(2015,month,day)
    endDate = startDate + timedelta(days=1)
    
    for i in range(len(inSegments)-1):
        print('Query going in...')
        strSQL = 'SELECT bluetooth.raw_data."Timestamp",'\
        'bluetooth.raw_data."AvgMeasuredTime",'\
        'bluetooth.raw_data."StartPointName",'\
        'bluetooth.raw_data."EndPointName" '\
        'FROM bluetooth.raw_data INNER JOIN bluetooth.ref_segments '\
        'ON (bluetooth.raw_data."StartPointName" '\
        '= bluetooth.ref_segments.orig_startpointname '\
        'AND bluetooth.raw_data."EndPointName" '\
        '= bluetooth.ref_segments.orig_endpointname) '\
        'WHERE (bluetooth.ref_segments.startpointname = %(pt1)s '\
        'AND bluetooth.ref_segments.endpointname = %(pt2)s '\
        'AND bluetooth.raw_data."Timestamp" >= %(dstart)s '\
        'AND bluetooth.raw_data."Timestamp" < %(dend)s)'
        dfList.append(pandasql.read_sql(sql=strSQL,
                                        params={'pt1':inSegments[i],
                                                'pt2':inSegments[i+1],
                                                'dstart':startDate,
                                                'dend':endDate},
                                        con=engine))
    return dfList

def selectDateInc(month,day,data):
    '''
    Returns list of incident data dataframes for inputed date on inputted segment in form [selected direction, other direction]
    '''
    data.StartDateTime = pd.to_datetime(data.StartDateTime)
    startDate = datetime.date(2015,month,day)
    endDate = startDate + timedelta(days=1)
    startDate = pd.to_datetime(startDate)
    endDate = pd.to_datetime(endDate)
    return (data[(data.StartDateTime >= startDate) 
                 & (data.StartDateTime < endDate)])

def plotDateSegments(month, day, inSegments, direction, colors, engine):
    '''
    Stacked area
    '''
    segmentTimes = readSegments(inSegments, month, day, engine)
    #TRAVEL TIME PLOT
    tempTimes = segmentTimes[0]
    plt.figure(figsize=(16,12),dpi=300)
    plt.ylim(0,60)
    plt.plot(tempTimes.Timestamp, 
             tempTimes.AvgMeasuredTime/60, 
             'k')
    plt.fill_between(tempTimes.Timestamp.as_matrix(),
                     tempTimes.AvgMeasuredTime.as_matrix()/60, 
                     color=colors[0])
    for i in range(1,len(segmentTimes)):
        tempTimesFill = tempTimes.copy() 
        tempTimes.AvgMeasuredTime += segmentTimes[i].AvgMeasuredTime
        plt.plot(tempTimes.Timestamp, 
                 tempTimes.AvgMeasuredTime/60,
                 'k')
        plt.fill_between(tempTimes.Timestamp.as_matrix(),
                         tempTimesFill.AvgMeasuredTime.as_matrix()/60,
                         tempTimes.AvgMeasuredTime.as_matrix()/60,
                         color=colors[i])
    return tempTimes.AvgMeasuredTime
    

def plotDateSegmentsInc(month, day, inSegments, incData1, incData2, direction,
                        colors, engine):
    '''
    Stacked area
    incData1 in the same dir as direction
    indData2 in the opposite dir as direction
    '''
    incDayData1 = selectDateInc(month,day,incData1)
    incDayData2 = selectDateInc(month,day,incData2)
    segmentTimes = readSegments(inSegments, month, day, engine)
    
    #TRAVEL TIME PLOT
    tempTimes = segmentTimes[0]
    plt.figure(figsize=(16,12),dpi=300)
    plt.ylim(0,60)
    plt.plot(tempTimes.Timestamp, 
             tempTimes.AvgMeasuredTime/60,'k')
    plt.fill_between(tempTimes.Timestamp.as_matrix(),
                     tempTimes.AvgMeasuredTime.as_matrix()/60, 
                     color=colors[0])
    for i in range(1,len(segmentTimes)):
        tempTimesFill = tempTimes.copy() 
        tempTimes.AvgMeasuredTime += segmentTimes[i].AvgMeasuredTime
        plt.plot(tempTimes.Timestamp, 
                 tempTimes.AvgMeasuredTime/60,'k')
        plt.fill_between(tempTimes.Timestamp.as_matrix(), 
                         tempTimesFill.AvgMeasuredTime.as_matrix()/60, 
                         tempTimes.AvgMeasuredTime.as_matrix()/60, 
                         color=colors[i])
 
    #INC PLOT
    if(direction == 'SB' or direction == 'EB'):
        inSegments = list(reversed(inSegments))
    if(direction == 'SB' or direction == 'NB'):
        start = 'bt-start'
        end = 'bt-end'
    if(direction == 'EB' or direction == 'WB'):
        start = 'bt-start_1'
        end = 'bt-end_1'
    for i in range(len(inSegments)-1): 
        incDayData1temp = incDayData1[(incDayData1[start] == inSegments[i+1]) 
                                      & (incDayData1[end] == inSegments[i])]
        incDayData2temp = incDayData2[(incDayData2[start] == inSegments[i+1]) 
                                      & (incDayData2[end] == inSegments[i])]
        for inc in incDayData1temp.StartDateTime:
            plt.axvline(x=inc, 
                        color=colors[i], 
                        linewidth=1.5)
        for inc in incDayData2temp.StartDateTime:
            plt.axvline(x=inc,
                        color=colors[i], 
                        linestyle='dashed', 
                        linewidth=0.2)
    plt.xlim(pd.to_datetime(datetime.date(2015,month,day)),
             pd.to_datetime(datetime.date(2015,month,day)+timedelta(days=1)))
    return tempTimes.AvgMeasuredTime 
    

def combineSegments(dfList):
    df = dfList[0]
    for segment in dfList[1:]:
        df.AvgMeasuredTime += segment.AvgMeasuredTime
    return df

def costReturn(rate, vol, t, slowIn, fastIn):
    integral = np.trapz(y=slowIn.AvgMeasuredTime.as_matrix(),x=t.as_matrix()) 
    - np.trapz(y=fastIn.AvgMeasuredTime.as_matrix(),x=t.as_matrix())
    delay = int(integral)/3600000000000
    cost = int(delay*rate*vol)
    return cost

def normalCombined(travelDataList):
    '''
    input = list of normal days, combined travel time 
    output = series of mean of normal days
    
    pseudocode:
    outframe = first inframe
    for rest of the frames in list
        concat to make 1 big frame,
    return mean along axis 1
    '''
   # GET THIS TO WORK
    df = travelDataList[0]
    for day in travelDataList[1:]:
        df = pd.concat([df.reset_index(drop=True),day.reset_index(drop=True)],
                        ignore_index=True,
                        axis=1) 
    return df.mean(axis=1)
  
    
c5 = ['b','g','c','m','y']    
grey5 = ['#e6e6e6','#b3b3b3','#808080','#4d4d4d','#1a1a1a']
grey6 = ['#e6e6e6','#b3b3b3','#808080','#4d4d4d','#1a1a1a','#ffffff']

dvpIncNB = pd.read_csv('dvp-north.csv')
dvpIncSB = pd.read_csv('dvp-south.csv')
fggIncEB = pd.read_csv('fgg-east.csv')
fggIncWB = pd.read_csv('fgg-west.csv')

timeSeries = pd.read_csv('temp.csv')

nNormalDays = [5,6,11,22,25]
sNormalDays = [4,8,11,14,22]

dvpNBaseline = pd.read_csv('dvpN-baseline.csv')
dvpSBaseline = pd.read_csv('dvpS-baseline.csv')
fggEBaseline = pd.read_csv('fggE-baseline.csv')
fggWBaseline = pd.read_csv('fggW-baseline.csv')



