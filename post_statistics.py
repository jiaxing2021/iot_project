
import torch
import torch.nn as nn
import json
import time
from MyMQTT import MyMQTT

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, (2,1))  # 3 input channels, 32 output channels, 1x2 kernel
        self.fc1 = nn.Linear(32, 64)
        self.fc2 = nn.Linear(64, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, 32)
        self.fc5 = nn.Linear(32, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = x.view(x.size()[0], -1)# flatten the output of the convolutional layers
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x = self.relu(x)
        x = self.fc4(x)
        x = self.relu(x)
        x = self.fc5(x)
        return x
class DNN(nn.Module):
    def __init__(self):
        super(DNN, self).__init__()
        self.fc1 = nn.Linear(3, 32)
        self.fc2 = nn.Linear(32, 1)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=0.2)
        
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x


class predicted_pub:
    def __init__(self, clientID, topic,broker,port):
        self.topic=topic
        self.client=MyMQTT(clientID,broker,port,None)
        
    def start (self):
        self.client.start()

    def stop (self):
        self.client.stop()

    def publish(self,temp_result,humid_result):
        
        predicted_data = [temp_result,humid_result]

        self.client.myPublish(self.topic,predicted_data)
        print(predicted_data)
        time.sleep(1)

if __name__ == "__main__":

    conf_pub=json.load(open("command_setting.json"))
    broker_pub=conf_pub["broker"]
    port_pub=conf_pub["port"]
    topic_pub = conf_pub['baseTopic']
    predicted_pub = predicted_pub("com_pub",topic_pub,broker_pub,port_pub)
    predicted_pub.client.start()
    time.sleep(2)

    temp_predicter = torch.load('DNN.pt')
    humid_predicter = torch.load('CNN.pt')

    sleeptime = 5
    t = sleeptime

    while True:
        # if pub:
        with open('sensor_log.json') as file:
            dic = json.load(file)
        
            data_temp = torch.tensor([eval(dic['data'][0]['t'][-3]), 
                    eval(dic['data'][0]['t'][-2]), 
                    eval(dic['data'][0]['t'][-1])])
        
            data_humid = torch.tensor([[[[eval(dic['data'][0]['t'][-3])],[eval(dic['data'][1]['h'][-3])]],
                        [[eval(dic['data'][0]['t'][-2])],[eval(dic['data'][1]['h'][-2])]],
                        [[eval(dic['data'][0]['t'][-1])],[eval(dic['data'][1]['h'][-1])]]]])
       
        temp_result = temp_predicter(data_temp)
        humid_result = humid_predicter(data_humid)
        temp_result = temp_result[0].item()
        humid_result = humid_result[0].item()
        temp_result = format(temp_result, '.2f')
        humid_result = format(humid_result, '.2f')

        temp_result = str(temp_result)
        humid_result = str(humid_result)
        predicted_pub.publish(temp_result, humid_result)
        try:
            with open('predicted_log.json') as file:
                dic = json.load(file)

            dic['data'][0]['t'].append(temp_result)
            dic['data'][1]['h'].append(humid_result)
            with open('predicted_log.json', 'w') as file:
                json.dump(dic, file)
        except:
            dic['data'][0]['t'] = temp_result
            dic['data'][1]['h'] = humid_result
            with open('predicted_log.json', 'w') as file:
                json.dump(dic, file)


        time.sleep(t)

