import GetData 
from GetData import load_token
import datetime
import requests
import pandas as pd
import csv 
import numpy as np
import matplotlib.pyplot as plt



class access_dfs:
    def __init__(self):
        self.dfs = {}


def date_processing(date:datetime.datetime):
    date = fix_date(date)
    end_date = date + datetime.timedelta(days=5) 
    start_date = date - datetime.timedelta(days=5)

    return start_date,end_date


def make_request(date, type, location):
    USERNAME,PASSWORD,TOKEN = load_token()
    date_from,date_to = date_processing(date)
    URL = GetData.make_url(USERNAME, PASSWORD, TOKEN, date_from, date_to,type,location)
    response = requests.get(URL).text
    return response

def get_past_data(date, type,location):
    info_df = pd.DataFrame()
    date = fix_date(date)
    for i in range(5,0,-1):
        date_for_request = date - datetime.timedelta(days=i*365)
        data = make_request(date_for_request,type,location)
        write_test_data(data)
        data_df = pd.read_csv('data.txt',delimiter=';')
        info_df = pd.concat([info_df,data_df])
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

def classify_rain_data(data):
    band = np.ceil(data['class'].mean())
    return band

def process_rain(date,location):
    data,avg,std,maximum,percentage_rainfall = get_rain_data(date,location)
    band = classify_rain_data(data)
    classification = classify_band(band,'Rain')
    return data,avg,band, std,maximum,percentage_rainfall, classification



def get_wind_data(date,location):
    data = get_past_data(date,'Wind',location)
    bins = np.array([0,1,5,11,19,28,38,49,61,74,88,102,117,1000000])
    data,avg, std, maximum, percentage_wind = produce_averages(data,'Wind', bins)
    return data,avg,std,maximum,percentage_wind

def classify_wind_data(data):
    band = np.ceil(data['class'].mean())
    return band

def process_wind(date,location):
    data,avg,std,maximum,percentage_wind = get_wind_data(date,location)
    band = classify_wind_data(data)
    classification = classify_band(band,'Wind')
    return data,avg,band,std, maximum, classification


def get_humidity_data(date,location):
    data = get_past_data(date,'Humidity',location)
    bins = np.array([0,10,20,30,40,50,60,70,80,90,100])
    data,avg, std, maximum, percentage_humidity = produce_averages(data,'Humidity', bins)
    return data,avg,std,maximum,percentage_humidity

def classify_humidity_data(data):
    band = np.ceil(data['class'].mean())
    return band

def process_humidity(date,location):
    data,avg,std,maximum,percentage_humidity = get_humidity_data(date,location)
    band = classify_humidity_data(data)
    classification = classify_band(band,'Humidity')
    return data,avg,band,std, maximum, classification

def get_temp_data(date,location):
    data = get_past_data(date,'Temperature',location)
    bins = np.array([-100,-5,5,25,32,35,10000])
    data,avg, std, maximum, percentage_temp = produce_averages(data,'Temperature', bins)
    return data,avg,std,maximum,percentage_temp

def classify_temp_data(data):
    band = np.ceil(data['class'].mean())
    return band

def process_temp(date,location):
    data,avg,std,maximum,percentage_temperature = get_temp_data(date,location)
    band = classify_temp_data(data)
    classification = classify_band(band,'Temperature')
    return data,avg,band, std,maximum, classification

def fix_date(date: datetime.datetime):
    while date > datetime.datetime.now():
        date = date - datetime.timedelta(days=365)
    return date

def classify_band(band, type):
    rain_bands = {1: "Light Rain",
        2: "Moderate Rain", 3: "Heavy Rain"}
    wind_bands = {1: "Calm", 2: "Light Air", 3: "Light Breeze", 4: "Gentle Breeze", 5: "Moderate Breeze", 6: "Fresh Breeze", 7: "Strong Breeze", 8: "Near Gale", 9: "Gale", 10: "Strong Gale", 11: "Storm", 12: "Violent Storm", 13: "Hurricane"}
    humidity_bands = {1:'Dry Moderate',2:'Dry Polar',3:'Dry Tropical',4:'Moist Moderate',5:'Moist Polar',6:'Moist Tropical',7:'Humid Moderate',8:'Humid Polar',9:'Humid Tropical',10:'Saturated'}
    temp_bands = {1:'Extremely Cold', 2:'Cold', 3:'Warm', 4:'Hot', 5:'Very Hot'}

    if type == 'Rain':
        return rain_bands.get(band, "Unknown Band")
    elif type == 'Wind':
        return wind_bands.get(band, "Unknown Band")
    elif type == 'Humidity':
        return humidity_bands.get(band, "Unknown Band")
    elif type == 'Temperature':
        return temp_bands.get(band, "Unknown Band")

def save_graph(data):
    pass

def get_day_in_set(data,date):
    
    data['Date'] = data['Date'].apply(lambda x: x.replace("T", " "))
    data['Date'] = data['Date'].apply(lambda x: x.replace("Z",""))
    format_date = "%Y-%m-%d %H:%M:%S"
    data['Date'] = data['Date'].apply(lambda x: datetime.datetime.strptime(x,format_date))
    start_date = date - datetime.timedelta(days=5)
    data['Day'] = data['Date'].apply(lambda x: (x - start_date).days)
    return data


def get_full_data_for_date(date,location):
    date = fix_date(date)
    rain_data,rain_avg,rain_band,rain_std,rain_max,percentage_rainfall,rain_classification = process_rain(date,location)
    wind_data,wind_avg,wind_band,wind_std,maximum_wind, wind_classification = process_wind(date,location)
    humidity_data,humidity_avg,humidity_band,humidity_std,maximum_humidity, humidity_classification = process_humidity(date,location)
    temp_data,temp_avg,temp_band,temp_std,maximum_temp, temp_classification = process_temp(date,location)

    data_list = [rain_data,wind_data,humidity_data,temp_data]
    for i in data_list: 
        get_day_in_set(i,date)

    return {
        "Rain": {
            "Average Rainfall": rain_avg,
            "Standard Deviation": rain_std,
            "Maximum Rainfall": rain_max,
            "Percentage Chance": percentage_rainfall,
            "Classification": rain_classification
        },
        "Wind": {
            "Average Wind Speed": wind_avg,
            "Standard Deviation": wind_std,
            "Maximum Wind Speed": maximum_wind,
            "Classification": wind_classification
        },
        "Humidity": {
            "Average Humidity": humidity_avg,
            "Standard Deviation": humidity_std,
            "Maximum Humidity": maximum_humidity,
            "Classification": humidity_classification
        },
        "Temperature": {
            "Average Temperature": temp_avg,
            "Standard Deviation": temp_std,
            "Maximum Temperature": maximum_temp,
            "Classification": temp_classification
        }
    }
    
if __name__ == '__main__':
    global USERNAME 
    global PASSWORD
    global TOKEN
    USERNAME = "lockie_sam"
    PASSWORD = "1fy6pJqE401w2OoAK1WR"
    TOKEN = GetData.get_token(username=USERNAME, password=PASSWORD)


    print(get_full_data_for_date(datetime.datetime(2029,12,3),'Canberra'))

