import requests
from base64 import b64encode


def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'

def get_Token(username, password):
    headers = { 'Authorization' :basic_auth(username,password) }
 
    response = requests.get('https://login.meteomatics.com/api/v1/token/',headers=headers)

    token = response.json()
    
    print(token)




if __name__ == '__main__':
    TOKEN = 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2IjoxLCJ1c2VyIjoiZ3VybmV5X25pY2hvbGFzIiwiaXNzIjoibG9naW4ubWV0ZW9tYXRpY3MuY29tIiwiZXhwIjoxNzU5NTczNDUwLCJzdWIiOiJhY2Nlc3MifQ.moa33aZJnX0MFI7uIebrGntK5VIgfHKVlD3PmIBPyAyocVxSN0RPXhw_GaVywX1esboVrCv_MmmCTUDJ9ORusw'

    USERNAME = 'gurney_nicholas' 
    PASSWORD = 'y51m14ABCgT7m4F6l235'
    get_Token(USERNAME, PASSWORD)

    #URL = f'https://api.meteomatics.com/2020-10-04T00Z--2025-10-04T00Z/precip_24h:mm/51.11,10.2/html?access_token={TOKEN}'

    #response = requests.get(URL)
    #print(response.content[:5000])
