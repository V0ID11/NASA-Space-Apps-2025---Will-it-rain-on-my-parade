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
        data_df = pd.read_csv('/home/data.txt',delimiter=';')
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


def write_test_data(data: str, filename: str="/home/data.txt") -> None:
        with open(filename, "w") as f:
            f.write(data)

def get_rain_data(date,location):
    data = get_past_data(date,'Precipitation',location)
    bins = np.array([-1,0.00001,0.500004,3.99996,100000])
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

def classify_band(band, type) -> tuple[str, str]: # Name of band, danger level
    rain_bands = {1: "Dry", 2: "Light Rain",
        2: "Moderate Rain", 3: "Heavy Rain"}
    wind_bands = {1: "Calm", 2: "Light Air", 3: "Light Breeze", 4: "Gentle Breeze", 5: "Moderate Breeze", 6: "Fresh Breeze", 7: "Strong Breeze", 8: "Near Gale", 9: "Gale", 10: "Strong Gale", 11: "Storm", 12: "Violent Storm", 13: "Hurricane"}
    humidity_bands = {1:'Dry Moderate',2:'Dry Polar',3:'Dry Tropical',4:'Moist Moderate',5:'Moist Polar',6:'Moist Tropical',7:'Humid Moderate',8:'Humid Polar',9:'Humid Tropical',10:'Saturated'}
    temp_bands = {1:'Very Cold', 2:'Cold', 3:'Mild', 4:'Warm', 5:'Hot', 6:'Very Hot'}
    danger_levels = ["Safe", "Dangerous", "Very Dangerous"]

    band_name = ""
    danger = danger_levels[0]

    if type == 'Rain':
        band_name = rain_bands.get(band, "Unknown Band")
        if band >= 3:
            danger = danger_levels[2]
        elif band >= 2:
            danger = danger_levels[1]

    elif type == 'Wind':
        band_name = wind_bands.get(band, "Unknown Band")
        if band >= 4:
            danger = danger_levels[2]
        elif band >= 3:
            danger = danger_levels[1]
    
    elif type == 'Humidity':
        band_name = humidity_bands.get(band, "Unknown Band")

    elif type == 'Temperature':
        band_name = temp_bands.get(band, "Unknown Band")
        
        # Cold
        if band <= 1:
            danger = danger_levels[2]
        elif band <= 2:
            danger = danger_levels[1]
        
        # Hot
        if band >= 6:
            danger = danger_levels[2]
        elif band >= 5:
            danger = danger_levels[1]

    
    return band_name, danger

def get_comfort_level(rain_class: str, wind_class: str, humid_class: str, temp_class: str) -> str:
    comfort_level = 0
    comforts = ["Normal", "Uncomfortable", "Very Uncomfortable"]
    if rain_class == "Dry":
        wet = False
    if wet:
        comfort_level += 1

    # Humidity
    if wet and temp_class == "Very Hot":
        return "Uncomfortable - skin may fry"
    elif humid_class == "Moist Tropical":
        comfort_level += 1
    elif humid_class == "Saturated":
        comfort_level += 1
    elif humid_class == "Humid Tropical":
        comfort_level += 2
    
    # Temperature
    if temp_class == "Hot" or temp_class == "Cold":
        comfort_level += 1
    elif temp_class == "Very Cold" or temp_class == "Very Hot":
        comfort_level += 2

    # Wind
    if wind_class == "Near Gale" or wind_class == "Gale" or wind_class == "Strong Gale":
        comfort_level += 1
    elif wind_class == "Storm" or wind_class == "Violent Storm" or wind_class == "Hurricane":
        comfort_level += 2

    if comfort_level > 2:
        comfort_level = 2

    return comforts[comfort_level]

def get_danger_level(rain_danger: str, wind_danger: str, temp_danger: str) -> str:
    dangers = [rain_danger, wind_danger, temp_danger]
    if "Very Dangerous" in dangers:
        return "Very Dangerous"
    num_dangers = 0
    for danger in dangers:
        if danger == "Dangerous":
            num_dangers += 1

    if num_dangers >= 2:
        return "Dangerous"
    else:
        return "Safe"



def save_graph(data,type):
    x_data = data['Days']
    y_data = data[type]
    # cs = CubicSpline(np.arange(0,10), y_data)
    # newx_dat = np.linspace(1,np.arange(0,10),1000)
    # newy_dat = cs(newx_dat)
    plt.scatter(x_data, y_data, label = type)
    plt.xlabel('Day')
    plt.ylabel(type)
    # type_av = st.mean(y_data)
    plt.axhline(y= type_av, color='r', linestyle='--', label= 'Average' +""+ type)
    plt.legend()
    plt.plot(x_data, y_data)
    plt.show()

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
    # for i in data_list: 
    #     save_graph(i,date, i.columns[2])

    return {
        "Rain": {
            "Average Rainfall": rain_avg,
            "Standard Deviation": rain_std,
            "Maximum Rainfall": rain_max,
            "Percentage Chance": percentage_rainfall,
            "Classification": rain_classification[0]
        },
        "Wind": {
            "Average Wind Speed": wind_avg,
            "Standard Deviation": wind_std,
            "Maximum Wind Speed": maximum_wind,
            "Classification": wind_classification[0]
        },
        "Humidity": {
            "Average Humidity": humidity_avg,
            "Standard Deviation": humidity_std,
            "Maximum Humidity": maximum_humidity,
            "Classification": humidity_classification[0]
        },
        "Temperature": {
            "Average Temperature": temp_avg,
            "Standard Deviation": temp_std,
            "Maximum Temperature": maximum_temp,
            "Classification": temp_classification[0]
        },
        "Feel": {
            "Danger Level": get_danger_level(rain_classification[1], wind_classification[1], temp_classification[1]),
            "Comfort Level": get_comfort_level(rain_classification[0], wind_classification[0], humidity_classification[0], temp_classification[0])
        }
    }
    
if __name__ == '__main__':
    global USERNAME 
    global PASSWORD
    global TOKEN

    TOKEN = GetData.get_token(username=USERNAME, password=PASSWORD)


    print(get_full_data_for_date(datetime.datetime(2029,12,3),'Canberra'))

