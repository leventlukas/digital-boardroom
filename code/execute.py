import requests
import json
from datetime import datetime, timedelta
import time
import sys
import os
import logging

def call():
    response = requests.post(url = 'http://digital-boardroom-service:8404/simulation/produktionsdurchlauf')
    return response.text

def lagereingang():
    response = requests.post(url = 'http://digital-boardroom-service8404/simulation/lagereingang')
    return json.loads(response.text)

def ping():
    response = requests.post(url = 'http://digital-boardroom-service:8404/ping')
    return response.text

def bestellung():
    response = requests.post('http://digital-boardroom-service:8404/simulation/bestellung')
    return response.text
    
def test():
    response = requests.post('http://digital-boardroom-service:8404/test/auslastung')
    return response.text

def get_maschinenreihenfolge():
    response = requests.post('http://digital-boardroom-service:8404/simulation/test')
    return response.text

def infiniloop(sek):
    while True:
        logging.info(call())
        time.sleep(sek)

def loop(sek, loops):
    for i in range(loops):
        logging.info(i, call())
        time.sleep(sek)
 
if __name__ == '__main__':

    logging.basicConfig(level='INFO')

    if len(sys.argv) >= 3:
        loop(int(sys.argv[1]), int(sys.argv[2]))

    else: 
        infiniloop(int(sys.argv[1]))
