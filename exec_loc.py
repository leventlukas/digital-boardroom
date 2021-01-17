import requests
import json
from datetime import datetime, timedelta
import time
import sys
import os

def call():
    response = requests.post(url = 'http://0.0.0.0:30001/simulation/produktionsdurchlauf')
    return response.text

def lagereingang():
    response = requests.post(url = 'http://0.0.0.0:30001/simulation/lagereingang')
    return json.loads(response.text)

def ping():
    response = requests.post(url = 'http://0.0.0.0:30001/ping')
    return response.text

def bestellung():
    response = requests.post('http://0.0.0.0:30001/simulation/bestellung')
    return 
    
def test():
    response = requests.post('http://0.0.0.0:30001/test/auslastung')
    return response.text

def get_maschinenreihenfolge():
    response = requests.post('http://0.0.0.0:30001/simulation/test')
    return response.text

def infiniloop(sek):
    while True:
        print(call())
        time.sleep(sek)

def loop(sek, loops):
    for i in range(loops):
        print(i, call())
        time.sleep(sek)

    
if __name__ == '__main__':
    # print(ping())

    # print(bestellung())

    # time_1 = datetime.utcnow()

    # time.sleep(3)

    # time_2 = datetime.utcnow()
    
    # difference = time_2 - time_1
    # print(difference.total_seconds())

    #lagereingang()
    #print(test())

    #print(get_maschinenreihenfolge())
    if len(sys.argv) >= 3:
        loop(int(sys.argv[1]), int(sys.argv[2]))

    else: 
        infiniloop(int(sys.argv[1]))

    

    #print(sys.argv[1], sys.argv[2])

    # while True:
    #     print(test())
    #     time.sleep(2)

    #nfiniloop()
