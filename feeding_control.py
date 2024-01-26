

import json
import time
from MyMQTT import MyMQTT


class fer_com_pub:
    def __init__(self, clientID, topic,broker,port):
        self.topic=topic
        
        self.client=MyMQTT(clientID,broker,port,None)
        

    def start (self):
        self.client.start()

    def stop (self):
        self.client.stop()

    def publish(self):
      
        scripts = ['fertilizer turn on automaticly']
        
        command = 'fer_on'
        self.client.myPublish(self.topic,command)


        print(scripts)
        
        time.sleep(1)

if __name__ == "__main__":

    conf_pub=json.load(open("fer_command_setting.json"))
    broker_pub=conf_pub["broker"]
    port_pub=conf_pub["port"]
    topic_pub = conf_pub['baseTopic']
    com_pub = fer_com_pub("fer_com_pub",topic_pub,broker_pub,port_pub)
    com_pub.client.start()
    time.sleep(2)

    t_month = 30

    while True:

        com_pub.publish()
        time.sleep(t_month)
     

            
                 

