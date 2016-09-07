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
    
def readVolumes(month, day, engine):
    
    startDate = datetime.date(2015,month,day)
    strStartDate = startDate.strftime('%Y-%m-%d')
    #strSQL = 'SELECT * FROM cot.volumes WHERE(cot.volumes.count_date LIKE \'%GARDINER%\' AND cot.volumes.count_date >= \''+strStartDate+'\' AND cot.volumes.count_date < \''+strEndDate+'\')'
    #strSQL = 'SELECT * FROM cot.volumes WHERE (cot.volumes.count_date = \''+strStartDate+'\' AND cot.volumes.location LIKE \' \%GARDINER\% \')' 
    strSQL = 'SELECT * FROM cot.volumes WHERE (cot.volumes.count_date = %(dstart)s AND cot.volumes.location LIKE %(road)s)'     
    df = pandasql.read_sql(sql=strSQL,params={"dstart":startDate,"road":"%GARDINER%"},con=engine)
    return df    