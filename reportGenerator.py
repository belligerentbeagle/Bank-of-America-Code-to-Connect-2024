import pandas as pd
import numpy as np


def generate_exchange_report(ordersRejected):
    column_names = ['OrderID','RejectionReason'] #header
    dataframe = pd.DataFrame(ordersRejected, columns=column_names) #creating dataframe using array
    dataframe.to_csv("output_exchange_report.csv",index=False) #dataframe to csv

def generate_client_report(client_report): #client report is in format {client_id: {instrument_id: net_position}}
    column_names = ['ClientID','InstrumentID','NetPosition'] #header
    data = []
    for client_id in client_report:
        for instruments in client_report[client_id]:
            data.append([client_id, instruments, client_report[client_id][instruments]])
    dataframe = pd.DataFrame(data, columns=column_names) #creating dataframe using array
    dataframe.to_csv("output_client_report.csv",index=False) #dataframe to csv
    return data

def instrumental_report(instrument_report):
    column_names = ['InstrumentID','OpenPrice','ClosePrice','TotalVolume','VWAP','DayHigh','DayLow'] #header
    dataframe = pd.DataFrame(instrument_report, columns=column_names) #creating dataframe using array
    dataframe.to_csv("output_instrument_report.csv",index=False) #dataframe to csv
