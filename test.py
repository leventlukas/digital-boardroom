import requests
import json
from datetime import datetime, timedelta
import time

def call():
    response = requests.post(url = 'http://0.0.0.0:8404/simulation/produktionsdurchlauf')
    return json.loads(response.text)

def ping():
    response = requests.post(url = 'http://0.0.0.0:8404/ping')
    return response.text

def bestellung():
    response = requests.post('http://0.0.0.0:8404/simulation/bestellung')
    return response


if __name__ == '__main__':
    # print(ping())

    # print(bestellung())

    # time_1 = datetime.now()

    # time.sleep(3)

    # time_2 = datetime.now()
    
    # difference = time_2 - time_1
    # print(difference.total_seconds())

    print(call())
