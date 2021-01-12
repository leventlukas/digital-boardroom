import requests
import json

def call():
    response = requests.post(url = 'http://0.0.0.0:8404/test')
    return json.loads(response.text)

def ping():
    response = requests.post(url = 'http://0.0.0.0:8404/ping')
    return response.text

if __name__ == '__main__':
    print(ping())
    print(call())