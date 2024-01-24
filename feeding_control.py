

import json
import time
from MyMQTT import MyMQTT

# class fer_sub:
#     def __init__(self, clientID, topic, broker, port):
#         self.client = MyMQTT(clientID, broker, port, self)
#         self.topic = topic
#         self.status = None

#     def start(self):
#         self.client.start()
#         self.client.mySubscribe(self.topic)

#     def stop(self):
#         self.client.stop()

#     def notify(self, topic, msg):
#         d = json.loads(msg)
#         self.temp = d['data'][0]['t']
#         self.humid = d['data'][1]['h']

#         with open('data_log.json') as file:
#             dic = json.load(file)

#         dic['data'][0]['t'].append(self.temp)
#         dic['data'][1]['h'].append(self.humid)

#         with open('data_log.json', 'w') as file:
#             json.dump(dic, file)
        
#         print("done")
#         # pub = True

class fer_com_pub:
    def __init__(self, clientID, topic,broker,port):
        self.topic=topic
        
        self.client=MyMQTT(clientID,broker,port,None)
        

    def start (self):
        self.client.start()

    def stop (self):
        self.client.stop()

    def publish(self):
        # with open('data_log.json') as file:
        #     dic = json.load(file)
        
        # try:
        #     t = float(eval(dic['data'][0]['t'][-1]))
        #     t_p = float(eval(dic['data'][0]['t'][-2]))
        #     h = float(eval(dic['data'][1]['h'][-1]))
        #     h_p = float(eval(dic['data'][1]['h'][-2]))
        # except:
        #     t = 0.0
        #     t_p = 0.0
        #     h = 0.0
        #     h_p = 0.0
        # print(eval(dic['data'][0]['t'][-1]))
        # if float(eval(dic['data'][0]['t'][-1])) <= 21:
        #     t_c = 'on'
        # if (float(eval(dic['data'][0]['t'][-1])) > 21) and (float(eval(dic['data'][0]['t'][-1])) <37):
        #     t_c = 'on'
        # if float(eval(dic['data'][0]['t'][-1])) >= 37:
        #     t_c = 'off'
        # if float(eval(dic['data'][1]['h'][-1])) <= 50:
        #     h_c = 'on'
        # if (float(eval(dic['data'][1]['h'][-1]))) > 50 and (float(eval(dic['data'][0]['t'][-1])) < 70):
        #     h_c = 'on'
        # if float(eval(dic['data'][1]['h'][-1])) >= 70:
        #     h_c = 'off'
            
        # if t <= 21:
        #     t_c = 'on'
        # if (t > 21) and (t <37):
        #     if (t-t_p < 0):
        #         t_c = 'off'
        #     if (t-t_p >= 0):
        #         t_c = 'on'
        # if t >= 37:
        #     t_c = 'off'
        # if h <= 50:
        #     h_c = 'on'
        # if (h > 50) and (h < 70):
        #     if (h-h_p < 0):
        #         h_c = 'off'
        #     if (h-h_p >= 0):
        #         h_c = 'on'
        # if h >= 70:
        #     h_c = 'off'

        command = ['fer_on']

        self.client.myPublish(self.topic,command)

        # with open('pub_command_log.json') as file:
        #     dic = json.load(file)
        # dic['data'][0]['Heating'] = t_c
        # dic['data'][1]['Watering'] = h_c

        # with open('pub_command_log.json','w') as file:
        #     json.dump(dic, file)

        print(command)
        
        time.sleep(1)

if __name__ == "__main__":
    # pub = False
    # dic = {'data':[{'t':['0']},{'h':['0']}]}
    # with open('data_log.json', 'w') as file:
    #     json.dump(dic, file)
        
    # conf_sub = json.load(open("ec_settings.json"))
    # broker_sub = conf_sub["broker"]
    # port_sub = conf_sub["port"]
    # topic_sub = conf_sub['baseTopic']
    # ec_sub = ec_sub("ec_sub", topic_sub, broker_sub, port_sub)
    # ec_sub.start()


    conf_pub=json.load(open("fer_command_setting.json"))
    broker_pub=conf_pub["broker"]
    port_pub=conf_pub["port"]
    topic_pub = conf_pub['baseTopic']
    com_pub = fer_com_pub("fer_com_pub",topic_pub,broker_pub,port_pub)
    com_pub.client.start()
    time.sleep(2)

    t_month = 2

    while True:
        # if pub:

        com_pub.publish()
        time.sleep(t_month)
     

            
                 

