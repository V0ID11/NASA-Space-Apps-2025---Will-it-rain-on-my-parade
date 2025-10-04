import GetData 
import datetime
import requests
import pandas as pd
import csv 
import numpy as np

def date_processing(date:datetime.datetime):
    end_date = date + datetime.timedelta(days=10) 
    start_date = date - datetime.timedelta(days=10)

    return start_date,end_date


def make_request(date, type, location):
    date_from, date_to = date_processing(date)
    URL = GetData.make_url(USERNAME, PASSWORD, TOKEN, date_from, date_to,type,location)
    response = requests.get(URL).text
    return response

def get_past_data(date, type,location):
    info_df = pd.DataFrame()
    for i in range(5,0,-1):
        date_for_request = date - datetime.timedelta(days=i*365)
        data = make_request(date_for_request,type,location)
        write_test_data(data)
        data_df = pd.read_csv('data.txt ',delimiter=';')
        info_df = pd.concat([info_df,data_df])
    print(info_df.head())
    info_df.columns = ["Lat","Lon","Date",type]
    return info_df

def produce_averages(data:pd.DataFrame,type,bins):
    mean = data[type].mean()
    std = data[type].std()
    maximum = data[type].max()
    percentage_rainfall = data[type].map(lambda x: 1 if x > 0 else 0)
    percentage_rainfall = sum(percentage_rainfall) * 100 / len(percentage_rainfall)
    data['class'] = pd.cut(data[type],bins,labels=[i+1 for i in range(len(bins)-1)],right=True,include_lowest=True)
    data['class']=data['class'].cat.codes
    return data, mean,std,maximum,percentage_rainfall


def write_test_data(data: str, filename: str="data.txt") -> None:
        with open(filename, "w") as f:
            f.write(data)

def get_rain_data(date,location):
    data = get_past_data(date,'Precipitation',location)
    bins = np.array([0,0.500004,3.99996,100000])
    data,avg, std, maximum, percentage_rainfall = produce_averages(data,'Precipitation', bins)
    return data,avg,std,maximum,percentage_rainfall

def classify_rain_data(data,avg, std, maximum, percentage_rainfall):
    band = np.ceil(data['class'].mean())
    return band

def process_rain(date,location):
    data,avg,std,maximum,percentage_rainfall = get_rain_data(date,location)
    band = classify_rain_data(data,avg,std,maximum,percentage_rainfall)
    return avg,band, percentage_rainfall

if __name__ == '__main__':
    global USERNAME 
    global PASSWORD
    global TOKEN
    USERNAME = "lockie_sam"
    PASSWORD = "1fy6pJqE401w2OoAK1WR"
    TOKEN = GetData.get_token(username=USERNAME, password=PASSWORD)

    print(GetData.get_lon_lat('London'))
    print(GetData.get_lon_lat('Miami'))

    print(process_rain(datetime.datetime(2025,12,3),'Canberra'))

