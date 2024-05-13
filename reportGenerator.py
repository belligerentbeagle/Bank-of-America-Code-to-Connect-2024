import pandas as pd
import numpy as np


def generate_exchange_report(ordersRejected):
    column_names = ['OrderID','RejectionReason'] #header
    dataframe = pd.DataFrame(ordersRejected, columns=column_names) #creating dataframe using array
    dataframe.to_csv("output_exchange_report.csv",index=False) #dataframe to csv

def client_report(client_report): #client report is in format {client_id: {instrument_id: net_position}}
    column_names = ['ClientID','InstrumentID','NetPosition'] #header
    data = []
    for client_id, instruments in client_report.items():
        for instrument_id, net_position in instruments.items():
            data.append([client_id, instrument_id, net_position])
    
    dataframe = pd.DataFrame(data, columns=column_names) #creating dataframe using array
    dataframe.to_csv("output_client_report.csv",index=False) #dataframe to csv

def instrumental_report(instrument_report):
    column_names = ['InstrumentID','OpenPrice','ClosePrice','TotalVolume','VWAP','DayHigh','DayLow'] #header
    dataframe = pd.DataFrame(instrument_report, columns=column_names) #creating dataframe using array
    dataframe.to_csv("output_instrument_report.csv",index=False) #dataframe to csv
