import time
import json
import random
import cherrypy
import requests
from MyMQTT import MyMQTT
from environment_control import ec_sub

base_url = 'https://api.thingspeak.com/update?api_key=VUV0KZ2FWCBO69QY&'
t = 5 #second

class TS_ec_sub(ec_sub):
    def notify(self, topic, msg):
        d = json.loads(msg)
        # print(d)

        pre_temp = d['data'][0]['t']
        pre_temp = eval(pre_temp)
        pre_humd = d['data'][1]['h']
        pre_humd = eval(pre_humd)

        pre_temp_req = requests.get(base_url+f'field3={pre_temp}')
        time.sleep(t)
        pre_humd_req = requests.get(base_url+f'field4={pre_humd}')
        time.sleep(t)

        with open('TSdata_log.json', 'w') as file:
            json.dump(d, file)

        print('get data')

class post_sub:
    def __init__(self, clientID, topic, broker, port):
        self.client = MyMQTT(clientID, broker, port, self)
        self.topic = topic
        self.status = None

    def start(self):
        self.client.start()
        self.client.mySubscribe(self.topic)

    def stop(self):
        self.client.stop()

    def notify(self, topic, msg):
        d = json.loads(msg)
        # print(d)

        temp = d['data'][0]['t']
        temp = eval(temp)
        humd = d['data'][1]['h']
        humd = eval(humd)

        temp_req = requests.get(base_url+f'field1={temp}')
        time.sleep(t)
        humd_req = requests.get(base_url+f'field2={humd}')
        time.sleep(t)

        with open('TSpost_log.json', 'w') as file:
            json.dump(d, file)


        print('get post data')


if __name__ == '__main__':

    conf = json.load(open("post_ec_setting.json"))
    broker = conf["broker"]
    port = conf["port"]
    topic = conf['baseTopic']
    TSec_sub = TS_ec_sub("TS_ec_sub", topic, broker, port)
    TSec_sub.start()


    conf_sub = json.load(open("post_setting.json"))
    broker_sub = conf_sub["broker"]
    port_sub = conf_sub["port"]
    topic_sub = conf_sub['baseTopic']
    TSpost_sub = post_sub("post_sub", topic_sub, broker_sub, port_sub)
    TSpost_sub.start()

    t = 2
        
    while True:      
        time.sleep(t)

