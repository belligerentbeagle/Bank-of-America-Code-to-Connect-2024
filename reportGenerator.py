#exchange report
import pandas as pd
import numpy as np

array=[1,2,3,4]

def array_to_csv_with_headers(array,column_names,filename):

    column_names= ['OrderID','RejectionReason'] #header
    dataframe = pd.DataFrame(array, column_names) #creating dataframe using array
    dataframe.to_csv("Exchange_report.csv", index=False) #dataframe to csv

    #client report
    column_names= ['ClientID','InstrumentalID','NetPosition'] #header
    dataframe = pd.DataFrame(array, column_names) #creating dataframe using array
    dataframe.to_csv("Client_report.csv",index=False) #dataframe to csv

    #instrumental report
    column_names= ['InstrumentalID','OpenPrice','ClosePrice','TotalVolume','VWAP','DayHigh','DayLow'] #header
    dataframe = pd.DataFrame(array, column_names) #creating dataframe using array
    dataframe.to_csv("Instrumental_report.csv",index=False) #dataframe to csv


array_to_csv_with_headers(array,'Exchange_report.csv')

