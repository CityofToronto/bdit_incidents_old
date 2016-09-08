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


engine = create_engine('postgresql://'\
'dolejar:dan@137.15.155.38:5432/bigdata_ah')

segments=['A','B','B1','C','D','E','F','G','H','I','J','K']
dvpSegmentsN = ['F','G','H','I','J','K']
dvpSegmentsS = list(reversed(dvpSegmentsN))
fggSegmentsE = ['A','B','B1','C','D','E','F']
fggSegmentsW = list(reversed(fggSegmentsE))

def readSegments(inSegments, month, day, n, engine):
    '''
    Returns list of dataframes 
    Each element is travel time on one segment
    '''
    dfList = []
    startDate = datetime.date(2015,month,day)
    endDate = startDate + timedelta(days=n)
    
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
    
def readVolumes(startDate, engine):
    
    #startDate = datetime.date(2014,month,day)
    strSQL = 'SELECT * '\
    'FROM cot.volumes '\
    'WHERE (cot.volumes.count_date = %(dstart)s ' \
    'AND cot.volumes.location LIKE %(road)s)'     
    df = pandasql.read_sql(sql=strSQL,
                           params={'dstart':startDate,
                                   'road':'%GARDINER%'},
                           con=engine)
    return df    

'''    
i = 0
startDate = datetime.date(2015,1,1)
emptyList = []

while i < 365:
    print(i)
    df = readVolumes(startDate,engine)
    if df.empty == True:
        emptyList.append(startDate)
    startDate += timedelta(days=1)
    i += 1
'''