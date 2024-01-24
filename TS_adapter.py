import time
import json
import random
import cherrypy
import requests


base_url = 'https://api.thingspeak.com/update?api_key=VUV0KZ2FWCBO69QY&'
t = 30 #second

while True:
    with open('sensor_log.json') as file:
        data = json.load(file)

    temp = data['data'][0]['t'][-1]
    temp = eval(temp)
    humd = data['data'][1]['h'][-1]
    humd = eval(humd)

    with open('predicted_log.json') as file:
        data = json.load(file)
    pre_temp = data['data'][0]['t'][-1]
    pre_temp = eval(pre_temp)
    pre_humd = data['data'][1]['h'][-1]
    pre_humd = eval(pre_humd)


    temp_req = requests.get(base_url+f'field1={temp}')
    time.sleep(t)
    humd_req = requests.get(base_url+f'field2={humd}')
    time.sleep(t)
    pre_temp_req = requests.get(base_url+f'field3={pre_temp}')
    time.sleep(t)
    pre_humd_req = requests.get(base_url+f'field4={pre_humd}')
    time.sleep(t)
    print('done')

    # time.sleep(t)
