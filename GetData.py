import requests
from base64 import b64encode
import csv
import datetime
from geopy.geocoders import Nominatim


def get_token(username, password) -> str:
    # Build Basic Auth header manually (requests can also do this for you)
    credentials = f"{username}:{password}"
    encoded = b64encode(credentials.encode("utf-8")).decode("ascii")
    headers = {
        "Authorization": f"Basic {encoded}",
        "Accept": "application/json",
    }

    url = 'https://login.meteomatics.com/api/v1/token'
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()  # raise HTTPError for 4xx/5xx
    data = resp.json()
    token = data.get("access_token")
    if not token:
        raise ValueError(f"No access_token in response: {data}")
    return token

def convert_to_dataset(datatype):
    dataDict = {'Precipitation':'precip_1h:mm', 'Wind':'wind_speed_2m:kmh', 'Temperature':'t_apparent_mean_1h:C', 'Humidity':'absolute_humidity_2m:gm3'}
    return dataDict[datatype]



def date_formatting(date_from,date_to):
    time_frame = str(date_from)+"Z" + "--" + str(date_to)+"Z"
    time_frame = time_frame.replace(" ","T")
    return time_frame

def make_url(username,password,token,date_from,date_to,datatype, location):
    location=get_lon_lat(location)
    location = create_lon_lat_rectangle(location[0],location[1])
    url = f"https://{username}:{password}@api.meteomatics.com/{date_formatting(date_from,date_to)}/{convert_to_dataset(datatype)}/{location[0]},{location[1]}_{location[2]},{location[3]}:5x5/csv?access_token={token}"
    return url

def get_lon_lat(location):
    geolocator = Nominatim(user_agent="Climate-Coders")
    location = geolocator.geocode(location)
    return location.longitude,location.latitude

def create_lon_lat_rectangle(longitude, latitude):
    min_long = longitude - 0.1
    max_long = longitude + 0.1
    min_lat =  latitude - 0.1
    max_lat = latitude + 0.1
    return max_lat,min_long,  min_lat,max_long


def load_token():
    
    USERNAME = "USERNAME GOES HERE"
    PASSWORD = "PASSWORD GOES HERE"
    TOKEN = get_token(username=USERNAME, password=PASSWORD)
    return USERNAME, PASSWORD,TOKEN

if __name__ == '__main__':
    def write_test_data(data: str, filename: str="test_data.txt") -> None:
        with open(filename, "w") as f:
            f.write(data)
    
    def read_test_data(filename: str = "test_data.txt") -> list[str]:
        with open(filename, "r") as f:
            lines = [line.strip() for line in f]
        
        return lines
    
    TOKEN = get_token(username=USERNAME, password=PASSWORD)
    
    #URL = f"https://{USERNAME}:{PASSWORD}@api.meteomatics.com/2020-10-04T00Z--2025-10-04T00Z/precip_24h:mm/51.11,10.2/csv?access_token={TOKEN}"

    # If there is not a new URL, for testing purposes this should be False to speed things up
    NEW_URL = True
    URL = make_url(USERNAME,PASSWORD,TOKEN,datetime.datetime(2020,10,10),datetime.datetime(2024,3,7),"Precipitation","Paris")
    print(URL)
    if NEW_URL:
        result = requests.get(URL).text
        print(result)
        #write_test_data(result)
    
    #data = read_test_data()
    #print(data)

    
    

